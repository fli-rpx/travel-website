#!/usr/bin/env python3
"""
Update city page images to match the main page.
"""

import os

# Same images as used in main page (from update_city_images_v2.py)
CITY_IMAGES = {
    "beijing": "https://images.unsplash.com/photo-1508804185872-d7badad00f7d?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80",
    "shanghai": "https://images.unsplash.com/photo-1578645510447-e4b5c5d90673?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80",
    "chengdu": "https://images.unsplash.com/photo-1564349683136-77e08dba1ef7?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80",
    "harbin": "https://images.unsplash.com/photo-1517299321609-52687d1bc55a?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80",
    "chongqing": "https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80",
    # Add other cities when their pages are created
    "wuxi": "https://images.unsplash.com/photo-1592210454359-9043f067919b?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80",
    "qingdao": "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80",
    "xiamen": "https://images.unsplash.com/photo-1528164344705-47542687000d?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80",
    "nanjing": "https://images.unsplash.com/photo-1599576838688-8a6c1137febb?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80",
    "shenzhen": "https://images.unsplash.com/photo-1518834103328-93d45986dce1?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80",
    "guangzhou": "https://images.unsplash.com/photo-1591261730799-ee4e6c2d16d7?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80",
    "hongkong": "https://images.unsplash.com/photo-1544984243-ec57ea16fe25?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80",
}

def update_city_page(city_file, image_url):
    """Update image in city page."""
    
    with open(city_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update hero image
    content = content.replace("--hero-image: url('CITY_IMAGE_URL')", f"--hero-image: url('{image_url}')")
    
    # Update gallery images (use same image for all three for now)
    content = content.replace("GALLERY_IMAGE_1", image_url)
    content = content.replace("GALLERY_IMAGE_2", image_url)
    content = content.replace("GALLERY_IMAGE_3", image_url)
    
    with open(city_file, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    """Update all city page images."""
    
    print("Updating city page images to match main page...")
    
    for city_id, image_url in CITY_IMAGES.items():
        city_file = f"cities/{city_id}.html"
        if os.path.exists(city_file):
            update_city_page(city_file, image_url)
            print(f"✅ Updated: {city_file}")
        else:
            print(f"⚠️  Not found: {city_file}")
    
    print("\n✅ City page images updated!")
    print("\n🎯 Remember: These are temporary images.")
    print("We still need proper Baidu images for:")
    print("1. Chengdu panda")
    print("2. Harbin ice festival")
    print("3. Chongqing city view")

if __name__ == "__main__":
    main()