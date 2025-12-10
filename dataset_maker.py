from PIL import Image, ImageDraw, ImageFont
import os

font_files = os.listdir("datasets/fonts/")
letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

img_size = (28, 28)

labels = list()

k = 1

for i in font_files:
    #if 'italics' in file_name.lower():
        #continue
    for letter in letters:
        
        img = Image.new("L", img_size, 0)

        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("datasets/fonts/" + i, 24)
        except Exception:
            print("Error while using file ", i, " - ", Exception)
            break

        draw.text(((img_size[0])//2, (img_size[1])//2), letter, fill=255, font=font, anchor="mm")

        img.save(f"datasets/font_images/{k}.png")
        labels.append(letter)
        k += 1

with open("datasets/font_labels.txt", "w") as f:
    for label in labels:
        f.write(label + '\n')