#!/usr/bin/env python3
"""
Create placeholder images for Xiamen travel page
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_gradient_image(width, height, color1, color2, text, filename):
    """Create a gradient background image with text"""
    # Create gradient
    image = Image.new('RGB', (width, height), color1)
    draw = ImageDraw.Draw(image)
    
    # Simple gradient effect
    for i in range(height):
        ratio = i / height
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        draw.line([(0, i), (width, i)], fill=(r, g, b))
    
    # Add text
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 48)
    except:
        font = ImageFont.load_default()
    
    # Calculate text position
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    
    # Draw text with shadow
    draw.text((x+2, y+2), text, font=font, fill=(0, 0, 0, 128))
    draw.text((x, y), text, font=font, fill=(255, 255, 255))
    
    # Save image
    image.save(filename)
    print(f"Created: {filename}")

def main():
    # Create images directory if it doesn't exist
    os.makedirs("images/user_photos", exist_ok=True)
    
    # Image 1: Gulangyu Island (blue theme)
    create_gradient_image(
        800, 600,
        (30, 60, 120),  # Dark blue
        (100, 180, 255),  # Light blue
        "Gulangyu Island\nXiamen",
        "images/user_photos/xiamen-1.jpg"
    )
    
    # Image 2: Xiamen University (green theme)
    create_gradient_image(
        800, 600,
        (20, 80, 40),  # Dark green
        (120, 220, 140),  # Light green
        "Xiamen University\nChina's Most Beautiful Campus",
        "images/user_photos/xiamen-2.jpg"
    )
    
    # Image 3: Coastal Xiamen (orange/beach theme)
    create_gradient_image(
        800, 600,
        (180, 100, 30),  # Dark orange
        (255, 220, 160),  # Light sand color
        "Coastal Xiamen\nGarden on the Sea",
        "images/user_photos/xiamen-3.jpg"
    )
    
    print("\n✅ Created 3 placeholder images for Xiamen travel page")
    print("📍 Location: images/user_photos/xiamen-1.jpg, xiamen-2.jpg, xiamen-3.jpg")

if __name__ == "__main__":
    main()