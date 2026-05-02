import random
import string
import os
from html2image import Html2Image
from PIL import Image

def generate_unique_filename(length=None):
    if length is None:
        length = random.randint(17, 30)
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choices(characters, k=length))

def generate_image_from_html(file_path, replacements, width=650, height=1250):
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"HTML file does not exist: {file_path}")
    
    with open(file_path, 'r') as html_file:
        html_content = html_file.read()
    
    for placeholder, value in replacements.items():
        html_content = html_content.replace(placeholder, str(value))
    
    hti = Html2Image()
    
    if not isinstance(width, int) or width <= 0:
        raise ValueError("Width must be a positive integer.")
    if not isinstance(height, int) or height <= 0:
        raise ValueError("Height must be a positive integer.")
    
    size = (width, height)
    
    image_filename = f"{generate_unique_filename()}.jpg"
    
    try:
        hti.screenshot(html_str=html_content, save_as=image_filename, size=size)
        
        if os.path.getsize(image_filename) == 0:
            raise Exception(f"Generated image is empty: {image_filename}")
        
        img = Image.open(image_filename)
        img = img.resize(size, Image.LANCZOS)
        img.save(image_filename)
    except Exception as e:
        raise Exception(f"Failed to create image: {str(e)}")
    
    return image_filename
