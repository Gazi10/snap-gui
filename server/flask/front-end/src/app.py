from flask import Flask, render_template, request, send_file
from backend import detect_GUI, inpaint, crop_by_mask
from PIL import Image
# from werkzeug.utils import secure_filename
import os
import base64

app = Flask(__name__)


@app.route('/single-clean', methods=['POST'])
def singleClean():
    if request.method == 'POST':
        data = request.get_json()

        img = data["img"]["img"]
        img_name = data["img"]["name"]
        img_name_clean = f"clean_{img_name}"
        mask = data["mask"]["img"]
        mask_name = data["mask"]["name"]

        with open(img_name, "wb") as f:
            f.write(base64.b64decode(img))

        with open(mask_name, "wb") as f:
            f.write(base64.b64decode(mask))

        image = Image.open(img_name)
        mask = Image.open(mask_name)
        mask = mask.resize(image.size)

        clean = inpaint(image, mask)
        clean.save(img_name_clean)

        with open(img_name_clean, "rb") as f:
            data = f.read()
            print(base64.b64encode(data), flush=True)
            return {"success": True, "img": base64.b64encode(data).decode("utf-8"), "name": img_name_clean}

    return {"success": False}


@app.route('/batch-clean', methods=['POST'])
def batchClean():
    if request.method == 'POST':
        data = request.get_json()
        cleaned_imgs = list()

        for file in data:
            with open("tmp", "wb") as f:
                f.write(base64.b64decode(file["img"]))

            image = Image.open("tmp")
            detected, image, mask = detect_GUI(image)

            if detected:
                img_clean_name = f"clean_{file['name']}"

                image, mask = crop_by_mask(image, mask)
                clean = inpaint(image, mask)
                clean.save(img_clean_name)
                image.save(img_clean_name)

                with open(img_clean_name, "rb") as f:
                    data = f.read()
                    cleaned_imgs.append({"img": base64.b64encode(data).decode("utf-8"), "name": img_clean_name})
            else:
                print("No GUI elements detected in",
                      secure_filename(file.filename))

        return {"success": True, "imgs": cleaned_imgs}

    return {"success": False}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
