import pyautogui
import requests
import base64
import io

def read_screen(prompt="What do you see on this screen? Be specific."):
    # force screenshot of display 0 — the actual screen not camera
    screenshot = pyautogui.screenshot()
    
    buf = io.BytesIO()
    screenshot.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode()

    response = requests.post("http://localhost:11434/api/generate", json={
        "model": "llava",
        "prompt": f"This is a screenshot of a computer screen. Do not describe any physical objects or rooms. Only describe what software, apps, text, and UI elements you see on the screen. {prompt}",
        "images": [b64],
        "stream": False
    })
    return response.json()["response"]

if __name__ == "__main__":
    result = read_screen()
    print(result)