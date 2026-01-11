import cv2
import numpy as np
import tensorflow as tf
from PIL import Image
from crossword_algorithm import find_words
import random

# The preproceesing part of the image was extremely time consuming. I tried out multiple ways to remove watermakrs, creases on the paper,
# etc and get the letters alone clearly visible. After a lot of experimenting i figured out making the block size larger and 
# more importantly sizing it relative to the image dimensions did wonders.



# input_image = cv2.imread("image_samples/word_search_snacks.png")
# word_list = ['A', 'B', 'C', 'POPSICLE', 'AB']
# model = tf.keras.models.load_model("backend/font_identifier.keras")

def process_image(input_image):
    h, w = input_image.shape[:2]
    block_size = int(min(h, w) * 0.8)
    block_size = block_size if block_size % 2 == 1 else block_size + 1
    processed_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
    #processed_image = cv2.GaussianBlur(processed_image, (3,3), 0.15)
    processed_image = cv2.adaptiveThreshold(processed_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, block_size, 55)
    contour_extraction_image = cv2.morphologyEx(processed_image, cv2.MORPH_CLOSE, np.ones((6,6), np.uint8)) # I fill gaps here leading to reliable contour extraction
    return processed_image, contour_extraction_image


def find_letter_coordinates(contour_extraction_image):
    contours, _ = cv2.findContours(contour_extraction_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    total_contours, total_letters = len(contours), len(contours)
    area = 0

    for cnt in contours:
        area += cv2.contourArea(cnt)

    area = area/total_contours
    letter_coordinates = dict()

    for i in range(total_contours):
        if cv2.contourArea(contours[i]) < 0.1*area:
            total_letters -= 1
            continue
        x, y, w, h = cv2.boundingRect(contours[i])
        pushed = False

        for key in letter_coordinates.keys():
            if key[0] <= y + 0.1*h <= key[1] or key[0] <= y + 0.9*h <= key[1]:
                letter_coordinates[key].append((x, y, x + w, y + h))
                pushed = True
                break

        if not pushed:
            letter_coordinates[(y, y+h)] = [(x, y, x + w, y + h)]

    return letter_coordinates, total_contours, total_letters
            
def identify_letter_grid(model, processed_image, letter_coordinates):
    letter_grid = list()
    letter_width = None

    for i in letter_coordinates.keys():
        letter_coordinates[i] = sorted(letter_coordinates[i], key=lambda x: x[0])

    all_images = list()
    row_lengths = list()

    for i in reversed(letter_coordinates.values()):
        row_lengths.append(len(i))
        for j in i:
            x1, y1, x2, y2 = j
            if not letter_width:
                letter_width = y2 - y1
            img = processed_image[y1:y2, x1:x2]
            img = Image.fromarray(img)
            img.thumbnail((18, 18), Image.Resampling.LANCZOS) #lacnzos is a downsizing filter

            pillow_image = Image.new("L", (28, 28), 0)
            pillow_image.paste(img, ((28 - img.size[0]) // 2, (28 - img.size[1]) // 2))

            img = np.array(pillow_image)
            #img = cv2.erode(img, np.ones((2,2), np.uint8))
            img = img.reshape((28,28,1))
            img = img/255.0

            all_images.append(img)

    all_images = np.array(all_images)
    predictions = model.predict(all_images, len(all_images))
    idx = 0

    for length in row_lengths:
        row = []
        for i in range(length):
            row.append(chr(np.argmax(predictions[idx]) + 65))
            idx += 1
        letter_grid.append(row)

    return letter_grid

def strike_words(input_image, word_list, letter_grid, letter_coordinates):
    word_position = find_words(letter_grid, word_list)
    input_image_cpy = input_image.copy()
    letter_height=None

    if len(word_position) == 0:
        return input_image      # no words found

    for x in word_position:
        start_word_pos, end_word_pos = x
        k = list(reversed(letter_coordinates.values()))
        start = k[start_word_pos[0]][start_word_pos[1]]
        end = k[end_word_pos[0]][end_word_pos[1]]
        cl1, cl2 = random.sample(range(50, 170), 2)
        color = (cl1, cl2, min(340 - cl1 - cl1, 170))
        if not letter_height:
            x1, y1, x2, y2 = k[0][0]
            letter_height = y2 - y1

        result = cv2.line(input_image, ((start[0] + start[2]) // 2 - 2, (start[1] + start[3]) // 2 - 2) , ((end[0] + end[2]) // 2 + 2, (end[1] + end[3]) // 2 + 2) , color, letter_height)
        
    alpha = 0.40
    output_image = cv2.addWeighted(result, alpha, input_image_cpy, 1 - alpha, 0)

    return output_image

# processed_image, contour_extraction_image = process_image(input_image)
# cv2.imshow("original", input_image)
# cv2.waitKey(1000)

# letter_coordinates, tc, tl = find_letter_coordinates(contour_extraction_image)
# print("TOTAL CONTOURS WITHOUT DENOISING: ", tc, "\nTOTAL LETTERS: ", tl)
# letter_grid = identify_letter_grid(model, processed_image, letter_coordinates)

# for row in letter_grid:
#     for ltr in row:
#         print(ltr, end=" ")
#     print("")

# output = strike_words(input_image, word_list, letter_grid, letter_coordinates)
# cv2.imshow("thresholded", processed_image)
# cv2.imshow("contour ex", contour_extraction_image)
# cv2.imshow("solved", output)
# cv2.waitKey(0)