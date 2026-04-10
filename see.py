import pyautogui
import requests
import base64
import io

def read_screen(prompt="What do you see on this screen? Be specific."):
    screenshot = pyautogui.screenshot()

    buf = io.BytesIO()
    screenshot.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode()

    response = requests.post("http://localhost:11434/api/generate", json={
        "model": "llava",
        "prompt": prompt,
        "images": [b64],
        "stream": False
    })
    return response.json()["response"]

if __name__ == "__main__":
    result = read_screen()
    print(result)