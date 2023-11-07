from PIL import Image

# Load and resize image and mask
image = Image.open("back-end/Inpainting/pics/backpack.png")
mask = Image.open("back-end/Inpainting/masks/paint_and_crop_mask_test.png")

# Crop out top red area
width, height = mask.size
for y in range(height):
    # Get the color of the current pixel
    r, g, b, _ = mask.getpixel((0, y))
    if not (r > 200 and g < 100 and b < 100): # left pixel is red
        break
    r, g, b, _ = mask.getpixel((width//2, y))
    if not (r > 200 and g < 100 and b < 100): # middle pixel is red
        break
    r, g, b, _ = mask.getpixel((width-1, y))
    if not (r > 200 and g < 100 and b < 100): # right pixel is red
        break
if y > 0:
    image = image.crop((0, y, width, height))
    mask = mask.crop((0, y, width, height))
# Crop out bottom red area:
width, height = mask.size
for y in reversed(range(height)):
    # Get the color of the current pixel
    r, g, b, _ = mask.getpixel((0, y))
    if not (r > 200 and g < 100 and b < 100): # left pixel is red
        break
    r, g, b, _ = mask.getpixel((width//2, y))
    if not (r > 200 and g < 100 and b < 100): # middle pixel is red
        break
    r, g, b, _ = mask.getpixel((width-1, y))
    if not (r > 200 and g < 100 and b < 100): # right pixel is red
        break
if y < height-1:
    image = image.crop((0, 0, width, y+1))
    mask = mask.crop((0, 0, width, y+1))

image.save('backpack_test.png')
mask.save('backpack_mask_test.png')
