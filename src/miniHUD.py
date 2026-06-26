import Cocoa
import Quartz
import ctypes


# =========================
# Retina scale 获取
# =========================
def get_scale():
    screen = Cocoa.NSScreen.mainScreen()
    return screen.backingScaleFactor()


class RectWindow(Cocoa.NSWindow):
    def canBecomeKeyWindow(self):
        return False

    def canBecomeMainWindow(self):
        return False


class MSSRectOverlay:

    def __init__(self):
        self.windows = []
        self.scale = get_scale()

        self.screen = Cocoa.NSScreen.mainScreen()
        self.screen_h = self.screen.frame().size.height

    # =========================
    # mss bbox 输入
    # (x1, y1, x2, y2)
    # =========================
    def add_rect_mss(self, x1, y1, x2, y2):

        w = x2 - x1
        h = y2 - y1

        # =========================
        # 坐标转换（核心）
        # mss(top-left)
        # → macOS(bottom-left)
        # =========================
        mac_x = x1
        mac_y = self.screen_h - y1 - h

        # Retina scaling（关键）
        frame = Cocoa.NSMakeRect(mac_x, mac_y, w, h)

        window = RectWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            frame,
            Cocoa.NSWindowStyleMaskBorderless,
            Cocoa.NSBackingStoreBuffered,
            False,
        )

        window.setOpaque_(False)
        window.setBackgroundColor_(Cocoa.NSColor.clearColor())
        window.setLevel_(Cocoa.NSScreenSaverWindowLevel)
        window.setIgnoresMouseEvents_(True)

        window.setCollectionBehavior_(
            Cocoa.NSWindowCollectionBehaviorCanJoinAllSpaces
            | Cocoa.NSWindowCollectionBehaviorFullScreenAuxiliary
        )

        # ===== border view =====
        view = Cocoa.NSView.alloc().initWithFrame_(Cocoa.NSMakeRect(0, 0, w, h))
        view.setWantsLayer_(True)

        layer = view.layer()
        layer.setBackgroundColor_(Cocoa.NSColor.clearColor().CGColor())
        layer.setBorderWidth_(1.0)
        layer.setBorderColor_(Cocoa.NSColor.redColor().CGColor())

        window.setContentView_(view)
        window.makeKeyAndOrderFront_(None)

        self.windows.append(window)

        return window

    def clear(self):
        for w in self.windows:
            w.orderOut_(None)
        self.windows = []


# =========================
# Demo
# =========================
class AppDelegate(Cocoa.NSObject):

    def applicationDidFinishLaunching_(self, notification):

        self.overlay = MSSRectOverlay()

        # 模拟 mss bbox（直接可用）
        self.overlay.add_rect_mss(480, 88, 1038, 96)
        self.overlay.add_rect_mss(610, 219, 927, 261)
        self.overlay.add_rect_mss(548, 104, 956, 162)

        self.i = 0

        self.timer = Cocoa.NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
            1.0, self, Cocoa.NSSelectorFromString("tick"), None, True
        )

    def tick(self):
        self.i += 10
        # self.overlay.add_rect_mss(200 + self.i, 300, 350 + self.i, 450)


if __name__ == "__main__":
    app = Cocoa.NSApplication.sharedApplication()
    delegate = AppDelegate.alloc().init()
    app.setDelegate_(delegate)
    app.run()
