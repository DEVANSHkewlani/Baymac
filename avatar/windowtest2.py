from AppKit import (
    NSApplication,
    NSWindow,
    NSColor,
    NSBackingStoreBuffered,
    NSBorderlessWindowMask,
    NSScreen,
    NSView,
    NSBezierPath,
)
from Foundation import NSMakeRect, NSPointInRect
import objc

# ── Window 1: full width, fully transparent, ignores ALL mouse events ────────
# This is just the red visual strip — purely decorative, never catches clicks

class RedStripView(NSView):
    def drawRect_(self, rect):
        NSColor.colorWithCalibratedRed_green_blue_alpha_(
            1.0, 0.2, 0.2, 0.3
        ).set()
        NSBezierPath.bezierPathWithRect_(self.bounds()).fill()

# ── Window 2: only as wide as the purple box, catches clicks ─────────────────
# This sits on top of window 1, only covers the character zone

class CharacterView(NSView):
    def initWithFrame_(self, frame):
        self = objc.super(CharacterView, self).initWithFrame_(frame)
        if self is None:
            return None
        return self

    def mouseDown_(self, event):
        click = event.locationInWindow()
        print(f"Character clicked! x={click.x:.0f} y={click.y:.0f}")

    def drawRect_(self, rect):
        # purple box
        NSColor.colorWithCalibratedRed_green_blue_alpha_(
            0.4, 0.2, 0.8, 0.9
        ).set()
        NSBezierPath.bezierPathWithRect_(self.bounds()).fill()

        # white dot
        NSColor.whiteColor().set()
        NSBezierPath.bezierPathWithOvalInRect_(
            NSMakeRect(45, 20, 10, 10)
        ).fill()


app = NSApplication.sharedApplication()

screen = NSScreen.mainScreen()
visible_frame = screen.visibleFrame()
full_frame = screen.frame()

dock_h = visible_frame.origin.y    # 96px on your machine
dock_w = visible_frame.size.width  # 1680px on your machine
dock_x = visible_frame.origin.x
overlay_h = 50

print(f"Dock height: {dock_h}  Dock width: {dock_w}")

# ── Window 1: full red strip, ignores ALL clicks ─────────────────────────────
red_frame = NSMakeRect(dock_x, dock_h, dock_w, overlay_h)

red_window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
    red_frame, NSBorderlessWindowMask, NSBackingStoreBuffered, False
)
red_window.setBackgroundColor_(NSColor.clearColor())
red_window.setOpaque_(False)
red_window.setIgnoresMouseEvents_(True)   # ALL clicks pass through this window

red_view = RedStripView.alloc().initWithFrame_(
    NSMakeRect(0, 0, dock_w, overlay_h)
)
red_window.setContentView_(red_view)
red_window.setLevel_(25)
red_window.setCollectionBehavior_(1 << 0)
red_window.makeKeyAndOrderFront_(None)

# ── Window 2: small purple box, catches clicks ────────────────────────────────
# Position it at the left edge, same height as red strip
char_w = 100
char_frame = NSMakeRect(dock_x, dock_h, char_w, overlay_h)

char_window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
    char_frame, NSBorderlessWindowMask, NSBackingStoreBuffered, False
)
char_window.setBackgroundColor_(NSColor.clearColor())
char_window.setOpaque_(False)
# no setIgnoresMouseEvents — this window catches clicks normally

char_view = CharacterView.alloc().initWithFrame_(
    NSMakeRect(0, 0, char_w, overlay_h)
)
char_window.setContentView_(char_view)
char_window.setLevel_(26)   # one level above the red strip
char_window.setCollectionBehavior_(1 << 0)
char_window.makeKeyAndOrderFront_(None)

app.run()


