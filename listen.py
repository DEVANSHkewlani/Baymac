import whisper
import sounddevice as sd
import numpy as np
import subprocess
import time

model = whisper.load_model("base")

GARBAGE = [
    "thank you", "thanks for watching", "bye", "you",
    ".", "", " ", "subscribe", "like and subscribe"
]

def is_garbage(text):
    t = text.strip().lower()
    if len(t) < 4:
        return True
    if t in GARBAGE:
        return True
    if all(c in "0123456789.%, \n" for c in t):
        return True
    return False

def beep_start():
    subprocess.Popen(['afplay', '/System/Library/Sounds/Tink.aiff'])
    time.sleep(0.5)

def beep_stop():
    subprocess.Popen(['afplay', '/System/Library/Sounds/Pop.aiff'])
    time.sleep(0.5)

def listen(duration=5):
    print("🎙 Listening... (speak now)")
    beep_start()

    audio = sd.rec(
        int(16000 * duration),
        samplerate=16000,
        channels=1,
        dtype="float32"
    )
    sd.wait()
    beep_stop()

    print("⏹ Done recording. Processing...")
    audio = audio.flatten()
    result = model.transcribe(audio, fp16=False)
    text = result["text"].strip()

    if is_garbage(text):
        print(f"⚠️ Ignored: '{text}'")
        return ""

    print(f"✅ You said: {text}")
    return text

if __name__ == "__main__":
    result = listen()
    print(f"Final: {result}")