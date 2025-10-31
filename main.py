# main.py
from fastapi import FastAPI, Request
from pydantic import BaseModel
import re

app = FastAPI()

class Attachment(BaseModel):
    url: str

class FileRequest(BaseModel):
    attachments: Attachment

@app.post("/file")
async def detect_mime_type(file_request: FileRequest):
    data_uri = file_request.attachments.url

    # Extract the MIME type from the data URI using regex
    match = re.match(r"data:(.*?);base64,", data_uri)
    if match:
        mime_type = match.group(1)
        # Identify the category (image, text, application, etc.)
        if mime_type.startswith("image/"):
            type_detected = "image"
        elif mime_type.startswith("text/"):
            type_detected = "text"
        elif mime_type.startswith("application/"):
            type_detected = "application"
        else:
            type_detected = "unknown"
    else:
        type_detected = "unknown"

    return {"type": type_detected}
