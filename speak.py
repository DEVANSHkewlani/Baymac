import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 0.9)

def speak(text):
    print(f"Agent: {text}")
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    speak("Hello, I am your voice agent.")