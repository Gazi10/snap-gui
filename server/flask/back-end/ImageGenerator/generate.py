from PIL import Image, ImageDraw, ImageFont

# create empty image
img = Image.open(r"back-end\ImageGenerator\SelfiesDataset\00a454da495e11e28a7322000a1fa414_6.jpg").convert('RGBA')

# crop image to make it vertical
img = img.crop((img.width // 8, 0, img.width - img.width // 8, img.height))

# add SendAChatBar to the bottom of image
send_a_chat_bar = Image.open(r"back-end\ImageGenerator\SnapChatGUI\SendAChatBar.png")
send_a_chat_bar = send_a_chat_bar.resize((img.width, send_a_chat_bar.height * img.width // send_a_chat_bar.width))
new_img = Image.new('RGBA', (img.width, img.height + send_a_chat_bar.height)) 
new_img.paste(img, (0, 0))
new_img.paste(send_a_chat_bar, (0, img.height))
img = new_img
# img.show()

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
draw.rectangle(((0, 200), (img.width, 220)), fill=TINT_COLOR+(OPACITY,))

img = Image.alpha_composite(img, overlay)

img.show()
