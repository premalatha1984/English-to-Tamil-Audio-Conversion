import os
from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    upload_folder = "uploaded_files"
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    with open(os.path.join(upload_folder, file.filename), "wb") as buffer:
        buffer.write(await file.read())
    return {"filename": file.filename}
