import math
from PIL import Image, ImageDraw, ImageFont


def get_max_luminance(img):
    max_value = 0
    widht, height = img.size
    pixels = img.load()

    for y in range(height):
        for x in range(widht):
            r, g, b = pixels[x, y]
            luminance = int(r / 3 + g / 3 + b / 3)
            if luminance > max_value:
                max_value = luminance
    return max_value


def get_char(luminance, interval, chars):
    index = (math.floor(luminance * interval) - 1) % len(chars)
    return chars[index]


def calculate_luminance(pixels, width, height):
    luminances = []
    for y in range(height):
        row = []
        for x in range(width):
            r, g, b = pixels[x, y]
            luminance = int(r / 3 + g / 3 + b / 3)
            row.append((luminance, r, g, b))
        luminances.append(row)
    return luminances


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

    width, height = img.size
    pixels = img.load()
    luminances = calculate_luminance(pixels, width, height)

    output_img = Image.new(
        "RGB", (char_width * width, char_height * height), color="black"
    )
    draw = ImageDraw.Draw(output_img)
    interval = len(char_list) / get_max_luminance(img)

    for y in range(height):
        for x in range(width):
            luminance, r, g, b = luminances[y][x]
            char = get_char(luminance, interval, chars)
            draw.text(
                (x * char_width, y * char_height),
                get_char(luminance, interval, chars),
                font=fnt,
                fill=(r, g, b),
            )

    output_img.save("output.png")
    print(f"ASCII art image saved as {output_image_path}")


if __name__ == "__main__":
    main()
