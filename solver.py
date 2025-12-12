import cv2
import numpy as np
import tensorflow as tf
from PIL import Image
from crossword_algorithm import find_words
import random

input_image = cv2.imread("image_samples/word_search_snacks.png")
model = tf.keras.models.load_model("font_identifier.keras")

def process_image(input_image):
    processed_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
    processed_image = cv2.adaptiveThreshold(processed_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 33, 25)
    processed_image = cv2.morphologyEx(processed_image, cv2.MORPH_CLOSE, np.ones((3,3), np.uint8))
    return processed_image


def find_letter_coordinates(processed_image):
    contours, _ = cv2.findContours(processed_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    area = 0

    #debug_image = input_image.copy()

    print("contours before filtering: ", len(contours))

    for cnt in contours:
        area += cv2.contourArea(cnt)

    area = area/len(contours)

    letter_coordinates = dict()
    y_top, y_bottom = -1,-1

    c = 0

    for i in range(len(contours)):
        if cv2.contourArea(contours[i]) < 0.1*area:
            continue
        x, y, w, h = cv2.boundingRect(contours[i])

        c += 1

        #cv2.rectangle(debug_image, (x, y), (x+w, y+h), (0, 255, 0), 1)

        pushed = False

        for key in letter_coordinates.keys():
            if y + w//2 in range(key[0], key[1]):
                y_top, y_bottom = y, y+h
                letter_coordinates[key].append((x - int((w)*(0.25)), y - int(h*(0.25)), x + w + int(w*(0.25)), y + h + int(h*(0.25))))
                pushed = True

        if not pushed:
            letter_coordinates[(y, y+w)] = [(x - int(w*(0.25)), y - int(h*(0.25)), x + w + int(w*(0.25)), y + h + int(h*(0.25)))]

    # cv2.imshow("debug", debug_image[:200, :200])
    # cv2.waitKey(0)

    print("contours after filtering: ", c)

    return letter_coordinates
            
def identify_letter_grid(model, processed_image, letter_coordinates):
    letter_grid = list()
    letter_width = None

    for i in letter_coordinates.keys():
        letter_coordinates[i] = sorted(letter_coordinates[i], key=lambda x: x[0])
        #print(letter_coordinates[i])

    all_images = list()

    letters = 0

    for i in reversed(letter_coordinates.values()):
        for j in i:
            letters += 1
            x1, y1, x2, y2 = j
            if not letter_width:
                letter_width = y2 - y1
            img = processed_image[y1:y2, x1:x2]
            img = Image.fromarray(img)
            img.thumbnail((28, 28), Image.Resampling.LANCZOS) #lacnzos is a downsizing filter

            pillow_image = Image.new("L", (28, 28), 0)
            pillow_image.paste(img, ((28 - img.size[0]) // 2, (28 - img.size[1]) // 2))

            img = np.array(pillow_image).reshape((28,28,1))
            img = img/255.0

            all_images.append(img)

    all_images = np.array(all_images)
    predictions = model.predict(all_images, len(all_images))

    letter_grid = list()

    print("LETTERS FOUND: ",letters, "\nLETTERS PREDICTED: ", len(predictions))

    for prediction in predictions:
        letter_grid.append(chr(np.argmax(prediction) + 65))

    letter_grid = np.array(letter_grid)
    print(letter_grid)
    letter_grid = letter_grid.reshape((len(letter_coordinates.values()), len(list(letter_coordinates.values())[0])))
    letter_grid = letter_grid.tolist()

    for row in letter_grid:
        for letter in row:
            print(letter, end=" ")
        print("")

    return letter_grid

def strike_words(input_image, word_list, letter_grid, letter_coordinates):
    word_position = find_words(letter_grid, word_list)
    input_image_cpy = input_image.copy()
    letter_width=None

    for x in word_position:
        start_word_pos, end_word_pos = x
        k = list(reversed(letter_coordinates.values()))
        start = k[start_word_pos[0]][start_word_pos[1]]
        end = k[end_word_pos[0]][end_word_pos[1]]
        color = random.sample(range(30, 200), 3)

        if not letter_width:
            x1, y1, x2, y2 = k[0][0]
            letter_width = y2 - y1

        result = cv2.line(input_image, ((start[0] + start[2]) // 2 - 2, (start[1] + start[3]) // 2 - 2) , ((end[0] + end[2]) // 2 + 2, (end[1] + end[3]) // 2 + 2) , color, letter_width*10//14)
        
    alpha = 0.45
    output_image = cv2.addWeighted(result, alpha, input_image_cpy, 1 - alpha, 0)

    return output_image

word_list = [
    'DRAMA', 'HISTORY', 'NUMBERS', 'SCIENCE', 'ART',
    'ELEMENTARY', 'HOMEWORK', 'PENCIL', 'SOCIALSTUDIES',
    'BACKPACK', 'ENGLISH', 'LANGUAGEARTS', 'PHYSICALEDUCATION',
    'SPELLING', 'BOOKS', 'FRIENDS', 'LEARN', 'READING',
    'STUDENTS', 'CLASSROOM', 'GEOGRAPHY', 'LIBRARY',
    'RECESS', 'SUBJECTS', 'CRAYONS', 'GRADES',
    'MATH', 'SCHOOL', 'TEACHER', 'DESK', 'HEALTH',
    'MUSIC', 'SCISSORS', 'WRITING'
]

processed_image = process_image(input_image)
letter_coordinates = find_letter_coordinates(processed_image)
letter_grid = identify_letter_grid(model, processed_image, letter_coordinates)
#output = strike_words(input_image, word_list, letter_grid, letter_coordinates)
#cv2.imshow("solved", output)
#cv2.waitKey(0)