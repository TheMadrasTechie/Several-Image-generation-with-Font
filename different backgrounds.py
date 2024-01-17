import random
from PIL import Image, ImageDraw, ImageFont
import os

def random_color():
    """ Generate a random color """
    return tuple(random.randint(0, 255) for _ in range(3))

def is_overlapping(new_position, existing_positions, text_size, gap):
    """ Check if the new position overlaps with existing positions """
    new_x, new_y = new_position
    new_width, new_height = text_size

    for pos, size in existing_positions:
        ex_x, ex_y = pos
        ex_width, ex_height = size

        if not (new_x + new_width + gap < ex_x or new_x > ex_x + ex_width + gap or
                new_y + new_height + gap < ex_y or new_y > ex_y + ex_height + gap):
            return True
    return False

def create_random_image(font_path, text, image_size, font_size, gap, output_folder, image_index):
    """ Create a single image with random background and text color """
    background_color = random_color()
    text_color = random_color()

    # Ensure text color is not too similar to background color
    while sum(abs(bc - tc) for bc, tc in zip(background_color, text_color)) < 100:
        text_color = random_color()

    # Load the custom font
    font = ImageFont.truetype(font_path, font_size)

    # Create an image
    image = Image.new("RGB", image_size, background_color)
    draw = ImageDraw.Draw(image)

    existing_positions = []
    for char in text:
        while True:
            text_width, text_height = draw.textsize(char, font=font)
            text_x = random.randint(0, image_size[0] - text_width)
            text_y = random.randint(0, image_size[1] - text_height)

            if not is_overlapping((text_x, text_y), existing_positions, (text_width, text_height), gap):
                existing_positions.append(((text_x, text_y), (text_width, text_height)))
                break

        draw.text((text_x, text_y), char, fill=text_color, font=font)

    # Save the image
    image.save(f'{output_folder}/image_{image_index}.png')

# Parameters
font_path = 'lemueria.ttf'  # Path to the font file
text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
image_size = (1200, 600)
font_size = 40
gap = 10
output_folder = 'output'  # Output folder

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Generate 100 images
for i in range(300):
    create_random_image(font_path, text, image_size, font_size, gap, output_folder, i)
