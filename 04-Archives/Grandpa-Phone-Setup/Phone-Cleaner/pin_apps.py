# ============================================================================
#  pin_apps.py - pins WhatsApp + Truecaller to the Moto home screen, then
#  drops one icon onto the other so the launcher auto-creates a folder.
#
#  Uses openatx/uiautomator2 (https://github.com/openatx/uiautomator2):
#  gestures are injected by Google's UiAutomator instrumentation on the
#  device, which launchers accept as real user input (raw `adb shell input`
#  drags are what Motorola launcher3 was rejecting).
#
#  Run:  python pin_apps.py  [screenshot_out.png]
#  Needs: phone connected, `uiautomator2 init` done once.
# ============================================================================

import sys
import time

import uiautomator2 as u2

WA, TC = "WhatsApp", "Truecaller"
# drop targets on the home workspace (1080x2400, third icon row is empty)
DROP = {WA: (430, 1450), TC: (750, 1450)}


def log(m):
    print(m, flush=True)


d = u2.connect()
log("connected: " + str(getattr(d, "serial", "default")))

# hide the ATX floating window if present
try:
    d.shell("am start -n com.github.uiautomator/.ToastActivity -e showFloatWindow false")
except Exception as e:
    log("float-window hide skipped: " + str(e))

d.screen_on()
time.sleep(0.6)
try:
    d.unlock()
except Exception as e:
    log("unlock skipped: " + str(e))
d.press("home")
time.sleep(1.5)


def bounds_of(el):
    info = el.info or {}
    b = info.get("visibleBounds") or info.get("bounds")
    if not b:
        return None
    return (b["left"] + b["right"]) // 2, (b["top"] + b["bottom"]) // 2


def find_on_home(name):
    """True if the app tile exists on the home workspace (not the drawer)."""
    d.press("home")
    time.sleep(1.2)
    return d(textContains=name).exists(timeout=3)


def locate_in_drawer(name):
    d.swipe(0.5, 0.88, 0.5, 0.40, 0.25)
    time.sleep(1.4)
    el = d(textContains=name)
    if not el.exists(timeout=3):
        for _ in range(2):
            d.swipe(0.5, 0.75, 0.5, 0.30, 0.3)
            time.sleep(0.9)
            if el.exists(timeout=1.5):
                break
    if not el.exists(timeout=2):
        return None
    c = bounds_of(el)
    return (el, c[0], c[1]) if c else None


def try_pin(name, tx, ty):
    if find_on_home(name):
        log(name + ": already on home, skipping")
        return True
    hit = locate_in_drawer(name)
    if not hit:
        log(name + ": NOT FOUND in drawer")
        return False
    el, cx, cy = hit
    log(name + ": drawer icon at " + str((cx, cy)) + ", pinning...")

    # A: object drag_to, slow
    try:
        el.drag_to(tx, ty, duration=2.0)
        time.sleep(1.6)
        if find_on_home(name):
            log(name + ": PINNED via drag_to")
            return True
    except Exception as e:
        log(name + ": drag_to failed: " + str(e))

    # B: one gesture, long stationary dwell then move (triggers long-press drag)
    d.swipe_points([(cx, cy)] * 10 + [(tx, ty)], 0.25)
    time.sleep(1.8)
    if find_on_home(name):
        log(name + ": PINNED via swipe_points dwell")
        return True

    # C: slow raw drag
    d.drag(cx, cy, tx, ty, 3.0)
    time.sleep(1.8)
    if find_on_home(name):
        log(name + ": PINNED via raw drag")
        return True

    log(name + ": drag strategies failed")
    return False


ok1 = try_pin(WA, *DROP[WA])
ok2 = try_pin(TC, *DROP[TC])
log("pin results: " + WA + "=" + str(ok1) + " " + TC + "=" + str(ok2))


def merge_folder():
    """Drag icon A onto icon B on the workspace; launcher auto-creates folder."""
    a = d(textContains=WA)
    if not a.exists(timeout=3):
        log("merge: " + WA + " not on home")
        return
    ac = bounds_of(a)
    if not ac:
        return
    acx, acy = ac
    # after merge attempt A, WhatsApp is inside the folder, so re-locate by the
    # surviving Truecaller tile: drop A's last position onto wherever B is now
    t = d(textContains=TC)
    if not t.exists(timeout=3):
        log("merge: " + TC + " not on home")
        return
    tc = bounds_of(t)
    tcx, tcy = tc
    log("merge: dragging " + str((acx, acy)) + " onto " + str((tcx, tcy)))

    try:
        a.drag_to(tcx, tcy, duration=2.0)
        time.sleep(1.8)
    except Exception as e:
        log("merge drag_to failed: " + str(e))

    if not d(textContains=WA).exists(timeout=2) and d(textContains=TC).exists(timeout=2):
        # WhatsApp no longer a standalone tile = it went inside the folder
        log("merge: folder created (drag_to)")
        return

    # dwell-style one-gesture attempt
    d.swipe_points([(acx, acy)] * 10 + [(tcx, tcy)], 0.25)
    time.sleep(2.0)
    if not d(textContains=WA).exists(timeout=2):
        log("merge: folder created (dwell)")
    else:
        log("merge: folder not confirmed, icons may sit side by side")


if ok1 and ok2:
    merge_folder()

# final state screenshot for the report
try:
    d.press("home")
    time.sleep(1.2)
    out = sys.argv[1] if len(sys.argv) > 1 else "pin_final.png"
    d.screenshot(out)
    log("screenshot saved: " + out)
except Exception as e:
    log("screenshot failed: " + str(e))

log("done")
