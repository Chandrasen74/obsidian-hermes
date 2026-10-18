#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys
import subprocess
from pathlib import Path
from PySide6.QtCore import QObject, Property, Signal, Slot, QUrl, QProcess
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine

class Launcher(QObject):
    def __init__(self, config_path):
        super().__init__()
        self._config_path = Path(config_path)
        self._overrides_path = self._config_path.parent / "llm_launcher_overrides.json"
        self._models = []
        self._executables = {}
        self._process = None
        self._is_running = False
        self._status_text = "Stopped"
        self._running_port = ""
        self._running_model = ""
        self.load_config()

    modelsChanged = Signal()
    executablesChanged = Signal()
    isRunningChanged = Signal()
    statusTextChanged = Signal()
    logLine = Signal(str)

    @Property(str, notify=statusTextChanged)
    def status_text(self):
        return self._status_text

    @Property('QVariantMap', notify=executablesChanged)
    def executables(self):
        return self._executables

    @Property('QVariantList', notify=modelsChanged)
    def models(self):
        return [{
            'name': m['name'],
            'executable': m.get('executable', ''),
            'model_file': m['model_file'],
            'args': m.get('args', [])
        } for m in self._models]

    @Property(bool, notify=isRunningChanged)
    def is_running(self):
        return self._is_running

    def load_config(self):
        try:
            with open(self._config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)

            default_args = config.get('default_args', [])
            self._executables = config.get('executables', {})
            # Add default executable to the executables map if it exists
            if 'default_executable' in config and config['default_executable']:
                self._executables['default'] = config['default_executable']
            self.executablesChanged.emit()
            self._models = []

            for model in config.get('models', []):
                # Deep copy each arg dict so models don't share references
                model_args = [arg.copy() for arg in default_args]
                for extra_arg in model.get('args', []):
                    model_args.append(extra_arg.copy())

                # Handle executable selection
                executable = model.get('executable', config.get('default_executable', ''))
                if 'executable_name' in model and model['executable_name'] in self._executables:
                    executable = self._executables[model['executable_name']]

                self._models.append({
                    'name': model['name'],
                    'executable': executable or config.get('default_executable', ''),
                    'model_file': model['model_file'],
                    'args': model_args
                })

            # Apply overrides from the separate overrides file
            self._apply_overrides()

            self.modelsChanged.emit()
            return True

        except Exception as e:
            print(f"Error loading config: {e}", file=sys.stderr)
            return False

    def _apply_overrides(self):
        """Apply saved overrides from llm_launcher_overrides.json"""
        if not self._overrides_path.exists():
            return
        try:
            with open(self._overrides_path, 'r', encoding='utf-8') as f:
                overrides = json.load(f)

            model_overrides = overrides.get('model_overrides', {})
            for model in self._models:
                name = model['name']
                if name in model_overrides:
                    ov = model_overrides[name]
                    # Apply executable override
                    if 'executable_name' in ov and ov['executable_name'] in self._executables:
                        model['executable'] = self._executables[ov['executable_name']]
                    # Apply arg overrides (full replacement)
                    if 'args' in ov:
                        model['args'] = [a.copy() for a in ov['args']]
        except Exception as e:
            print(f"Error loading overrides: {e}", file=sys.stderr)

    @Slot(int, 'QVariantList', 'QVariantList', result=bool)
    def launch(self, model_index, args_enabled, args_values):
        try:
            if self._is_running:
                print("Error: Process already running", file=sys.stderr)
                return False

            model = self._models[model_index]
            if not model['executable']:
                print("Error: No executable specified", file=sys.stderr)
                return False

            cmd = [model['executable']]

            # Add model file
            cmd.extend(['-m', model['model_file']])

            # Add enabled arguments, using UI-edited values
            port = ""
            for i, arg in enumerate(model['args']):
                if i < len(args_enabled) and args_enabled[i]:
                    cmd.append(arg['name'])
                    # Use the value from the UI (args_values) if available,
                    # otherwise fall back to the config value
                    value = ''
                    if i < len(args_values) and args_values[i]:
                        value = str(args_values[i])
                    elif 'value' in arg and arg['value']:
                        value = str(arg['value'])
                    if value:
                        cmd.append(value)
                    # Track port for status display
                    if arg['name'] == '--port':
                        port = value

            print(f"Launching: {' '.join(cmd)}")

            # Start the process
            self._process = QProcess()
            self._process.finished.connect(self._on_process_finished)
            self._process.errorOccurred.connect(self._on_process_error)
            self._process.readyReadStandardOutput.connect(self._on_stdout_ready)
            self._process.readyReadStandardError.connect(self._on_stderr_ready)
            self._process.start(cmd[0], cmd[1:])

            if self._process.waitForStarted(5000):  # Wait up to 5 seconds
                self._is_running = True
                self._running_model = model['name']
                self._running_port = port
                if port:
                    self._status_text = f"Running: {model['name']} on :{port}"
                else:
                    self._status_text = f"Running: {model['name']}"
                self.isRunningChanged.emit()
                self.statusTextChanged.emit()
                return True
            else:
                print("Error: Failed to start process", file=sys.stderr)
                self._process = None
                return False

        except Exception as e:
            print(f"Error launching model: {e}", file=sys.stderr)
            self._process = None
            return False

    @Slot(int, str)
    def set_executable(self, model_index, executable_name):
        """Update the executable for a model. Does NOT emit modelsChanged
        so the model ComboBox selection is preserved."""
        if 0 <= model_index < len(self._models):
            if executable_name in self._executables:
                self._models[model_index]['executable'] = self._executables[executable_name]
            elif executable_name == 'default' and 'default' in self._executables:
                self._models[model_index]['executable'] = self._executables['default']
            else:
                self._models[model_index]['executable'] = executable_name
            # Intentionally NOT emitting modelsChanged to avoid resetting model ComboBox

    @Slot(int, result=str)
    def get_executable_name(self, model_index):
        """Get the name of the current executable for a model"""
        if 0 <= model_index < len(self._models):
            exe_path = self._models[model_index].get('executable', '')
            # Find the name of the executable in our executables map
            for name, path in self._executables.items():
                if path == exe_path:
                    return name
            # If not found, return the path itself
            return exe_path
        return ''

    @Slot(int, 'QVariantList')
    def update_model_args(self, model_index, args_data):
        """Sync UI arg edits back to in-memory model so they survive model switching."""
        if 0 <= model_index < len(self._models):
            args_list = []
            for arg in args_data:
                args_list.append({
                    'name': arg.get('name', ''),
                    'value': arg.get('value', ''),
                    'enabled': bool(arg.get('enabled', False))
                })
            self._models[model_index]['args'] = args_list

    @Slot(str, result=bool)
    def add_model(self, file_path):
        """Add a new .gguf model to the BASE config and reload"""
        try:
            # Handle file:/// URLs from QML FileDialog
            if file_path.startswith("file:///"):
                file_path = QUrl(file_path).toLocalFile()

            p = Path(file_path)
            if not p.exists():
                print(f"Error: File not found: {file_path}", file=sys.stderr)
                return False

            # Load current base config
            with open(self._config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)

            # Check if model already exists
            for m in config.get('models', []):
                if Path(m['model_file']).resolve() == p.resolve():
                    print(f"Model already exists: {file_path}", file=sys.stderr)
                    return False

            # Add new model entry to base config
            new_model = {
                "name": p.stem,
                "model_file": str(p.resolve())
            }
            config.setdefault('models', []).append(new_model)

            # Save to base config
            with open(self._config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)

            print(f"Added model: {new_model['name']}")

            # Reload everything
            self.load_config()
            return True

        except Exception as e:
            print(f"Error adding model: {e}", file=sys.stderr)
            return False

    @Slot(result=int)
    def prune_missing_models(self):
        """Remove models from the BASE config whose model_file does not exist"""
        try:
            with open(self._config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)

            original_count = len(config.get('models', []))
            kept_models = []
            for m in config.get('models', []):
                if Path(m['model_file']).expanduser().exists():
                    kept_models.append(m)

            removed_count = original_count - len(kept_models)
            if removed_count > 0:
                config['models'] = kept_models
                with open(self._config_path, 'w', encoding='utf-8') as f:
                    json.dump(config, f, indent=2, ensure_ascii=False)
                print(f"Pruned {removed_count} missing models from config")
                self.load_config()

            return removed_count

        except Exception as e:
            print(f"Error pruning models: {e}", file=sys.stderr)
            return 0

    @Slot(int, result=bool)
    def remove_model(self, model_index):
        """Remove a specific model from the BASE config"""
        try:
            if model_index < 0 or model_index >= len(self._models):
                return False

            model_to_remove = self._models[model_index]

            with open(self._config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)

            # Find the model in the config by its name and file path
            original_models = config.get('models', [])
            new_models = []
            removed = False
            for m in original_models:
                if not removed and m['name'] == model_to_remove['name'] and m['model_file'] == model_to_remove['model_file']:
                    removed = True
                    continue
                new_models.append(m)

            if removed:
                config['models'] = new_models
                with open(self._config_path, 'w', encoding='utf-8') as f:
                    json.dump(config, f, indent=2, ensure_ascii=False)
                print(f"Removed model: {model_to_remove['name']}")
                self.load_config()
                return True

            return False
        except Exception as e:
            print(f"Error removing model: {e}", file=sys.stderr)
            return False

    @Slot(int, str, str)
    def add_arg(self, model_index, name, value):
        """Add a new argument to a model (in-memory only, save via save_overrides)"""
        if 0 <= model_index < len(self._models):
            self._models[model_index]['args'].append({
                'name': name,
                'value': value,
                'enabled': True
            })
            self.modelsChanged.emit()

    @Slot(int, int)
    def remove_arg(self, model_index, arg_index):
        """Remove an argument from a model (in-memory only, save via save_overrides)"""
        if 0 <= model_index < len(self._models):
            args = self._models[model_index]['args']
            if 0 <= arg_index < len(args):
                removed = args.pop(arg_index)
                print(f"Removed arg: {removed['name']}")
                self.modelsChanged.emit()

    @Slot(int, 'QVariantList')
    def save_overrides(self, model_index, args_data):
        """Save the current model's arg state and executable to the overrides file.
        The base config is never modified by this — overrides are stored separately."""
        try:
            if model_index < 0 or model_index >= len(self._models):
                return

            model = self._models[model_index]

            # Load existing overrides or start fresh
            overrides = {}
            if self._overrides_path.exists():
                with open(self._overrides_path, 'r', encoding='utf-8') as f:
                    overrides = json.load(f)

            model_overrides = overrides.setdefault('model_overrides', {})

            # Find current executable name
            exe_name = ''
            exe_path = model.get('executable', '')
            for name, path in self._executables.items():
                if path == exe_path:
                    exe_name = name
                    break

            # Build the override entry from the UI data
            args_list = []
            for arg in args_data:
                args_list.append({
                    'name': arg.get('name', ''),
                    'value': arg.get('value', ''),
                    'enabled': bool(arg.get('enabled', False))
                })

            model_overrides[model['name']] = {
                'executable_name': exe_name,
                'args': args_list
            }

            with open(self._overrides_path, 'w', encoding='utf-8') as f:
                json.dump(overrides, f, indent=2, ensure_ascii=False)

            # Also update in-memory state so it stays consistent
            model['args'] = args_list

            print(f"Overrides saved for model: {model['name']}")

        except Exception as e:
            print(f"Error saving overrides: {e}", file=sys.stderr)

    @Slot()
    def stop_process(self):
        """Stop the running process"""
        if self._process and self._is_running:
            print("Stopping process...")
            self._process.terminate()
            if not self._process.waitForFinished(3000):  # Wait up to 3 seconds
                print("Process didn't terminate, killing it...")
                self._process.kill()
                self._process.waitForFinished()

    def _on_process_finished(self, exit_code, exit_status):
        """Called when the process finishes"""
        print(f"Process finished with exit code: {exit_code}")
        self._is_running = False
        self._status_text = "Stopped"
        self._running_model = ""
        self._running_port = ""
        self.isRunningChanged.emit()
        self.statusTextChanged.emit()
        self._process = None

    def _on_process_error(self, error):
        """Called when the process encounters an error"""
        print(f"Process error: {error}")
        self._is_running = False
        self._status_text = "Stopped (error)"
        self._running_model = ""
        self._running_port = ""
        self.isRunningChanged.emit()
        self.statusTextChanged.emit()
        self._process = None

    def _on_stdout_ready(self):
        """Called when process has stdout data available"""
        if self._process:
            data = self._process.readAllStandardOutput().data().decode('utf-8', errors='ignore')
            print(data, end='', flush=True)
            for line in data.splitlines():
                if line.strip():
                    self.logLine.emit(line)

    def _on_stderr_ready(self):
        """Called when process has stderr data available"""
        if self._process:
            data = self._process.readAllStandardError().data().decode('utf-8', errors='ignore')
            print(data, end='', file=sys.stderr, flush=True)
            for line in data.splitlines():
                if line.strip():
                    self.logLine.emit(line)

    def cleanup(self):
        """Clean up resources before exit"""
        if self._is_running:
            self.stop_process()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Get config path from command line or use default
    config_path = sys.argv[1] if len(sys.argv) > 1 else "llm_launcher_config.json"
    launcher = Launcher(config_path)

    # Set up cleanup on app exit
    app.aboutToQuit.connect(launcher.cleanup)

    # Set up QML engine
    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("launcher", launcher)
    engine.load(QUrl.fromLocalFile(str(Path(__file__).parent / "ui.qml")))

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())
