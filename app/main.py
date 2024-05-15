import os
from fastapi import FastAPI, File, UploadFile
from googletrans import Translator
from gtts import gTTS
import speech_recognition as sr
from googletrans import Translator
import pyttsx3

app = FastAPI()


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    upload_folder = "uploaded_files"
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    with open(os.path.join(upload_folder, file.filename), "wb") as buffer:
        buffer.write(await file.read())
    return {"filename": file.filename}


def text_to_speech(text, output_file):
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()

    # Set properties (optional)
    engine.setProperty("rate", 150)  # Speed percent (can go over 100)
    engine.setProperty("volume", 1)  # Volume 0-1

    # Save audio to a file
    engine.save_to_file(text, output_file)

    # Wait for the speech to complete
    engine.runAndWait()


# def translate_to_tamil(text):
#     translated_text = translator.translate(text, dest="ta").text
#     return translated_text


@app.post("/translate")
async def translate_audio(file: UploadFile = File(...)):
    try:
        # Define the recognizer
        recognizer = sr.Recognizer()

        # Use the recognizer to open the audio file
        with sr.AudioFile(file.file) as source:
            # Listen for the data (load audio to memory)
            audio_data = recognizer.record(source)

            # Use Google Web Speech API to recognize the audio
            text = recognizer.recognize_google(audio_data)
            print("Text: ", text)
            # tamil_text = translate_to_tamil(text)
            # print("English: ", text)
            # print("Tamil: ", tamil_text)

            # Generate translated audio
            translated_audio_file = "translated_audio.mp3"
            translator = Translator()
            print(translated_text=translator.translate(text, src="en", dest="ta").text)
            translated_text = translator.translate(text, src="en", dest="ta").text
            tts = gTTS(text=translated_text, lang="ta")
            tts.save(translated_audio_file)
            print(f"Translated audio saved to {translated_audio_file}")

            return {
                "english_text": text,
                "translated_audio_file": translated_audio_file,
            }
    except sr.UnknownValueError:
        return {"error": "Google Web Speech API could not understand the audio"}
    except sr.RequestError as e:
        return {"error": f"Could not request results from Google Web Speech API; {e}"}
