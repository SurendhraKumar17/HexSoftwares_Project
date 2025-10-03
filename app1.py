import datetime
import time
import pyttsx3
import wikipedia
import pywhatkit
import speech_recognition as sr


engine = pyttsx3.init()
engine.setProperty("rate", 150)
 
reminders = [] 

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio)
            print("You:", command)
            return command.lower()
    except:
        return input("Type your command: ").lower()

def check_reminders():
    now = datetime.datetime.now().strftime("%H:%M")
    for r in reminders:
        if r["time"] == now and not r["done"]:
            speak(f"Reminder: {r['msg']}")
            r["done"] = True

def main():
    speak("Hello! I am your assistant. Say something.")
    while True:
        check_reminders()
        command = listen()

        if "time" in command:
            now = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The time is {now}")

        elif "remind me" in command:
            try:
                parts = command.split("at")
                msg = parts[0].replace("remind me", "").strip()
                time_str = parts[1].strip()
                reminders.append({"msg": msg, "time": time_str, "done": False})
                speak(f"Reminder set for {time_str}")
            except:
                speak("Please say like: remind me take medicine at 14:30")

        elif "wikipedia" in command or "who is" in command or "what is" in command:
            topic = command.replace("wikipedia", "").replace("who is", "").replace("what is", "").strip()
            try:
                info = wikipedia.summary(topic, sentences=2)
                speak(info)
            except:
                speak("Sorry, I couldn't find that.")

        elif "play" in command:
            song = command.replace("play", "").strip()
            speak(f"Playing {song} on YouTube.")
            pywhatkit.playonyt(song)

        elif "exit" in command or "quit" in command:
            speak("Goodbye!")
            break

        else:
            speak("I can tell time, set reminders, search Wikipedia, or play YouTube."),
        
        time.sleep(2)

if __name__ == "__main__":
    main()


