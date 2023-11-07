from diffusers import StableDiffusionInpaintPipeline
from ultralytics import YOLO
from PIL import Image
import torch
import numpy as np

# Load the YOLO object dection model
model = YOLO("best_s.pt")
#model.to("cuda:0")

# Load the inpainting diffusion model
inpainter = StableDiffusionInpaintPipeline.from_pretrained(
    "runwayml/stable-diffusion-inpainting",
    #revision="fp16",
    #torch_dtype=torch.float16
)
inpainter.safety_checker = lambda images, **kwargs: (images, False) # disable the safety checker
#inpainter.to("cuda:0")
inpainter.to("cpu")

def detect_GUI(image):
    """Identify the GUI elements, crop the original image, and create a mask for removing the elements.
    
    Parameters
    ----------
    image: a PIL image which may or may not contain GUI elements

    Returns
    -------
    GUI_elements: a bool, True if there are GUI elements, false otherwise
    image: the input image, cropped if necessary to remove GUI elements
    mask: a PIL image where white corresponds to GUI element, black to picture
    """
    # hyper-parameters
    THRESHOLD = 0.6 # filter out low confidence predictions
    BLACK, WHITE, RED = (0, 0, 0), (256, 256, 256), (256, 0, 0) # RGB values for masks
    CLASS_TO_CROP = (0, 3) # class of GUI elements to crop from the input image instead of to inpaint
    BB_MARGIN = 4 # bounding box margin
    
    # source can be of various formats, e.g., path, URL, PIL image, numpy images, etc.
        # we use PIL image here
    results = model(source=image)
    # return if there are no detections
    if not results:
        return False, image, image
    
    # There's only one input image, so we access the first and only result
    result = results[0].cpu().boxes.numpy()
    
    # only consider predictions with confidence scores greater than the threshold
    confidence_scores = result.data[:,4]
    idc_to_keep = confidence_scores >= THRESHOLD
    result = result[idc_to_keep]
    
    # note that output cooridnates of the model are floats, we round them to int
    # 0 = GUI, 1 = three dots, 2 = text bar, 3 = top bar
    coordinates = np.int32(result.data[:,0:4])
    classes = result.data[:,-1]
    
    # pad the bounding boxes inpainting is better
    coordinates[:,0] -= BB_MARGIN
    coordinates[:,1] -= BB_MARGIN
    coordinates[:,2] += BB_MARGIN
    coordinates[:,3] += BB_MARGIN
    
    # create the mask
    mask = image.copy()
    mask.paste(BLACK, [0, 0, mask.size[0],mask.size[1]]) # initialize the mask to be all black
    for box, clss in zip(coordinates, classes):
        if clss in CLASS_TO_CROP: # elements to crop
            mask.paste(RED, box)
        else: # elements to inpaint
            mask.paste(WHITE, box)  
            
    return True, image, mask

def inpaint(image, mask):
    """Inpaint areas of the image corresponding to white areas in the mask.
    
    Parameters
    ----------
    image: a PIL image with GUI elements to clean
    mask: a PIL image containing the mask for `image`\]==
    Returns
    -------
    clean: the result of inpainting image using mask
    """
    # Preprocess image and mask
    assert(image.size == mask.size)
    size = image.size
    image = image.resize((512, 512))
    mask = mask.resize((512, 512)).convert('L')

    # Perform image inpainting (forward pass on diffusion model)
    clean = inpainter(prompt="", image=image, mask_image=mask).images[0]
        
    # Postprocess image result
    clean = Image.composite(clean, image, mask) # splice the inpainted area onto original image
    clean = clean.resize(size)
    return clean


def crop_by_mask(image, mask):
    """Crops out red boxes which span the images width"""
    # TODO: cast to JPG (mode = RGB)
    # Crop out top red area
    image = image.convert('RGB')
    mask = mask.convert('RGB')
    width, height = mask.size
    def find_end_of_red(ys):
        for y in ys:
            pixels_to_check = (((0, y)), (width//2, y), (width-1, y))
            for pixel in pixels_to_check:
                r, g, b = mask.getpixel(pixel)
                if not (r > 200 and g < 100 and b < 100):
                    return y
                
    upper = find_end_of_red([y for y in range(height)])
    lower = find_end_of_red([y for y in reversed(range(height))])
    image = image.crop((0, upper, width, lower+1))
    mask = mask.crop((0, upper, width, lower+1))
    return image, mask