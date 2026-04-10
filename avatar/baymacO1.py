from Foundation import NSMakeRect
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
    NSTimer,
    NSStatusBar,
    NSVariableStatusItemLength,
    NSMenu,
    NSMenuItem,
)
import objc
import subprocess

char_window_ref = None
char_view_ref   = None
x_pos           = 0.0
frame_index     = 0
direction       = 1
dock_w          = 0.0
dock_h          = 0.0
dock_x          = 0.0
overlay_h       = 62
char_w          = 50
avatar_enabled  = True


def get_dock_icon_bounds():
    script = '''
    tell application "System Events"
        tell process "Dock"
            set dockList to list 1
            set dockPos to position of dockList
            set dockSize to size of dockList
            return (item 1 of dockPos as string) & "," & (item 2 of dockPos as string) & "," & (item 1 of dockSize as string) & "," & (item 2 of dockSize as string)
        end tell
    end tell
    '''
    result = subprocess.run(
        ['osascript', '-e', script],
        capture_output=True, text=True
    )
    data = result.stdout.strip().split(',')
    if len(data) == 4:
        return float(data[0]), float(data[2])
    return None, None


class CharacterView(NSView):

    def initWithFrame_(self, frame):
        self = objc.super(CharacterView, self).initWithFrame_(frame)
        if self is None:
            return None
        self._frame     = 0
        self._direction = 1
        return self

    @objc.python_method
    def setWalkFrame_(self, f):
        self._frame = f

    @objc.python_method
    def setDirection_(self, d):
        self._direction = d

    @objc.python_method
    def drawCharacter(self):
        f = self._frame
        d = self._direction

        # head
        NSColor.colorWithCalibratedRed_green_blue_alpha_(
            0.95, 0.75, 0.55, 1.0
        ).set()
        NSBezierPath.bezierPathWithOvalInRect_(
            NSMakeRect(14, 38, 22, 22)
        ).fill()

        # hair
        NSColor.colorWithCalibratedRed_green_blue_alpha_(
            0.25, 0.15, 0.05, 1.0
        ).set()
        NSBezierPath.bezierPathWithOvalInRect_(
            NSMakeRect(13, 48, 24, 14)
        ).fill()

        # body
        NSColor.colorWithCalibratedRed_green_blue_alpha_(
            0.3, 0.5, 0.9, 1.0
        ).set()
        NSBezierPath.bezierPathWithRect_(
            NSMakeRect(13, 20, 24, 20)
        ).fill()

        # legs
        NSColor.colorWithCalibratedRed_green_blue_alpha_(
            0.15, 0.15, 0.35, 1.0
        ).set()
        if f == 0:
            NSBezierPath.bezierPathWithRect_(NSMakeRect(10, 4, 7, 16)).fill()
            NSBezierPath.bezierPathWithRect_(NSMakeRect(31, 4, 7, 16)).fill()
        else:
            NSBezierPath.bezierPathWithRect_(NSMakeRect(17, 4, 7, 16)).fill()
            NSBezierPath.bezierPathWithRect_(NSMakeRect(24, 4, 7, 16)).fill()

        # shoes
        NSColor.colorWithCalibratedRed_green_blue_alpha_(
            0.1, 0.1, 0.1, 1.0
        ).set()
        if f == 0:
            NSBezierPath.bezierPathWithOvalInRect_(NSMakeRect(6,  0, 12, 6)).fill()
            NSBezierPath.bezierPathWithOvalInRect_(NSMakeRect(28, 0, 12, 6)).fill()
        else:
            NSBezierPath.bezierPathWithOvalInRect_(NSMakeRect(13, 0, 12, 6)).fill()
            NSBezierPath.bezierPathWithOvalInRect_(NSMakeRect(21, 0, 12, 6)).fill()

        # arms
        NSColor.colorWithCalibratedRed_green_blue_alpha_(
            0.3, 0.5, 0.9, 1.0
        ).set()
        if f == 0:
            NSBezierPath.bezierPathWithRect_(NSMakeRect(37, 20, 7, 18)).fill()
            NSBezierPath.bezierPathWithRect_(NSMakeRect(6,  20, 7, 18)).fill()
        else:
            NSBezierPath.bezierPathWithRect_(NSMakeRect(6,  20, 7, 18)).fill()
            NSBezierPath.bezierPathWithRect_(NSMakeRect(37, 20, 7, 18)).fill()

        # hands
        NSColor.colorWithCalibratedRed_green_blue_alpha_(
            0.95, 0.75, 0.55, 1.0
        ).set()
        NSBezierPath.bezierPathWithOvalInRect_(NSMakeRect(4,  17, 8, 8)).fill()
        NSBezierPath.bezierPathWithOvalInRect_(NSMakeRect(38, 17, 8, 8)).fill()

        # eyes
        NSColor.colorWithCalibratedRed_green_blue_alpha_(
            0.1, 0.1, 0.1, 1.0
        ).set()
        eye_offset = 2 if d == 1 else -2
        NSBezierPath.bezierPathWithOvalInRect_(
            NSMakeRect(18 + eye_offset, 46, 4, 4)
        ).fill()
        NSBezierPath.bezierPathWithOvalInRect_(
            NSMakeRect(28 + eye_offset, 46, 4, 4)
        ).fill()

        # eye shine
        NSColor.whiteColor().set()
        NSBezierPath.bezierPathWithOvalInRect_(
            NSMakeRect(19 + eye_offset, 47, 1.5, 1.5)
        ).fill()
        NSBezierPath.bezierPathWithOvalInRect_(
            NSMakeRect(29 + eye_offset, 47, 1.5, 1.5)
        ).fill()

        # mouth
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

    def mouseDown_(self, event):
        # open Siri — most reliable way on M1 macOS
        print("Avatar clicked — opening Siri")
        subprocess.Popen(['open', '-a', 'Siri'])


