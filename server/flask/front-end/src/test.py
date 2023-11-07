from backend import detect_GUI, inpaint, crop_by_mask
from PIL import Image

image = Image.open("backpack.png")
print("GUI detection")
detected, image, mask = detect_GUI(image)
image.save("test1.png")
mask.save("test2.png")

image, mask = crop_by_mask(image, mask)

print("Inpainting")
clean = inpaint(image, mask)

clean.show()