import torch
from diffusers import StableDiffusionInpaintPipeline
from PIL import Image
import pickle

# Load the model
pipe = StableDiffusionInpaintPipeline.from_pretrained(
    "runwayml/stable-diffusion-inpainting"#,
    # revision="fp16", #darsh custom
    # torch_dtype=torch.float16 #darsh custom
)
pipe.safety_checker = lambda images, **kwargs: (images, False) # disable the safety checker
# pipe.to("cuda:0")
pipe.to("cpu") #darsh custom

# Load and resize image and mask
image = "pics/iphone_story.png"
mask = "masks/iphone_story_mask.png"

image = Image.open(image)
mask = Image.open(mask) # white = inpaint, black = ignore
assert(image.size == mask.size)
orig_size = image.size
image = image.resize((512, 512))
mask = mask.resize((512, 512)).convert('L')

# Perform image cleaning
clean = pipe(prompt="", image=image, mask_image=mask).images[0] # use AI to inpaint mask
clean = Image.composite(clean, image, mask) # splice the inpainted area onto original image
clean = clean.resize(orig_size)
clean.save("outputs/iphone_story_bad1.png")