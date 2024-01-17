import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import os

def random_brown_shade():
    """ Generate a random brown shade """
    return (random.randint(100, 200), random.randint(42, 100), random.randint(0, 60))

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


def random_light_color():
    """ Generate a random light color """
    colors = [(random.randint(150, 255), random.randint(85, 160), random.randint(0, 60)),  # Light brown
              (255, 0, 0),  # Red
              (255, 255, 0),  # Yellow
              (255, 165, 0),  # Orange
              (255, 255, 255),  # White
              (0, 0, 0)]  # Black
    return random.choice(colors)

def add_blur(image, probability=0.2):
    """ Add blur to the image with a certain probability """
    if random.random() < probability:
        return image.filter(ImageFilter.GaussianBlur(radius=random.randint(1, 3)))
    return image

def adjust_brightness(image, min_factor=0.5, max_factor=1.5):
    """ Randomly adjust the brightness of the image """
    enhancer = ImageEnhance.Brightness(image)
    factor = random.uniform(min_factor, max_factor)
    return enhancer.enhance(factor)

def add_shadow(draw, text, position, font, shadow_color, offset=(2, 2)):
    """ Add shadow to the text """
    x, y = position
    shadow_position = (x + offset[0], y + offset[1])
    draw.text(shadow_position, text, font=font, fill=shadow_color)

def create_random_image(font_path, text, image_size, font_size, gap, output_folder, image_index):
    """ Create a single image with various effects """
    background_color = random_brown_shade()
    text_color = random_light_color()

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

        # Add shadow
        add_shadow(draw, char, (text_x, text_y), font, shadow_color="grey")

        # Draw the text
        draw.text((text_x, text_y), char, fill=text_color, font=font)

    # Add blur and adjust brightness
    image = add_blur(image)
    image = adjust_brightness(image)

    # Save the image
    image.save(f'{output_folder}/image_{image_index}.png')

# Parameters
font_path = 'lemueria.ttf'  # Path to the font file
text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
image_size = (1200, 600)
font_size = 40
gap = 10
output_folder = 'output_sample'  # Output folder

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Generate 100 images
for i in range(400):
    create_random_image(font_path, text, image_size, font_size, gap, output_folder, i)
