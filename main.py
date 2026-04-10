from listen import listen
from see import read_screen
from speak import speak

def run():
    speak("Agent is ready. Ask me anything.")

    while True:
        command = listen(duration=5)

        if not command:
            continue

        if "exit" in command.lower():
            speak("Shutting down.")
            break

        speak("Let me check the screen.")
        description = read_screen(
            prompt=f"You are a screen reading assistant. Look at this screenshot carefully and answer this question about what you see on screen: {command}"
        )
        speak(description)

if __name__ == "__main__":
    run()