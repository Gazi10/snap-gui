import torch
import os
from torchvision import datasets, transforms
from PIL import ImageDraw, Image
import matplotlib.pyplot as plt
import numpy as np
import random


folder_path = r"back-end\ImageGenerator\SelfiesDataset"
images_path = r"back-end\ImageGenerator\SnapsDataset\images"
annots_path = r"back-end\ImageGenerator\SnapsDataset\annotations"

tot = 0
for filename in os.listdir(folder_path):
    if tot >= 2000:
        break
    # Load the image
    img = Image.open(os.path.join(folder_path, filename))

    # crop image to make it vertical
    img = img.crop((img.width // 8, 0, img.width - img.width // 8, img.height))

    # add SendAChatBar to the bottom of image
    send_a_chat_bar = Image.open(r"back-end\ImageGenerator\SnapChatGUI\SendAChatBar.png")
    send_a_chat_bar = send_a_chat_bar.resize((img.width, send_a_chat_bar.height * img.width // send_a_chat_bar.width))
    new_img = Image.new('RGBA', (img.width, img.height + send_a_chat_bar.height)) 
    new_img.paste(img, (0, 0))
    new_img.paste(send_a_chat_bar, (0, img.height))
    img = new_img

    # add three white dots to top right
    three_dots = Image.open(r"back-end\ImageGenerator\SnapChatGUI\ThreeDots.png")
    three_dots = three_dots.resize((int(three_dots.width / 3.5), int(three_dots.height / 3.5)))
    three_dots_indent = 5
    img.paste(three_dots, (img.width - three_dots.width - three_dots_indent, three_dots_indent), mask = three_dots.convert("RGBA"))

    # overlay transparent black box on image
    TINT_COLOR = (0, 0, 0)  # Black
    TRANSPARENCY = .45  # Degree of transparency, 0-100%
    OPACITY = int(255 * TRANSPARENCY)
    overlay = Image.new('RGBA', img.size, TINT_COLOR+(0,))
    draw = ImageDraw.Draw(overlay)  # Create a context for drawing things on it.
    text_box_loc = random.randint(40, img.height - send_a_chat_bar.height - 40)
    text_box_height = 20
    draw.rectangle(((0, text_box_loc), (img.width, text_box_loc + text_box_height)), fill=TINT_COLOR+(OPACITY,))
    img = Image.alpha_composite(img, overlay)

    # save image
    img_name = os.path.splitext(filename)[0] + '.png'
    img_path = os.path.join(images_path, img_name)
    img.save(img_path, 'PNG')

    # save annotations
    annot_name = os.path.splitext(filename)[0] + '.txt'
    annot_path = os.path.join(annots_path, annot_name)

    with open(annot_path, 'w') as f:
        # 0 = GUI bar
        x_center = 0.5
        y_center = (img.height - send_a_chat_bar.height / 2) / img.height
        width = 1
        height = send_a_chat_bar.height / img.height
        f.write(f"0 {x_center} {y_center} {width} {height}\n")

        # 1 = three dots
        x_center = (img.width - three_dots_indent - three_dots.width / 2) / img.width
        y_center = (three_dots_indent + three_dots.height / 2) / img.height
        width = three_dots.width / img.width
        height = three_dots.height / img.height
        f.write(f"1 {x_center} {y_center} {width} {height}\n")

        # 2 = text bar
        x_center = 0.5
        y_center = (text_box_loc + text_box_height / 2) / img.height
        width = 1
        height = text_box_height / img.height
        f.write(f"2 {x_center} {y_center} {width} {height}\n")

    tot += 1