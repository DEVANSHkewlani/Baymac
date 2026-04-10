from AppKit import (
    NSApplication,
    NSWindow,
    NSColor,
    NSBackingStoreBuffered,
    NSBorderlessWindowMask,
    NSScreen,
    NSObject,
)
from Foundation import NSMakeRect
import objc

class AppDelegate(NSObject):
    def applicationDidFinishLaunching_(self, notification):
        screen = NSScreen.mainScreen()
        visible_frame = screen.visibleFrame()

        dock_h = visible_frame.origin.y
        dock_w = visible_frame.size.width
        dock_x = visible_frame.origin.x
        overlay_h = 62
        char_w = 50

        print(f"Dock height: {dock_h}  Dock width: {dock_w}")

        # red strip — full width, click through
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

        # character window — small purple box
        char_frame = NSMakeRect(dock_x, dock_h, char_w, overlay_h)
        self.char_window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            char_frame, NSBorderlessWindowMask, NSBackingStoreBuffered, False
        )
        self.char_window.setBackgroundColor_(
            NSColor.colorWithCalibratedRed_green_blue_alpha_(0.4, 0.2, 0.8, 0.9)
        )
        self.char_window.setOpaque_(False)
        self.char_window.setLevel_(26)
        self.char_window.setCollectionBehavior_(1 << 0)
        self.char_window.makeKeyAndOrderFront_(None)

        print("Windows created successfully")


app = NSApplication.sharedApplication()
app.setActivationPolicy_(1)
delegate = AppDelegate.alloc().init()
app.setDelegate_(delegate)
app.run()