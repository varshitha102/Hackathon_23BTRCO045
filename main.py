import cv2
import speech_recognition as sr
import pyttsx3
import requests
import wikipedia
import datetime
import webbrowser
import threading
import time
import os
from deepface import DeepFace
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
API_KEY = os.getenv("GOOGLE_API")
genai.configure(api_key=API_KEY)
engine = pyttsx3.init()
current_emotion = "neutral"
last_response = None

def fetch_gemini_response(query):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(query)
        return response.text if response.text else "I'm not sure about that."
    except Exception as e:
        return f"Error fetching AI response: {e}"

def assistant_tasks(command):
    if "time" in command:
        response = f"The current time is {datetime.datetime.now().strftime('%I:%M %p')}."
    elif "search" in command:
        query = command.replace("search", "").strip()
        response = f"Searching for {query} on Google..."
        webbrowser.open(f"https://www.google.com/search?q={query}")
    elif "wikipedia" in command or "tell me about" in command:
        query = command.replace("wikipedia", "").replace("tell me about", "").strip()
        response = fetch_gemini_response(query)
    elif "open youtube" in command:
        response = "Opening YouTube..."
        webbrowser.open("https://www.youtube.com")
    elif "open google" in command:
        response = "Opening Google..."
        webbrowser.open("https://www.google.com")
    else:
        response = fetch_gemini_response(command)
    print(f"AI: {response}")
    engine.say(response)
    engine.runAndWait()

def analyze_emotion():
    global current_emotion
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        for (x, y, w, h) in faces:
            face_img = frame[y:y+h, x:x+w]
            if face_img.size > 0:
                try:
                    analysis = DeepFace.analyze(face_img, actions=["emotion"], enforce_detection=False)
                    if analysis and isinstance(analysis, list):
                        new_emotion = analysis[0]["dominant_emotion"]
                        if new_emotion != current_emotion:
                            current_emotion = new_emotion
                            print(f"Updated Emotion: {current_emotion}")
                except Exception as e:
                    print("Emotion Analysis Error:", e)
        time.sleep(3)

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            return recognizer.recognize_google(audio).lower()
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand that.")
        except sr.RequestError:
            print("Speech service is unavailable.")
        except Exception as e:
            print(f"Speech Recognition Error: {e}")
    return None

def generate_response(command):
    global last_response
    responses = {
        "happy": "You sound happy! Want to hear a joke?",
        "sad": "I'm here for you. How about a fun fact to cheer you up?",
        "angry": "I understand you're upset. Maybe a deep breath would help?",
        "surprise": "Wow! That sounds exciting! Tell me more!",
        "fear": "It's okay, you're safe. Want me to play some calming music?",
        "neutral": "How can I assist you today?"
    }
    response = responses.get(current_emotion, "I'm here to listen. How can I help?")
    if response != last_response:
        engine.say(response)
        engine.runAndWait()
        print(f"AI: {response}")
        last_response = response

def continuous_listening():
    while True:
        command = recognize_speech()
        if command:
            print(f"User said: {command}")
            generate_response(command)
            assistant_tasks(command)

def main():
    threading.Thread(target=analyze_emotion, daemon=True).start()
    threading.Thread(target=continuous_listening, daemon=True).start()
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()