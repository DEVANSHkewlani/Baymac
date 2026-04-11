from listen import listen
from see import read_screen
from speak import speak
import time

GARBAGE_PHRASES = ["thank you", "thanks for watching", "bye", "you"]

def is_garbage(text):
    if len(text.strip()) < 3:
        return True
    if text.strip().lower() in GARBAGE_PHRASES:
        return True
    # whisper hallucination — only numbers/symbols
    if all(c in "0123456789.% \n" for c in text.strip()):
        return True
    return False

def run():
    speak("Agent is ready. Ask me anything.")

    while True:
        command = listen(duration=5)

        if not command or is_garbage(command):
            print("⚠️ No valid command detected, listening again...")
            time.sleep(1)
            continue

        if "exit" in command.lower():
            speak("Shutting down.")
            break

        speak("Let me check the screen.")
        description = read_screen(
            prompt=f"You are a screen reading assistant. Look at this screenshot carefully and answer this question about what you see on screen: {command}"
        )
        speak(description)
        time.sleep(1)   # pause before listening again

if __name__ == "__main__":
    run()