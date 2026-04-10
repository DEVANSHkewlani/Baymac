import subprocess

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

print("Raw output:", result.stdout.strip())
print("Error if any:", result.stderr.strip())

# parse it
data = result.stdout.strip().split(',')
if len(data) == 4:
    dock_icon_x    = float(data[0])
    dock_icon_y    = float(data[1])
    dock_icon_w    = float(data[2])
    dock_icon_h    = float(data[3])
    print(f"\nDock icons start at x = {dock_icon_x}")
    print(f"Dock icons width     = {dock_icon_w}")
    print(f"Dock icons end at x  = {dock_icon_x + dock_icon_w}")
    print(f"Character should bounce between x={dock_icon_x} and x={dock_icon_x + dock_icon_w - 50}")