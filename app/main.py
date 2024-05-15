import os
from fastapi import FastAPI, File, UploadFile
from googletrans import Translator
from gtts import gTTS
import speech_recognition as sr
from googletrans import Translator
import pyttsx3
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse
from starlette.requests import Request
from pydantic import BaseModel

app = FastAPI()

app.mount("/templates", StaticFiles(directory="templates"), name="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
@app.get("/")
async def read_index():
    try:
        # Serve the speechconverter.html file from the templates directory
        return FileResponse("templates/speechconverter.html", media_type="text/html")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    # Path to your HTML file
    
@app.get('/speech-converter')
async def speech_converter(request: Request):
    html_file_path = os.path.join("templates", "index.html")
    with open(html_file_path, "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)

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


# @app.post("/translate")
async def translate_audio(filename):
    try:
        # Define the recognizer
        recognizer = sr.Recognizer()

        # Use the recognizer to open the audio file
        with sr.AudioFile("uploaded_files/"+filename) as source:
            # Listen for the data (load audio to memory)
            audio_data = recognizer.record(source)

            # Use Google Web Speech API to recognize the audio
            text = recognizer.recognize_google(audio_data)
            print("Text: ", text)
            # tamil_text = translate_to_tamil(text)
            # print("English: ", text)
            # print("Tamil: ", tamil_text)
            translated_audio_file = os.path.join("static", "translated_audio.mp3")
            # Generate translated audio
            # translated_audio_file = "/static/translated_audio.mp3"
            translator = Translator()
           
            translated_text = translator.translate(text, src="en", dest="ta").text
            print(f"Translated text: {translated_text}")
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
    
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    upload_folder = "uploaded_files"
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    with open(os.path.join(upload_folder, file.filename), "wb") as buffer:
        buffer.write(await file.read())
    transcription = await translate_audio(file.filename)
    return {"filename": file.filename, "transcription": transcription}

class SpeechInput(BaseModel):
    speech_text: str
r = sr.Recognizer()
translator_new = Translator()
def translate_long_text(text):
    print("text",text)
    
    print("Length of text:", len(text))
    # Split the text into smaller chunks (e.g., 100 characters per chunk)
    chunk_size = 3000
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    print("chunks",chunks)
    translated_chunks = []
    for chunk in chunks:
        translated_chunk = translator_new.translate(chunk, dest='ta').text
        translated_chunks.append(translated_chunk)
    
    return translated_chunks
@app.post('/process_speech')
async def process_speech(data: SpeechInput):
    try:
        speech_text = data.speech_text
        print("speech_text",speech_text)
        # Translate long text
        translated_chunks = translate_long_text(speech_text)
        print("translated_chunks",translated_chunks)
        if translated_chunks:
            # Return the translated chunks as JSON
            return {'translated_chunks': translated_chunks}
        else:
            return {'translated_chunks': ['']}  # Return an empty chunk as a fallback

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
