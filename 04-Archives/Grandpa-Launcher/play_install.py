# installs given packages from the Play Store automatically:
#   python play_install.py com.Version1 com.csam.icici.bank.imobile
import sys
import tempfile
import time

import uiautomator2 as u2

TEMP = tempfile.gettempdir()


def log(m):
    print(m, flush=True)


def dump(d, tag=""):
    try:
        xml = d.dump_hierarchy()
        path = "%s\\play_%s.xml" % (TEMP, tag or "dump")
        with open(path, "w", encoding="utf-8") as f:
            f.write(xml)
        log("dump saved: " + path)
    except Exception as e:
        log("dump failed: " + str(e))


def open_play(d, pkg):
    d.press("home")
    time.sleep(1.0)
    d.shell('am start -a android.intent.action.VIEW -d "market://details?id=%s"' % pkg)
    time.sleep(5)


def click_first(d, labels):
    for label in labels:
        el = d(text=label)
        if el.exists(timeout=1):
            try:
                el.click()
                log("clicked: " + label)
                return True
            except Exception as e:
                log("click failed on %s: %s" % (label, str(e)))
    return False


def wait_installed(d, pkg, timeout=720):
    start = time.time()
    while time.time() - start < timeout:
        if d(text="Open").exists(timeout=1) or d(text="Uninstall").exists(timeout=1):
            return True
        click_first(d, ["Try again", "Continue", "Accept", "OK"])
        time.sleep(5)
    dump(d, pkg + "_timeout")
    return False


def main():
    pkgs = sys.argv[1:]
    if not pkgs:
        log("usage: play_install.py <pkg>...")
        return
    d = u2.connect()
    log("connected: " + str(getattr(d, "serial", "default")))
    d.screen_on()
    time.sleep(0.5)
    try:
        d.unlock()
    except Exception:
        pass
    d.shell("am start -n com.github.uiautomator/.ToastActivity -e showFloatWindow false")
    for pkg in pkgs:
        log("=== " + pkg + " ===")
        open_play(d, pkg)
        if not click_first(d, ["Install", "Update"]):
            log("no Install button found; dumping UI")
            dump(d, pkg + "_noinstall")
        else:
            ok = wait_installed(d, pkg)
            log("install result: " + str(ok))
        d.press("home")
        time.sleep(1)
    d.press("home")
    log("all done")


main()
