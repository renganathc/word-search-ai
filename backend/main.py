from fastapi import FastAPI, UploadFile, Response, File, Form
from pydantic import BaseModel
import numpy as np
import cv2
import tensorflow as tf
from solver import process_image, find_letter_coordinates, identify_letter_grid, strike_words

app = FastAPI()

@app.post("/solver")
async def solve(file: UploadFile = File(...), words: str = Form(...)):
    img_bytes = await file.read()
    np_arr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    model = tf.keras.models.load_model("font_identifier.keras")
    word_list = words.split(',')

    processed_image = process_image(img)
    letter_coordinates = find_letter_coordinates(processed_image)
    letter_grid = identify_letter_grid(model, processed_image, letter_coordinates)
    output = strike_words(img, word_list, letter_grid, letter_coordinates)

    # cv2.imshow("debu g", output)
    # cv2.waitKey(20)

    _, buffer = cv2.imencode(".png", output)
    png_bytes = buffer.tobytes()

    return Response(content=png_bytes, media_type="image/png")