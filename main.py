import os
import time
import json
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import FileResponse
import uvicorn

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")

@app.get("/")
def read_root():
    return {"Hello": "FastAPI"}

@app.post("/file/upload")
def upload_file(file: UploadFile):
    if file.content_type != "application/json":
        raise HTTPException(status_code=400, detail="Invalid document type. Please upload a JSON file.")
    
    # Create uploads directory if it doesn't exist
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Generate unique filename based on timestamp
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"{timestamp}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    # Write the JSON data to a Python file
    with open(file_path, "w") as f:
        json_data = json.load(file.file)
        f.write("# Python file converted from JSON\n\n")
        for key, value in json_data.items():
            f.write(f"{key} = {json.dumps(value)}\n")
    
    return {"filename": filename}

@app.post("/file/uploadndownload")
def upload_n_downloadfile(file: UploadFile):
    if file.content_type != "application/json":
        raise HTTPException(status_code=400, detail="Invalid document type. Please upload a JSON file.")
    
    # Create uploads directory if it doesn't exist
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Generate unique filename based on timestamp
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"{timestamp}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    # Write the JSON data to a Python file
    with open(file_path, "w") as f:
        json_data = json.load(file.file)
        f.write("# Python file converted from JSON\n\n")
        for key, value in json_data.items():
            f.write(f"{key} = {json.dumps(value)}\n")

    # Return the uploaded Python file for download
    return FileResponse(path=file_path, filename=filename)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
