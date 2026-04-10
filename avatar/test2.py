from AppKit import (
    NSApplication,
    NSWindow,
    NSColor,
    NSBackingStoreBuffered,
    NSBorderlessWindowMask,
    NSScreen,
    NSView,
    NSObject,
)
from Foundation import NSMakeRect
import objc

class CharacterView(NSView):

    @objc.python_method
    def drawCharacter(self):
        # head
        NSColor.colorWithCalibratedRed_green_blue_alpha_(
            0.95, 0.75, 0.55, 1.0
        ).set()
        from AppKit import NSBezierPath
        NSBezierPath.bezierPathWithOvalInRect_(
            NSMakeRect(14, 38, 22, 22)
        ).fill()

    def drawRect_(self, rect):
        # clear background
        NSColor.clearColor().set()
        from AppKit import NSBezierPath
        NSBezierPath.bezierPathWithRect_(self.bounds()).fill()
        # call our drawing method
        self.drawCharacter()


class AppDelegate(NSObject):
    def applicationDidFinishLaunching_(self, notification):
        screen = NSScreen.mainScreen()
        visible_frame = screen.visibleFrame()

        dock_h = visible_frame.origin.y
        dock_w = visible_frame.size.width
        dock_x = visible_frame.origin.x
        overlay_h = 62
        char_w = 50

        # red strip
        red_frame = NSMakeRect(dock_x, dock_h, dock_w, overlay_h)
        self.red_window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            red_frame, NSBorderlessWindowMask, NSBackingStoreBuffered, False
        )
        self.red_window.setBackgroundColor_(
            NSColor.colorWithCalibratedRed_green_blue_alpha_(1.0, 0.2, 0.2, 0.3)
        )
        self.red_window.setOpaque_(False)
        self.red_window.setIgnoresMouseEvents_(True)
        self.red_window.setLevel_(25)
        self.red_window.setCollectionBehavior_(1 << 0)
        self.red_window.makeKeyAndOrderFront_(None)

        # character window
        char_frame = NSMakeRect(dock_x, dock_h, char_w, overlay_h)
        self.char_window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            char_frame, NSBorderlessWindowMask, NSBackingStoreBuffered, False
        )
        self.char_window.setBackgroundColor_(NSColor.clearColor())
        self.char_window.setOpaque_(False)

        # attach view
        self.char_view = CharacterView.alloc().initWithFrame_(
            NSMakeRect(0, 0, char_w, overlay_h)
        )
        self.char_window.setContentView_(self.char_view)

        self.char_window.setLevel_(26)
        self.char_window.setCollectionBehavior_(1 << 0)
        self.char_window.makeKeyAndOrderFront_(None)

        print("Done — you should see red strip and a skin colored circle")


app = NSApplication.sharedApplication()
app.setActivationPolicy_(1)
delegate = AppDelegate.alloc().init()
app.setDelegate_(delegate)
app.run()