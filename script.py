import math, time
import numpy as np
from PIL import Image, ImageDraw, ImageFont


def get_luminance(img, case=False):
    pixels = np.array(img)
    luminance = (
        pixels[:, :, 0] * 0.299 + pixels[:, :, 1] * 0.587 + pixels[:, :, 2] * 0.114
    )
    return np.max(luminance) if case else luminance


def get_char(luminance, interval, chars):
    index = (math.floor(luminance * interval) - 1) % len(chars)
    return chars[index]


def main():
    chars = " `.-':_,^=;><+rcz?LT)JfIneoZ5Y2SkP6OX0%&@"
    char_list = list(chars)
    char_width = 8
    char_height = 12
    scale_factor = 1 / 8
    font_path = "lucon.ttf"
    output_image_path = "output.png"
    image_path = input("Enter the path to the image:\n")

    try:
        img = Image.open(image_path)
    except FileNotFoundError:
        print("No such file at the given path.")
        return

    try:
        fnt = ImageFont.truetype(font_path, 15)
    except IOError:
        print(f"Font file {font_path} not found")
        return

    width, height = img.size
    img = img.resize(
        (
            int(width * scale_factor),
            int(height * scale_factor * (char_width / char_height)),
        ),
        Image.BOX,
    )

    pixels = np.array(img)
    luminance = get_luminance(img)

    output_img = Image.new(
        "RGB",
        (char_width * pixels.shape[1], char_height * pixels.shape[0]),
        color="black",
    )
    draw = ImageDraw.Draw(output_img)
    interval = len(char_list) / get_luminance(img, case=True)

    for y in range(pixels.shape[0]):
        for x in range(pixels.shape[1]):
            lum = luminance[y, x]
            r, g, b = pixels[y, x]
            char = get_char(lum, interval, chars)
            draw.text((x * char_width, y * char_height), char, font=fnt, fill=(r, g, b))

    output_img.save("output.png")
    print(f"ASCII art image saved as {output_image_path}")


if __name__ == "__main__":
    main()
