import torch
import os
from torchvision import datasets, transforms
from PIL import ImageDraw, Image
import matplotlib.pyplot as plt
import numpy as np


class CustomDataset(torch.utils.data.Dataset):
    def __init__(self, root_dir, transform=None):
        self.root_dir = root_dir
        self.transform = transform
        self.image_filenames = os.listdir(root_dir)
        
    def __len__(self):
        return len(self.image_filenames)
    
    def __getitem__(self, index):
        # Load the image
        img = Image.open(os.path.join(self.root_dir, self.image_filenames[index]))
        
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
        img.paste(three_dots, (img.width - three_dots.width - 5, 5), mask = three_dots.convert("RGBA"))

        # overlay transparent black box on image
        TINT_COLOR = (0, 0, 0)  # Black
        TRANSPARENCY = .45  # Degree of transparency, 0-100%
        OPACITY = int(255 * TRANSPARENCY)
        overlay = Image.new('RGBA', img.size, TINT_COLOR+(0,))
        draw = ImageDraw.Draw(overlay)  # Create a context for drawing things on it.

        draw.rectangle(((0, 200), (img.width, 220)), fill=TINT_COLOR+(OPACITY,)) # TODO: randomize location

        img = Image.alpha_composite(img, overlay)
        # img.show()

        # Apply any additional transforms
        if self.transform:
            img = self.transform(img)
        
        return img, self.image_filenames[index]


# Set up transforms
transform = transforms.Compose([
    transforms.Resize((7*32, 12*32)),  # Resize dimensions to multiple of 32 for YOLO
    transforms.ToTensor()  # Convert image to tensor
])

# Load the custom dataset
dataset = CustomDataset(r"back-end\ImageGenerator\SelfiesDataset", transform=transform)
print(len(dataset))

# Create a dataloader
dataloader = torch.utils.data.DataLoader(dataset, batch_size=32, shuffle=True)

for batch in dataloader:
    image, filename = batch[0][0], batch[1][0]
    # Convert the image from a PyTorch tensor to a numpy array
    image = np.transpose(image.numpy(), (1, 2, 0))

    # Display the image
    print(filename)
    plt.imshow(image)
    plt.title(filename)
    plt.show()