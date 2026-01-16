from fastapi import FastAPI, UploadFile, Response, File, Form
from pydantic import BaseModel
import numpy as np
import cv2
import tensorflow as tf
from solver import process_image, find_letter_coordinates, identify_letter_grid, strike_words
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # im allowin all origins for now
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Total-Contours-Before-Denoising", "Total-Letters"] #log purposes
)

model = tf.keras.models.load_model("font_identifier.keras")

@app.post("/solver")
async def solve(file: UploadFile = File(...), words: str = Form(""), solver_type: str = Form(...)):
    img_bytes = await file.read()
    np_arr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    if img is None:
        return Response(
            content="Invalid or unsupported image file",
            status_code=400
        )

    word_list = words.split(',')

    processed_image, contour_extraction_image = process_image(img)
    letter_coordinates, total_contours, total_letters = find_letter_coordinates(contour_extraction_image)
    letter_grid = identify_letter_grid(model, processed_image, letter_coordinates)
    for row in letter_grid:
        for ltr in row:
            print(ltr, end=" ")
        print("")
    output = strike_words(img, letter_grid, letter_coordinates, solver_type, word_list)

    _, buffer = cv2.imencode(".png", output)
    png_bytes = buffer.tobytes()

    # log purposes
    headers = {"Total-Contours-Before-Denoising": str(total_contours), "Total-Letters": str(total_letters)}

    return Response(content=png_bytes, media_type="image/png", headers=headers)