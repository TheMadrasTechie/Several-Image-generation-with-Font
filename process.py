import random
from PIL import Image, ImageDraw, ImageFont

def is_overlapping(new_position, existing_positions, text_size, gap):
    new_x, new_y = new_position
    new_width, new_height = text_size

    for pos, size in existing_positions:
        ex_x, ex_y = pos
        ex_width, ex_height = size

        if not (new_x + new_width + gap < ex_x or new_x > ex_x + ex_width + gap or
                new_y + new_height + gap < ex_y or new_y > ex_y + ex_height + gap):
            return True
    return False

def create_image_with_random_alphabets(font_path, text, image_size, background_color, text_color, font_size, gap, output_path):
    # Load the custom font
    font = ImageFont.truetype(font_path, font_size)

    # Create an image with the specified background color
    image = Image.new("RGB", image_size, background_color)

    # Initialize the drawing context
    draw = ImageDraw.Draw(image)

    existing_positions = []
    for char in text:
        while True:
            # Generate a random position for each character
            text_width, text_height = draw.textsize(char, font=font)
            text_x = random.randint(0, image_size[0] - text_width)
            text_y = random.randint(0, image_size[1] - text_height)

            # Check if the new position overlaps with existing characters
            if not is_overlapping((text_x, text_y), existing_positions, (text_width, text_height), gap):
                existing_positions.append(((text_x, text_y), (text_width, text_height)))
                break

        # Add text to image
        draw.text((text_x, text_y), char, fill=text_color, font=font)

    # Save the image
    image.save(output_path)

# Parameters
font_path = 'lemueria.ttf'  # Path to the font file
text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
image_size = (1200, 600)  # Adjusted image size for better fit
background_color = "white"
text_color = "black"
font_size = 40
gap = 10  # Minimum gap between characters
output_path = 'output/random_alphabets_image.png'  # Output file path

# Create the image
create_image_with_random_alphabets(font_path, text, image_size, background_color, text_color, font_size, gap, output_path)
