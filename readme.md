AI Voice Assistant with Emotion Detection

Overview

This assistant recognizes speech, detects emotions, and responds using Google Gemini AI. It can tell the time, search the web, fetch Wikipedia-like answers, and open websites.

Features

Voice Commands (time, search, Wikipedia, open YouTube/Google)

Emotion Detection (adapts responses based on facial expressions)

AI Responses (uses Gemini AI for general queries)

Text-to-Speech (TTS)


Setup

1. Install dependencies:

pip install opencv-python speechrecognition pyttsx3 requests wikipedia deepface python-dotenv google-generativeai


2. Set up .env with your Google API Key:

GOOGLE_API=your_google_api_key


3. Run the script:

python assistant.py



Commands

"What time is it?" → Tells the time

"Search Python tutorials" → Opens Google search

"Tell me about Einstein" → AI-generated response

"Open YouTube" → Opens YouTube


Notes

Ensure mic and camera permissions are enabled.

Check API key if AI responses fail.


License

Open-source, free to use.

