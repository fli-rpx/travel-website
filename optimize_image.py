#!/usr/bin/env python3
"""
Image optimization script for travel website
Optimizes JPEG images while maintaining good quality
"""

import os
from PIL import Image
import sys

def optimize_jpeg(image_path, quality=85, progressive=True):
    """
    Optimize a JPEG image by reducing quality and using progressive encoding
    
    Args:
        image_path: Path to the image file
        quality: JPEG quality (1-100, default 85)
        progressive: Use progressive encoding (default True)
    
    Returns:
        tuple: (original_size, optimized_size, savings_percent)
    """
    if not os.path.exists(image_path):
        print(f"Error: File not found - {image_path}")
        return None
    
    # Get original file size
    original_size = os.path.getsize(image_path)
    
    # Open and optimize the image
    try:
        with Image.open(image_path) as img:
            # Convert to RGB if necessary (for PNG with transparency)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Create a temporary output path
            temp_path = image_path + '.optimized'
            
            # Save with optimization
            img.save(
                temp_path,
                'JPEG',
                quality=quality,
                optimize=True,
                progressive=progressive
            )
            
            # Get optimized size
            optimized_size = os.path.getsize(temp_path)
            
            # Calculate savings
            savings = original_size - optimized_size
            savings_percent = (savings / original_size) * 100 if original_size > 0 else 0
            
            # Replace original with optimized if it's smaller
            if optimized_size < original_size:
                os.replace(temp_path, image_path)
                print(f"✓ Optimized: {os.path.basename(image_path)}")
                print(f"  Original: {original_size:,} bytes")
                print(f"  Optimized: {optimized_size:,} bytes")
                print(f"  Savings: {savings:,} bytes ({savings_percent:.1f}%)")
                return (original_size, optimized_size, savings_percent)
            else:
                # Delete temp file, keep original
                os.remove(temp_path)
                print(f"✓ Already optimized: {os.path.basename(image_path)}")
                print(f"  Size: {original_size:,} bytes (no improvement)")
                return (original_size, original_size, 0)
                
    except Exception as e:
        print(f"Error optimizing {image_path}: {e}")
        # Clean up temp file if it exists
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 optimize_image.py <image_path> [quality]")
        print("Example: python3 optimize_image.py images/user_photos/kaifeng_1.jpg 85")
        sys.exit(1)
    
    image_path = sys.argv[1]
    quality = int(sys.argv[2]) if len(sys.argv) > 2 else 85
    
    result = optimize_jpeg(image_path, quality)
    
    if result:
        original_size, optimized_size, savings_percent = result
        if savings_percent > 0:
            print(f"\n✅ Optimization successful!")
        else:
            print(f"\nℹ️ Image was already well optimized")
    else:
        print(f"\n❌ Optimization failed")

if __name__ == "__main__":
    main()