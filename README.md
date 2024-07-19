# ASCII Art Generator

This project converts an image into ASCII art. It calculates the luminance of each pixel in a downscaled version of the image and replaces it with the corresponding character from a given character set.

## Requirements

- Python 3.x
- [Pillow library](https://pypi.org/project/pillow/) (`PIL`)

```bash
pip install pillow
```

## Usage

Run the script:

```bash
python ascii_art_generator.py
```

Provide the path to the image you want to convert when prompted by the program.

```bash
Enter the path to the image:
path/to/your/image.jpg
```

### Important Notes:

1. **Font File**: Ensure that the [lucon.ttf](https://legionfonts.com/fonts/lucon) is available on your machine, or change the `font_path` variable to point to a valid font file path.
2. **Scale Factor**: The image's is set to `1/8` but it can be changed to literally anything. In the showcase I used power of 2s,
   
#### In Progress:
- edge detection
- more luminous images