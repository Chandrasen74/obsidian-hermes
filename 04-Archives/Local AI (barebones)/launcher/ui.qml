import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import Qt.labs.platform 1.1 as Platform

ApplicationWindow {
    id: root
    width: 860
    height: 780
    minimumWidth: 640
    minimumHeight: 560
    title: "Local AI Launcher"
    visible: true
    color: "#0f0f11"

    property int selectedModelIndex: -1
    property var filteredIndexMap: []

    readonly property color bg:         "#0f0f11"
    readonly property color surface:    "#1a1a1f"
    readonly property color surfaceAlt: "#22222a"
    readonly property color border:     "#2e2e38"
    readonly property color accent:     "#7c6ff7"
    readonly property color accentHov:  "#9a90ff"
    readonly property color danger:     "#e05c5c"
    readonly property color dangerHov:  "#f07070"
    readonly property color success:    "#4caf6e"
    readonly property color textPri:    "#e8e8f0"
    readonly property color textSec:    "#8a8a9a"
    readonly property color textMono:   "#a0d0b0"

    Platform.FileDialog {
        id: fileDialog
        title: "Select a GGUF model file"
        nameFilters: ["GGUF files (*.gguf)"]
        onAccepted: {
            if (launcher.add_model(file.toString())) {
                refreshModelList()
            }
        }
    }

    Connections {
        target: launcher
        function onLogLine(line) {
            logModel.append({ "text": line })
            if (logModel.count > 500) logModel.remove(0)
            logView.positionViewAtEnd()
        }
        function onIsRunningChanged() {
            if (!launcher.is_running) {
                logModel.append({ "text": "── server stopped ──" })
                logView.positionViewAtEnd()
            }
        }
    }

    ListModel { id: logModel }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 16
        spacing: 12

        RowLayout {
            Layout.fillWidth: true

            Text {
                text: "Local AI Launcher"
                color: root.textPri
                font.pixelSize: 20
                font.weight: Font.DemiBold
            }

            Item { Layout.fillWidth: true }

            Rectangle {
                width: statusRow.implicitWidth + 20
                height: 28
                radius: 14
                color: launcher.is_running ? "#1a3a26" : "#2a1a1a"
                border.color: launcher.is_running ? root.success : root.danger
                border.width: 1

                RowLayout {
                    id: statusRow
                    anchors.centerIn: parent
                    spacing: 6

                    Rectangle {
                        width: 8; height: 8; radius: 4
                        color: launcher.is_running ? root.success : root.danger
                    }
                    Text {
                        text: launcher.status_text
                        color: launcher.is_running ? root.success : root.danger
                        font.pixelSize: 12
                    }
                }
            }
        }

        Rectangle { Layout.fillWidth: true; height: 1; color: root.border }

        Rectangle {
            Layout.fillWidth: true
            color: root.surface
            radius: 8
            border.color: root.border
            border.width: 1
            implicitHeight: modelCardCol.implicitHeight + 24

            ColumnLayout {
                id: modelCardCol
                anchors { left: parent.left; right: parent.right; top: parent.top; margins: 12 }
                spacing: 8

                Text {
                    text: "MODEL"
                    color: root.textSec
                    font.pixelSize: 11
                    font.weight: Font.Medium
                    font.letterSpacing: 1.2
                }

                RowLayout {
                    Layout.fillWidth: true
                    spacing: 8

                    Rectangle {
                        Layout.fillWidth: true
                        height: 36
                        radius: 6
                        color: root.surfaceAlt
                        border.color: modelSearch.activeFocus ? root.accent : root.border
                        border.width: 1

                        TextInput {
                            id: modelSearch
                            anchors { left: parent.left; right: parent.right; verticalCenter: parent.verticalCenter; leftMargin: 10; rightMargin: 10 }
                            color: root.textPri
                            font.pixelSize: 13
                            clip: true
                            onTextChanged: filterModels()

                            Text {
                                anchors.fill: parent
                                text: "Search models..."
                                color: root.textSec
                                font.pixelSize: 13
                                visible: parent.text.length === 0
                                verticalAlignment: Text.AlignVCenter
                            }
                        }
                    }

                    Rectangle {
                        height: 36
                        width: addGgufLabel.implicitWidth + 24
                        radius: 6
                        color: addGgufMouse.containsMouse ? root.surfaceAlt : root.surface
                        border.color: root.border
                        border.width: 1

                        Text {
                            id: addGgufLabel
                            anchors.centerIn: parent
                            text: "+ Add .gguf"
                            color: root.textPri
                            font.pixelSize: 13
                        }
                        MouseArea {
                            id: addGgufMouse
                            anchors.fill: parent
                            hoverEnabled: true
                            cursorShape: Qt.PointingHandCursor
                            onClicked: fileDialog.open()
                        }
                    }

                    Rectangle {
                        height: 36
                        width: pruneLabel.implicitWidth + 24
                        radius: 6
                        color: pruneMouse.containsMouse ? root.surfaceAlt : root.surface
                        border.color: root.border
                        border.width: 1

                        Text {
                            id: pruneLabel
                            anchors.centerIn: parent
                            text: "Prune Missing"
                            color: root.textSec
                            font.pixelSize: 13
                        }
                        MouseArea {
                            id: pruneMouse
                            anchors.fill: parent
                            hoverEnabled: true
                            cursorShape: Qt.PointingHandCursor
                            onClicked: {
                                var removed = launcher.prune_missing_models()
                                if (removed > 0) {
                                    root.selectedModelIndex = -1
                                    refreshModelList()
                                }
                            }
                        }
                    }
                }

                ComboBox {
                    id: modelCombo
                    Layout.fillWidth: true
                    model: []

                    contentItem: Text {
                        leftPadding: 10
                        text: modelCombo.displayText
                        color: root.textPri
                        font.pixelSize: 13
                        verticalAlignment: Text.AlignVCenter
                        elide: Text.ElideRight
                    }

                    background: Rectangle {
                        radius: 6
                        color: root.surfaceAlt
                        border.color: modelCombo.popup.visible ? root.accent : root.border
                        border.width: 1
                    }

                    popup: Popup {
                        y: modelCombo.height
                        width: modelCombo.width
                        padding: 4

                        background: Rectangle {
                            color: root.surfaceAlt
                            radius: 6
                            border.color: root.border
                            border.width: 1
                        }

                        contentItem: ListView {
                            implicitHeight: Math.min(contentHeight, 240)
                            model: modelCombo.delegateModel
                            clip: true
                            ScrollBar.vertical: ScrollBar {}
                        }
                    }

                    delegate: ItemDelegate {
                        width: modelCombo.width
                        contentItem: Text {
                            text: modelData
                            color: root.textPri
                            font.pixelSize: 13
                            elide: Text.ElideRight
                        }
                        background: Rectangle {
                            color: hovered ? root.border : "transparent"
                            radius: 4
                        }
                    }

                    onActivated: function(index) {
                        if (index >= 0 && index < root.filteredIndexMap.length) {
                            saveCurrentArgsState()
                            root.selectedModelIndex = root.filteredIndexMap[index]
                            updateModelInfo()
                        }
                    }
                }
            }
        }

        Rectangle {
            Layout.fillWidth: true
            color: root.surface
            radius: 8
            border.color: root.border
            border.width: 1
            visible: root.selectedModelIndex >= 0
            implicitHeight: modelInfoCol.implicitHeight + 24

            ColumnLayout {
                id: modelInfoCol
                anchors { left: parent.left; right: parent.right; top: parent.top; margins: 12 }
                spacing: 8

                Text {
                    text: "CONFIGURATION"
                    color: root.textSec
                    font.pixelSize: 11
                    font.weight: Font.Medium
                    font.letterSpacing: 1.2
                }

                RowLayout {
                    Layout.fillWidth: true
                    spacing: 10

                    Text { text: "Executable"; color: root.textSec; font.pixelSize: 12; Layout.preferredWidth: 90 }

                    ComboBox {
                        id: executableCombo
                        Layout.fillWidth: true
                        model: Object.keys(launcher.executables)
                        currentIndex: {
                            if (root.selectedModelIndex < 0) return -1
                            var exeName = launcher.get_executable_name(root.selectedModelIndex)
                            return model.indexOf(exeName)
                        }

                        contentItem: Text {
                            leftPadding: 10
                            text: executableCombo.displayText
                            color: root.textPri
                            font.pixelSize: 12
                            font.family: "Consolas"
                            verticalAlignment: Text.AlignVCenter
                            elide: Text.ElideLeft
                        }

                        background: Rectangle {
                            radius: 6
                            color: root.surfaceAlt
                            border.color: executableCombo.popup.visible ? root.accent : root.border
                            border.width: 1
                        }

                        popup: Popup {
                            y: executableCombo.height
                            width: executableCombo.width
                            padding: 4
                            background: Rectangle {
                                color: root.surfaceAlt; radius: 6
                                border.color: root.border; border.width: 1
                            }
                            contentItem: ListView {
                                implicitHeight: Math.min(contentHeight, 160)
                                model: executableCombo.delegateModel
                                clip: true
                            }
                        }

                        delegate: ItemDelegate {
                            width: executableCombo.width
                            contentItem: Text {
                                text: modelData
                                color: root.textPri
                                font.pixelSize: 12
                                elide: Text.ElideRight
                            }
                            background: Rectangle {
                                color: hovered ? root.border : "transparent"; radius: 4
                            }
                        }

                        onActivated: function(index) {
                            if (root.selectedModelIndex >= 0)
                                launcher.set_executable(root.selectedModelIndex, model[index])
                        }
                    }
                }

                RowLayout {
                    Layout.fillWidth: true
                    spacing: 10

                    Text { text: "Model File"; color: root.textSec; font.pixelSize: 12; Layout.preferredWidth: 90 }

                    Text {
                        text: root.selectedModelIndex >= 0 ? launcher.models[root.selectedModelIndex].model_file : ""
                        color: root.textMono
                        font.pixelSize: 11
                        font.family: "Consolas"
                        elide: Text.ElideLeft
                        Layout.fillWidth: true
                    }

                    Rectangle {
                        height: 28
                        width: removeLbl.implicitWidth + 20
                        radius: 5
                        color: removeMouse.containsMouse ? "#3a1a1a" : "transparent"
                        border.color: root.danger
                        border.width: 1

                        Text {
                            id: removeLbl
                            anchors.centerIn: parent
                            text: "Remove"
                            color: root.danger
                            font.pixelSize: 12
                        }
                        MouseArea {
                            id: removeMouse
                            anchors.fill: parent
                            hoverEnabled: true
                            cursorShape: Qt.PointingHandCursor
                            onClicked: {
                                if (launcher.remove_model(root.selectedModelIndex)) {
                                    root.selectedModelIndex = -1
                                    refreshModelList()
                                }
                            }
                        }
                    }
                }
            }
        }

        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.minimumHeight: 120
            color: root.surface
            radius: 8
            border.color: root.border
            border.width: 1

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 12
                spacing: 8

                Text {
                    text: "ARGUMENTS"
                    color: root.textSec
                    font.pixelSize: 11
                    font.weight: Font.Medium
                    font.letterSpacing: 1.2
                }

                ScrollView {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    clip: true
                    ScrollBar.horizontal.policy: ScrollBar.AlwaysOff

                    Column {
                        width: parent.width
                        spacing: 4

                        Repeater {
                            id: argsRepeater
                            model: root.selectedModelIndex >= 0 ? launcher.models[root.selectedModelIndex].args : []

                            RowLayout {
                                width: parent.width
                                spacing: 8

                                Rectangle {
                                    width: 18; height: 18; radius: 4
                                    color: chkArea.containsMouse ? root.surfaceAlt : root.bg
                                    border.color: argCheck.checked ? root.accent : root.border
                                    border.width: 1

                                    property alias checked: argCheck.checked

                                    CheckBox {
                                        id: argCheck
                                        anchors.centerIn: parent
                                        checked: modelData.enabled || false
                                        indicator: Item {}
                                    }
                                    Rectangle {
                                        anchors.centerIn: parent
                                        width: 10; height: 10; radius: 2
                                        color: root.accent
                                        visible: argCheck.checked
                                    }
                                    MouseArea {
                                        id: chkArea
                                        anchors.fill: parent
                                        hoverEnabled: true
                                        cursorShape: Qt.PointingHandCursor
                                        onClicked: argCheck.checked = !argCheck.checked
                                    }
                                }

                                Text {
                                    text: modelData.name || ""
                                    color: root.textMono
                                    font.family: "Consolas"
                                    font.pixelSize: 12
                                    Layout.preferredWidth: 140
                                    elide: Text.ElideRight
                                }

                                Rectangle {
                                    Layout.fillWidth: true
                                    height: 28
                                    radius: 5
                                    color: root.surfaceAlt
                                    border.color: argField.activeFocus ? root.accent : root.border
                                    border.width: 1

                                    TextInput {
                                        id: argField
                                        anchors { left: parent.left; right: parent.right; verticalCenter: parent.verticalCenter; leftMargin: 8; rightMargin: 8 }
                                        text: modelData.value !== undefined ? modelData.value : ""
                                        color: root.textPri
                                        font.pixelSize: 12
                                        font.family: "Consolas"
                                        clip: true

                                        Text {
                                            anchors.fill: parent
                                            text: "(flag only)"
                                            color: root.textSec
                                            font.pixelSize: 12
                                            visible: parent.text.length === 0
                                            verticalAlignment: Text.AlignVCenter
                                        }
                                    }
                                }

                                Rectangle {
                                    width: 24; height: 24; radius: 4
                                    color: rmArgMouse.containsMouse ? "#3a1a1a" : "transparent"
                                    border.color: rmArgMouse.containsMouse ? root.danger : root.border
                                    border.width: 1

                                    Text {
                                        anchors.centerIn: parent
                                        text: "✕"
                                        color: rmArgMouse.containsMouse ? root.danger : root.textSec
                                        font.pixelSize: 11
                                    }
                                    MouseArea {
                                        id: rmArgMouse
                                        anchors.fill: parent
                                        hoverEnabled: true
                                        cursorShape: Qt.PointingHandCursor
                                        onClicked: {
                                            launcher.remove_arg(root.selectedModelIndex, index)
                                            updateModelInfo()
                                        }
                                    }
                                }
                            }
                        }
                    }
                }

                RowLayout {
                    Layout.fillWidth: true
                    spacing: 8

                    Rectangle {
                        width: 140; height: 28; radius: 5
                        color: root.surfaceAlt
                        border.color: newArgName.activeFocus ? root.accent : root.border
                        border.width: 1

                        TextInput {
                            id: newArgName
                            anchors { fill: parent; leftMargin: 8; rightMargin: 8 }
                            color: root.textPri
                            font.pixelSize: 12
                            font.family: "Consolas"
                            verticalAlignment: TextInput.AlignVCenter
                            clip: true

                            Text {
                                anchors.fill: parent
                                text: "Arg (e.g. -c)"
                                color: root.textSec
                                font.pixelSize: 12
                                visible: parent.text.length === 0
                                verticalAlignment: Text.AlignVCenter
                            }
                        }
                    }

                    Rectangle {
                        Layout.fillWidth: true; height: 28; radius: 5
                        color: root.surfaceAlt
                        border.color: newArgValue.activeFocus ? root.accent : root.border
                        border.width: 1

                        TextInput {
                            id: newArgValue
                            anchors { fill: parent; leftMargin: 8; rightMargin: 8 }
                            color: root.textPri
                            font.pixelSize: 12
                            font.family: "Consolas"
                            verticalAlignment: TextInput.AlignVCenter
                            clip: true

                            Text {
                                anchors.fill: parent
                                text: "Value (optional)"
                                color: root.textSec
                                font.pixelSize: 12
                                visible: parent.text.length === 0
                                verticalAlignment: Text.AlignVCenter
                            }
                        }
                    }

                    Rectangle {
                        height: 28
                        width: addArgLbl.implicitWidth + 20
                        radius: 5
                        color: addArgMouse.containsMouse ? root.surfaceAlt : root.surface
                        border.color: root.border
                        border.width: 1
                        opacity: newArgName.text.length > 0 && root.selectedModelIndex >= 0 ? 1 : 0.4

                        Text {
                            id: addArgLbl
                            anchors.centerIn: parent
                            text: "Add Arg"
                            color: root.textPri
                            font.pixelSize: 12
                        }
                        MouseArea {
                            id: addArgMouse
                            anchors.fill: parent
                            hoverEnabled: true
                            cursorShape: Qt.PointingHandCursor
                            enabled: newArgName.text.length > 0 && root.selectedModelIndex >= 0
                            onClicked: {
                                launcher.add_arg(root.selectedModelIndex, newArgName.text, newArgValue.text)
                                newArgName.text = ""
                                newArgValue.text = ""
                                updateModelInfo()
                            }
                        }
                    }
                }
            }
        }

        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 160
            color: root.bg
            radius: 8
            border.color: root.border
            border.width: 1

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 10
                spacing: 6

                RowLayout {
                    Layout.fillWidth: true

                    Text {
                        text: "SERVER LOG"
                        color: root.textSec
                        font.pixelSize: 11
                        font.weight: Font.Medium
                        font.letterSpacing: 1.2
                    }

                    Item { Layout.fillWidth: true }

                    Rectangle {
                        height: 22
                        width: clrLbl.implicitWidth + 16
                        radius: 4
                        color: clrMouse.containsMouse ? root.surfaceAlt : "transparent"
                        border.color: clrMouse.containsMouse ? root.border : "transparent"
                        border.width: 1

                        Text {
                            id: clrLbl
                            anchors.centerIn: parent
                            text: "Clear"
                            color: root.textSec
                            font.pixelSize: 11
                        }
                        MouseArea {
                            id: clrMouse
                            anchors.fill: parent
                            hoverEnabled: true
                            cursorShape: Qt.PointingHandCursor
                            onClicked: logModel.clear()
                        }
                    }
                }

                ListView {
                    id: logView
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    model: logModel
                    clip: true
                    spacing: 1
                    ScrollBar.vertical: ScrollBar {}

                    delegate: Text {
                        width: logView.width - 12
                        text: model.text
                        color: model.text.indexOf("error") >= 0 || model.text.indexOf("Error") >= 0
                               ? "#e07070"
                               : model.text.indexOf("──") >= 0
                               ? root.textSec
                               : root.textMono
                        font.family: "Consolas"
                        font.pixelSize: 11
                        wrapMode: Text.WrapAnywhere
                    }

                    Text {
                        anchors.centerIn: parent
                        text: "No output yet. Start a model to see logs."
                        color: root.textSec
                        font.pixelSize: 12
                        visible: logModel.count === 0
                    }
                }
            }
        }

        RowLayout {
            Layout.fillWidth: true
            spacing: 10

            Rectangle {
                height: 40
                width: 120
                radius: 8
                color: launcher.is_running || root.selectedModelIndex < 0
                       ? root.surfaceAlt
                       : (launchMouse.containsMouse ? root.accentHov : root.accent)
                opacity: launcher.is_running || root.selectedModelIndex < 0 ? 0.5 : 1

                Text {
                    anchors.centerIn: parent
                    text: "Launch"
                    color: root.textPri
                    font.pixelSize: 14
                    font.weight: Font.DemiBold
                }
                MouseArea {
                    id: launchMouse
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    enabled: !launcher.is_running && root.selectedModelIndex >= 0
                    onClicked: {
                        if (root.selectedModelIndex >= 0) {
                            var enabledArgs = []
                            var argValues = []
                            for (var i = 0; i < argsRepeater.count; i++) {
                                var item = argsRepeater.itemAt(i)
                                if (item) {
                                    enabledArgs.push(item.children[0].checked)
                                    argValues.push(item.children[2].children[0].text || "")
                                }
                            }
                            logModel.append({ "text": "── launching " + launcher.models[root.selectedModelIndex].name + " ──" })
                            logView.positionViewAtEnd()
                            launcher.launch(root.selectedModelIndex, enabledArgs, argValues)
                        }
                    }
                }
            }

            Rectangle {
                height: 40
                width: 100
                radius: 8
                color: !launcher.is_running
                       ? root.surfaceAlt
                       : (stopMouse.containsMouse ? root.dangerHov : root.danger)
                opacity: !launcher.is_running ? 0.4 : 1

                Text {
                    anchors.centerIn: parent
                    text: "Stop"
                    color: root.textPri
                    font.pixelSize: 14
                    font.weight: Font.DemiBold
                }
                MouseArea {
                    id: stopMouse
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    enabled: launcher.is_running
                    onClicked: launcher.stop_process()
                }
            }

            Item { Layout.fillWidth: true }

            Rectangle {
                height: 36
                width: saveOvLbl.implicitWidth + 24
                radius: 7
                color: saveOvMouse.containsMouse ? root.surfaceAlt : root.surface
                border.color: root.border
                border.width: 1
                opacity: root.selectedModelIndex >= 0 ? 1 : 0.4

                Text {
                    id: saveOvLbl
                    anchors.centerIn: parent
                    text: "Save Overrides"
                    color: root.textSec
                    font.pixelSize: 12
                }
                MouseArea {
                    id: saveOvMouse
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    enabled: root.selectedModelIndex >= 0
                    onClicked: {
                        var argsData = []
                        for (var i = 0; i < argsRepeater.count; i++) {
                            var item = argsRepeater.itemAt(i)
                            if (item) {
                                var argModel = launcher.models[root.selectedModelIndex].args[i]
                                argsData.push({
                                    "name": argModel.name,
                                    "value": item.children[2].children[0].text || "",
                                    "enabled": item.children[0].checked
                                })
                            }
                        }
                        launcher.save_overrides(root.selectedModelIndex, argsData)
                    }
                }
            }
        }
    }

    function filterModels() {
        var allModels = launcher.models
        var search = modelSearch.text.toLowerCase()
        var filteredNames = []
        root.filteredIndexMap = []
        var newComboIndex = -1

        for (var i = 0; i < allModels.length; i++) {
            if (search === "" || allModels[i].name.toLowerCase().indexOf(search) >= 0) {
                if (i === root.selectedModelIndex) {
                    newComboIndex = filteredNames.length
                }
                filteredNames.push(allModels[i].name)
                root.filteredIndexMap.push(i)
            }
        }

        modelCombo.model = filteredNames
        if (newComboIndex >= 0) {
            modelCombo.currentIndex = newComboIndex
        }
    }

    function refreshModelList() {
        modelSearch.text = ""
        filterModels()
    }

    function saveCurrentArgsState() {
        if (root.selectedModelIndex >= 0 && argsRepeater.count > 0) {
            var argsData = []
            for (var i = 0; i < argsRepeater.count; i++) {
                var item = argsRepeater.itemAt(i)
                if (item) {
                    var argModel = launcher.models[root.selectedModelIndex].args[i]
                    argsData.push({
                        "name": argModel.name,
                        "value": item.children[2].children[0].text || "",
                        "enabled": item.children[0].checked
                    })
                }
            }
            launcher.update_model_args(root.selectedModelIndex, argsData)
        }
    }

    function updateModelInfo() {
        argsRepeater.model = []
        if (root.selectedModelIndex >= 0 && root.selectedModelIndex < launcher.models.length) {
            argsRepeater.model = launcher.models[root.selectedModelIndex].args
        }
    }

    Component.onCompleted: {
        refreshModelList()
        if (root.filteredIndexMap.length > 0) {
            modelCombo.currentIndex = 0
            root.selectedModelIndex = root.filteredIndexMap[0]
            updateModelInfo()
        }
    }
}