"""from AppKit import (
    NSApplication,    # connects Python to the macOS window server
    NSWindow,         # creates an OS-level window
    NSColor,          # colors — clear, red, purple, white etc
    NSBackingStoreBuffered,   # renders window in memory before displaying
    NSBorderlessWindowMask,   # window with no title bar, no buttons, raw
    NSScreen,         # lets you read screen dimensions
    NSView,           # the canvas inside a window — you draw on this
    NSBezierPath,     # the drawing tool — rectangles, circles, curves
)
from Foundation import NSMakeRect, NSPointInRect
# NSMakeRect(x, y, w, h) — creates a rectangle
# NSPointInRect(point, rect) — checks if a point is inside a rectangle
import objc           # the bridge between Python and Objective-C

RedStripView — the visual background
pythonclass RedStripView(NSView):
    def drawRect_(self, rect):
macOS calls drawRect_ automatically every time this view needs to be drawn — on first show, when uncovered by another window, etc. You never call it yourself.
python        NSColor.colorWithCalibratedRed_green_blue_alpha_(
            1.0, 0.2, 0.2, 0.3   # red=1.0, green=0.2, blue=0.2, opacity=0.3
        ).set()
Picks up the drawing color like choosing a marker. .set() activates it — nothing is drawn yet.
python        NSBezierPath.bezierPathWithRect_(self.bounds()).fill()
self.bounds() = the full size of this view. Creates a rectangle that fills the entire view, then .fill() paints it with the color you just set. Result — semi-transparent red strip across the whole view.

CharacterView — the clickable character
pythonclass CharacterView(NSView):
    def initWithFrame_(self, frame):
        self = objc.super(CharacterView, self).initWithFrame_(frame)
initWithFrame_ is the constructor for NSView. You must call objc.super() — not Python's super() — because initWithFrame_ is an Objective-C method. objc.super() bridges correctly into the Objective-C world.
python        if self is None:
            return None
        return self
Standard Objective-C init pattern — always check if init returned nil before continuing.
python    def mouseDown_(self, event):
        click = event.locationInWindow()
        print(f"Character clicked! x={click.x:.0f} y={click.y:.0f}")
macOS calls mouseDown_ automatically when the user clicks inside this view's window. locationInWindow() gives you the x,y of the click in window coordinates. This is where you'll later open the chatbot.
python    def drawRect_(self, rect):
        NSColor.colorWithCalibratedRed_green_blue_alpha_(0.4, 0.2, 0.8, 0.9).set()
        NSBezierPath.bezierPathWithRect_(self.bounds()).fill()
Draws the purple box filling the entire character window (100×50px).
python        NSColor.whiteColor().set()
        NSBezierPath.bezierPathWithOvalInRect_(NSMakeRect(45, 20, 10, 10)).fill()
Draws a small white circle at x=45, y=20, width=10, height=10 — the dot in the center of the purple box. Just a visual marker for now.

Getting screen and Dock dimensions
pythonscreen = NSScreen.mainScreen()
visible_frame = screen.visibleFrame()
full_frame = screen.frame()
mainScreen() = your primary display. frame() = entire screen. visibleFrame() = screen minus Dock and menu bar.
pythondock_h = visible_frame.origin.y    # 96px — how tall your Dock is
dock_w = visible_frame.size.width  # 1680px — full width
dock_x = visible_frame.origin.x    # 0 — Dock starts at left edge
overlay_h = 50                     # our overlay is 50px tall
visible_frame.origin.y is the smartest line here. Because visibleFrame excludes the Dock, its origin.y starts exactly where the Dock ends — so it directly tells you the Dock height without any calculation.

Window 1 — the red strip
pythonred_frame = NSMakeRect(dock_x, dock_h, dock_w, overlay_h)
# x=0, y=96, width=1680, height=50
# sits exactly above the Dock, full width
pythonred_window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
    red_frame,
    NSBorderlessWindowMask,   # no title bar
    NSBackingStoreBuffered,   # standard rendering
    False                     # create immediately
)
pythonred_window.setBackgroundColor_(NSColor.clearColor())
red_window.setOpaque_(False)
# transparent background — only the red drawing shows
pythonred_window.setIgnoresMouseEvents_(True)
# THE KEY LINE for the red strip
# tells macOS: forward ALL mouse events straight through this window
# to whatever app is underneath — in this case, your Dock
pythonred_window.setLevel_(25)
# normal windows = 0
# menu bar = 24
# our overlay = 25, floats above everything
pythonred_window.setCollectionBehavior_(1 << 0)
# 1<<0 = canJoinAllSpaces
# window stays visible across all Mission Control desktops
pythonred_window.makeKeyAndOrderFront_(None)
# put the window on screen, bring it forward

Window 2 — the character window
pythonchar_w = 100
char_frame = NSMakeRect(dock_x, dock_h, char_w, overlay_h)
# x=0, y=96, width=100, height=50
# same y position as red strip, but only 100px wide
pythonchar_window.setLevel_(26)
# one level ABOVE the red strip (25)
# so character window is always on top of the background strip"""
