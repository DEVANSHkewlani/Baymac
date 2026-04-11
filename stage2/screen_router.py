import subprocess

def get_context():
    script = '''
    tell application "System Events"
        get name of first process whose frontmost is true
    end tell
    '''
    result = subprocess.run(
        ['osascript', '-e', script],
        capture_output=True, text=True
    )
    app = result.stdout.strip()
    browsers = ["Google Chrome", "Safari", "Firefox", "Arc"]
    
    if app in browsers:
        return "browser"
    return "desktop"