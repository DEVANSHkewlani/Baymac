from AppKit import (
    NSApplication,
    NSWindow,
    NSColor,
    NSBackingStoreBuffered,
    NSBorderlessWindowMask,
)
from Foundation import NSMakeRect

app = NSApplication.sharedApplication()

frame = NSMakeRect(200, 300, 400, 200)

window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
    frame,
    NSBorderlessWindowMask,
    NSBackingStoreBuffered,
    False
)

window.setBackgroundColor_(NSColor.colorWithCalibratedRed_green_blue_alpha_(
    0.4, 0.2, 0.8, 0.5
))
window.setOpaque_(False)
window.setTitle_("My Overlay")
window.makeKeyAndOrderFront_(None)

app.run()