class AppDelegate(NSObject):

    def applicationDidFinishLaunching_(self, notification):
        global char_window_ref, char_view_ref
        global x_pos, dock_w, dock_h, dock_x

        screen  = NSScreen.mainScreen()
        visible = screen.visibleFrame()

        dock_h = visible.origin.y

        icon_x, icon_w = get_dock_icon_bounds()
        if icon_x is not None:
            dock_x = icon_x
            dock_w = icon_w
        else:
            dock_x = visible.origin.x
            dock_w = visible.size.width

        x_pos = dock_x

        # character window
        self.char_window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            NSMakeRect(dock_x, dock_h, char_w, overlay_h),
            NSBorderlessWindowMask, NSBackingStoreBuffered, False
        )
        self.char_window.setBackgroundColor_(NSColor.clearColor())
        self.char_window.setOpaque_(False)
        self.char_view = CharacterView.alloc().initWithFrame_(
            NSMakeRect(0, 0, char_w, overlay_h)
        )
        self.char_window.setContentView_(self.char_view)
        self.char_window.setLevel_(25)
        self.char_window.setCollectionBehavior_(1 << 0)
        self.char_window.makeKeyAndOrderFront_(None)

        char_window_ref = self.char_window
        char_view_ref   = self.char_view

        # walk timer
        self.timer = NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
            1.0 / 30.0, self, 'tick:', None, True
        )

        # ── menu bar status item ────────────────────────────────────────
        self.status_item = NSStatusBar.systemStatusBar().statusItemWithLength_(
            NSVariableStatusItemLength
        )
        self.status_item.button().setTitle_("🤖")

        # build dropdown menu
        self.menu = NSMenu.alloc().init()

        # toggle item — starts ON with checkmark
        self.toggle_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            "✦ Avatar: ON", "toggleAvatar:", ""
        )
        self.toggle_item.setTarget_(self)
        self.toggle_item.setState_(1)   # checkmark = ON at startup
        self.menu.addItem_(self.toggle_item)

        self.menu.addItem_(NSMenuItem.separatorItem())

        # info label
        info = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            "Click avatar → opens Siri", None, ""
        )
        info.setEnabled_(False)
        self.menu.addItem_(info)

        self.menu.addItem_(NSMenuItem.separatorItem())

        # quit
        quit_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            "Quit BayMac", "quitApp:", ""
        )
        quit_item.setTarget_(self)
        self.menu.addItem_(quit_item)

        self.status_item.setMenu_(self.menu)

    def toggleAvatar_(self, sender):
        global avatar_enabled

        avatar_enabled = not avatar_enabled

        if avatar_enabled:
            char_window_ref.makeKeyAndOrderFront_(None)
            self.timer = NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
                1.0 / 30.0, self, 'tick:', None, True
            )
            self.toggle_item.setTitle_("✦ Avatar: ON")
            self.toggle_item.setState_(1)
        else:
            char_window_ref.orderOut_(None)
            self.timer.invalidate()
            self.toggle_item.setTitle_("✦ Avatar: OFF")
            self.toggle_item.setState_(0)

    def quitApp_(self, sender):
        NSApplication.sharedApplication().terminate_(None)

    def tick_(self, timer):
        global x_pos, frame_index, direction

        if not avatar_enabled:
            return

        x_pos += 1.5 * direction

        right_limit = dock_x + dock_w - char_w
        left_limit  = dock_x

        if x_pos >= right_limit:
            x_pos     = right_limit
            direction = -1
            char_view_ref.setDirection_(-1)
        elif x_pos <= left_limit:
            x_pos     = left_limit
            direction = 1
            char_view_ref.setDirection_(1)

        char_window_ref.setFrame_display_(
            NSMakeRect(x_pos, dock_h, char_w, overlay_h), False
        )

        frame_index += 1
        char_view_ref.setWalkFrame_((frame_index // 5) % 2)
        char_view_ref.setNeedsDisplay_(True)


app = NSApplication.sharedApplication()
app.setActivationPolicy_(1)
delegate = AppDelegate.alloc().init()
app.setDelegate_(delegate)
app.run()