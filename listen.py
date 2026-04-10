import whisper
import sounddevice as sd
import numpy as np
import subprocess
import wave
import struct
import math
import os
import time

model = whisper.load_model("base")

def beep(frequency=440, duration=0.1):
    sr = 44100
    frames = [
        struct.pack('<h', int(32767 * math.sin(2 * math.pi * frequency * i / sr)))
        for i in range(int(sr * duration))
    ]
    tmp = "/tmp/beep.wav"
    w = wave.open(tmp, 'w')
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(sr)
    w.writeframes(b''.join(frames))
    w.close()
    subprocess.run(['afplay', tmp])
    os.remove(tmp)
    time.sleep(0.3)

def listen(duration=5):
    print("🎙 Listening... (speak now)")
    beep(440, 0.1)

    audio = sd.rec(
        int(16000 * duration),
        samplerate=16000,
        channels=1,
        dtype="float32"
    )
    sd.wait()

    beep(600, 0.1)
    print("⏹ Done recording. Processing...")

    audio = audio.flatten()
    result = model.transcribe(audio, fp16=False)
    text = result["text"].strip()
    print(f"✅ You said: {text}")
    return text

if __name__ == "__main__":
    result = listen()
    print(f"Final: {result}")