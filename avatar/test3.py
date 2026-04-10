from AppKit import (
    NSApplication,
    NSWindow,
    NSColor,
    NSBackingStoreBuffered,
    NSBorderlessWindowMask,
    NSScreen,
    NSView,
    NSObject,
    NSBezierPath,
)
from Foundation import NSMakeRect
import objc

class CharacterView(NSView):

    @objc.python_method
    def drawCharacter(self):

        # head — oval fill only
        NSColor.colorWithCalibratedRed_green_blue_alpha_(
            0.95, 0.75, 0.55, 1.0
        ).set()
        NSBezierPath.bezierPathWithOvalInRect_(
            NSMakeRect(14, 38, 22, 22)
        ).fill()

        # hair — oval fill only
        NSColor.colorWithCalibratedRed_green_blue_alpha_(
            0.25, 0.15, 0.05, 1.0
        ).set()
        NSBezierPath.bezierPathWithOvalInRect_(
            NSMakeRect(13, 48, 24, 14)
        ).fill()

        # body — rect fill only
        NSColor.colorWithCalibratedRed_green_blue_alpha_(
            0.3, 0.5, 0.9, 1.0
        ).set()
        NSBezierPath.bezierPathWithRect_(
            NSMakeRect(13, 20, 24, 20)
        ).fill()

        # left leg — thin rect instead of stroke
        NSColor.colorWithCalibratedRed_green_blue_alpha_(
            0.15, 0.15, 0.35, 1.0
        ).set()
        NSBezierPath.bezierPathWithRect_(
            NSMakeRect(14, 4, 7, 16)
        ).fill()

        # right leg — thin rect instead of stroke
        NSBezierPath.bezierPathWithRect_(
            NSMakeRect(29, 4, 7, 16)
        ).fill()

        # left shoe
        NSColor.colorWithCalibratedRed_green_blue_alpha_(
            0.1, 0.1, 0.1, 1.0
        ).set()
        NSBezierPath.bezierPathWithOvalInRect_(
            NSMakeRect(9, 0, 12, 6)
        ).fill()

        # right shoe
        NSBezierPath.bezierPathWithOvalInRect_(
            NSMakeRect(29, 0, 12, 6)
        ).fill()

        # left arm — thin rect instead of stroke
        NSColor.colorWithCalibratedRed_green_blue_alpha_(
            0.3, 0.5, 0.9, 1.0
        ).set()
        NSBezierPath.bezierPathWithRect_(
            NSMakeRect(6, 20, 7, 18)
        ).fill()

        # right arm — thin rect instead of stroke
        NSBezierPath.bezierPathWithRect_(
            NSMakeRect(37, 20, 7, 18)
        ).fill()

        # left hand
        NSColor.colorWithCalibratedRed_green_blue_alpha_(
            0.95, 0.75, 0.55, 1.0
        ).set()
        NSBezierPath.bezierPathWithOvalInRect_(
            NSMakeRect(4, 17, 8, 8)
        ).fill()

        # right hand
        NSBezierPath.bezierPathWithOvalInRect_(
            NSMakeRect(38, 17, 8, 8)
        ).fill()

        # left eye
        NSColor.colorWithCalibratedRed_green_blue_alpha_(
            0.1, 0.1, 0.1, 1.0
        ).set()
        NSBezierPath.bezierPathWithOvalInRect_(
            NSMakeRect(18, 46, 4, 4)
        ).fill()

        # right eye
        NSBezierPath.bezierPathWithOvalInRect_(
            NSMakeRect(28, 46, 4, 4)
        ).fill()

        # eye shine left
        NSColor.whiteColor().set()
        NSBezierPath.bezierPathWithOvalInRect_(
            NSMakeRect(19, 47, 1.5, 1.5)
        ).fill()

        # eye shine right
        NSBezierPath.bezierPathWithOvalInRect_(
            NSMakeRect(29, 47, 1.5, 1.5)
        ).fill()

        # mouth — small oval instead of curve stroke
        NSColor.colorWithCalibratedRed_green_blue_alpha_(
            0.5, 0.1, 0.1, 1.0
        ).set()
        NSBezierPath.bezierPathWithOvalInRect_(
            NSMakeRect(19, 39, 12, 4)
        ).fill()

    def drawRect_(self, rect):
        NSColor.clearColor().set()
        NSBezierPath.bezierPathWithRect_(self.bounds()).fill()
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

        print(f"Dock height: {dock_h}  Dock width: {dock_w}")

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

        self.char_view = CharacterView.alloc().initWithFrame_(
            NSMakeRect(0, 0, char_w, overlay_h)
        )
        self.char_window.setContentView_(self.char_view)
        self.char_window.setLevel_(26)
        self.char_window.setCollectionBehavior_(1 << 0)
        self.char_window.makeKeyAndOrderFront_(None)


app = NSApplication.sharedApplication()
app.setActivationPolicy_(1)
delegate = AppDelegate.alloc().init()
app.setDelegate_(delegate)
app.run()