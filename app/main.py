from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    with open(f"uploaded_files/{file.filename}", "wb") as buffer:
        buffer.write(await file.read())
    return {"filename": file.filename}
