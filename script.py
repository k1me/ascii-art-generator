import math, time, cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


def get_luminance(img, case=False):
    pixels = np.array(img)
    luminance = (
        pixels[:, :, 0] * 0.299 + pixels[:, :, 1] * 0.587 + pixels[:, :, 2] * 0.114
    )
    return np.max(luminance) if case else luminance


def get_char(luminance, interval, chars):
    index = (math.floor(luminance * interval)) % len(chars)
    return chars[index]


def detect_edges(img):
    grayscale = cv2.cvtColor(np.array(img), cv2.COLOR_RGBA2GRAY)
    img_gx = cv2.Sobel(
        grayscale, cv2.CV_32FC1, 1, 0, ksize=5, borderType=cv2.BORDER_DEFAULT
    )
    img_gy = cv2.Sobel(
        grayscale, cv2.CV_32FC1, 0, 1, ksize=5, borderType=cv2.BORDER_DEFAULT
    )
    img_grad_magnitude = cv2.magnitude(img_gx, img_gy)
    normalized = cv2.normalize(
        img_grad_magnitude, None, 0, 255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1
    )
    threshold = 50
    _, img_thresholded = cv2.threshold(normalized, threshold, 255, cv2.THRESH_BINARY)
    return img_thresholded, img_gx, img_gy


def compute_angles(img, gx, gy):
    angles = np.full_like(img, fill_value=None, dtype=object)
    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            if img[y, x] >= 0:
                angle_rad = math.atan2(gx[y, x], gy[y, x])
                angle_deg = int(math.degrees(angle_rad))
                angles[y, x] = angle_deg
    return angles


def get_edge_char(angle):
    if (75 < angle < 105) or (-95 < angle < -85):
        return "|"
    if (-15 < angle < 15) or (angle > 165) or (angle < -165):
        return "—"
    if (-15 <= angle < 75) or (-165 < angle < -95):
        return "/"
    return "\\"


def main():
    chars = " .;coPO?@■"
    char_list = list(chars)
    char_width = 8
    char_height = 12
    scale_factor = 1 / 4
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
    edges, img_gx, img_gy = detect_edges(img)
    angles = compute_angles(edges, img_gx, img_gy)

    for y in range(pixels.shape[0]):
        for x in range(pixels.shape[1]):
            if edges[y, x] > 0:
                char = get_edge_char(angles[y, x])
            else:
                lum = luminance[y, x]
                char = get_char(lum, interval, char_list)
            r, g, b = pixels[y, x]
            draw.text((x * char_width, y * char_height), char, font=fnt, fill=(r, g, b))

    output_img.save("output.png")
    print(f"ASCII art image saved as {output_image_path}")


if __name__ == "__main__":
    main()
