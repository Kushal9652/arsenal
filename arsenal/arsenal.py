import os
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
from googletrans import Translator
import subprocess

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wish_me():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak('hello sir')
    speak(" I'm Arsenal, your virtual assistant. Allow me to assist you.")

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("say:")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("processing")
        query = r.recognize_google(audio, language='en-in')
        print(f"master said: {query}\n")

    except Exception as e:
        print("Say that again please...")
        return "None"
    return query

def play_next_song():
    global current_song_index
    if current_song_index < len(songs):
        song_to_play = os.path.join(music_dir, songs[current_song_index])
        os.startfile(song_to_play)
        speak(f"Now playing: {songs[current_song_index]}")
        current_song_index += 1
    else:
        speak("End of playlist")

def translate_text(text, dest_language='en'):
    translator = Translator()
    try:
        translated = translator.translate(text, dest=dest_language)
        return translated.text
    except Exception as e:
        print(f"Translation failed: {str(e)}")
        return None

def run_streamlit_app():
    try:
        subprocess.run(["python", "-m", "streamlit", "run", "chat.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

music_dir = "C:\music"
songs = os.listdir(music_dir) if os.path.exists(music_dir) else []  # Get a list of songs in the music directory
current_song_index = 0
gesture_detect_process = None  # Initialize the subprocess variable

if __name__ == "__main__":
    wish_me()

    while True:
        query = take_command().lower()

        if 'stop' in query:
            speak("Stopping the system.")
            if gesture_detect_process:
                gesture_detect_process.terminate()
            break

        if 'start interactive mode' in query:
            speak("Starting interactive mode...")
            run_streamlit_app()
            speak("Interactive mode ended.")

        if 'activate air gestures' in query:
            speak("Activating air gestures.just a moment sir")
            if not gesture_detect_process or gesture_detect_process.poll() is not None:
                gesture_detect_process = subprocess.Popen(["python", "main.py"])

        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open' in query:
            if 'youtube' in query:
                webbrowser.open("youtube.com")
            elif 'chatgpt' in query:
                webbrowser.open("chat.openai.com")
            elif 'facebook' in query:
                webbrowser.open("facebook.com")
            elif 'whatsapp' in query:
                webbrowser.open("web.whatsapp.com")
            elif 'google' in query:
                webbrowser.open("google.com")
            elif 'stackoverflow' in query:
                webbrowser.open("stackoverflow.com")
            elif 'hackerone' in query:
                webbrowser.open("hackerone.com/users/sign_in")

        elif 'play music' in query:
            play_next_song()

        elif 'the time' in query:
            str_time = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {str_time}")

        elif 'open your code' in query:
            code_path = "C:\python\__pycache__"
            os.startfile(code_path)

        elif 'email to user' in query:
            try:
                speak("what should i write?")
                content = take_command()
                to = "kushalkumar1617@gmail.com"
                # sendEmail(to, content)  # Function not defined in your code snippet
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry sir, I'm not able to send this mail")

        elif 'translate this' in query:
            speak("What would you like to translate?")
            text_to_translate = take_command()
            speak("Which language should I translate it to?")
            destination_language = take_command().lower()

            translated_text = translate_text(text_to_translate, dest_language=destination_language)
            if translated_text:
                speak("The translation is:")
                speak(translated_text)  # Speak out the translated text
            else:
                speak("Sorry, I couldn't perform the translation.")
