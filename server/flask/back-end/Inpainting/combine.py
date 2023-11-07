from PIL import Image
import matplotlib.pyplot as plt
import cv2

orig = Image.open("pics/backpack_crop.png")
orig_size = orig.size
print(orig_size)
orig = orig.resize((512, 512))
mask = Image.open("masks/backpack_crop_mask.png").resize((512, 512)).convert('L')
clean = Image.open("outputs/backpack_clean.png")

res = Image.composite(clean, orig, mask)
res = res.resize((orig_size))
print(orig_size)

plt.imshow(res)
plt.show()