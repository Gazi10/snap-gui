from PIL import Image


image = Image.open("iphone_story_output.png")
image.resize((1169, 2032)).save("iphone_story_output2.png")
