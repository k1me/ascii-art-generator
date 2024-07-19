from PIL import Image, ImageDraw, ImageFont
import math


def get_max_luminance(img):
    max_value = 0
    w, h = img.size
    pixels = img.load()
    for i in range(h):
        for j in range(w):
            r, g, b = pixels[j, i]
            h = int(r / 3 + g / 3 + b / 3)
            if h > max_value:
                max_value = h
    return max_value


def get_char(num):
    return char_list[((math.floor(num * interval) - 1) % 41)]


chars = " `.-':_,^=;><+rcz?LT)JfIneoZ5Y2SkP6OX0%&@"
char_list = list(chars)
car_len = len(char_list)
path = input("Enter the path to the image:\n")

char_width = 8
char_height = 12
scale_factor = 1 / 8

try:
    img = Image.open(path)
except:
    print("No such file at the given path.")

fnt = ImageFont.truetype("lucon.ttf", 15)

width, height = img.size
img = img.resize(
    (
        int(width * scale_factor),
        int(height * scale_factor * (char_width / char_height)),
    ),
    Image.NEAREST,
)

width, height = img.size
pixels = img.load()
output_img = Image.new("RGB", (char_width * width, char_height * height), color="black")

draw = ImageDraw.Draw(output_img)
interval = car_len / get_max_luminance(img)

for i in range(height):
    for j in range(width):
        r, g, b = pixels[j, i]
        h = int(r / 3 + g / 3 + b / 3)
        pixels[j, i] = (h, h, h)
        draw.text(
            (j * char_width, i * char_height), get_char(h), font=fnt, fill=(r, g, b)
        )

output_img.save("output.png")
