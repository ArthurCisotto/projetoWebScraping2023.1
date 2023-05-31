import logging
from functools import lru_cache
import easyocr
import numpy as np
from fastapi import APIRouter, UploadFile, WebSocket
import fastapi
import os
import cv2
import redis
import json

log = logging.getLogger("uvicorn")
UPLOAD_DIRECTORY = "uploads"

ocr_global = None

router = APIRouter()

@lru_cache()
@router.on_event("startup")
def ocr_reader():
    global ocr_global
    log.info("Loading easyocr reader")
    ocr = easyocr.Reader(["en"], gpu=False)
    ocr_global = ocr
    return ocr



redis_client = redis.Redis().from_url('redis://default:FEmCLARrZ8JFbECLpEMA@containers-us-west-5.railway.app:6103')

def recognize(reader: easyocr.Reader, image: np.ndarray) -> int:
    img = cv2.imread(image)

    # img = cv2.resize(img, (0, 0), fx=0.3, fy=0.3)

    WIDTH = img.shape[1]
    HEIGHT = img.shape[0]

    # img_cropped = img[int(HEIGHT/2-200):int(HEIGHT/2+200),
    #                   int(WIDTH/2-200):int(WIDTH/2+200)]
    img_gray_cropped = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img_thresh = cv2.threshold(
        img_gray_cropped, 250, 255, cv2.THRESH_BINARY)

    mask = img_thresh.copy()
    mask = cv2.blur(mask, (5, 5))

    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE,
                            np.ones((4, 4), np.uint8))

    mask = cv2.bitwise_not(mask)

    # Save mask
    cv2.imwrite("mask.jpg", mask)

    text = reader.readtext(mask, detail=0)
    text = text[0].replace(" ", "")

    return int(text)




@router.get("/")
async def get_number():
    return {"number": redis_client.get("Number")}

@router.post("/upload")
async def upload_file(file: UploadFile = fastapi.File(...)):
    create_upload_directory()

    file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
    with open(file_location, "wb") as f:
        contents = await file.read()
        f.write(contents)

    number = recognize(ocr_global, file_location)
    delete_image(file.filename)

    redis_client.set("Number", number)

    return {"filename": file.filename, "number": number}

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        last_number = redis_client.get("Number")
        await websocket.send_text(str(last_number))




def create_upload_directory():
    if not os.path.exists(UPLOAD_DIRECTORY):
        os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

def delete_image(file_name):
    file_location = os.path.join(UPLOAD_DIRECTORY, file_name)
    os.remove(file_location)
