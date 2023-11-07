import torch
from diffusers import StableDiffusionInpaintPipeline
from PIL import Image


pipe = StableDiffusionInpaintPipeline.from_pretrained(
    "runwayml/stable-diffusion-inpainting",
    revision="fp16",
)
pipe.to("cuda:0")
# prompt = "Face of a yellow cat, high resolution, sitting on a park bench"
#image and mask_image should be PIL images.
#The mask structure is white for inpainting and black for keeping as is
image = Image.open(r"back-end\Inpainting\pics\backpack.PNG").resize((512, 512))
mask_image = Image.open(r"back-end\Inpainting\masks\backpack_mask.png").resize((512, 512))

image = pipe(prompt="", image=image, mask_image=mask_image).images[0]
image.save("./backpack_clean.png")

