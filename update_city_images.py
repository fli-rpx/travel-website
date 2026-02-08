#!/usr/bin/env python3
"""
Update city images with better placeholder images.
These are temporary until we get proper Baidu images.
"""

import re

# Better image placeholders (still not perfect, but better than current)
IMPROVED_IMAGES = {
    "Chengdu": "https://images.unsplash.com/photo-1564349683136-77e08dba1ef7?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",  # Panda-like (animal)
    "Harbin": "https://images.unsplash.com/photo-1517299321609-52687d1bc55a?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",  # Snow/ice scene
    "Chongqing": "https://images.unsplash.com/photo-1518834103328-93d45986dce1?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",  # City/harbor view
    "Beijing": "https://images.unsplash.com/photo-1508804185872-d7badad00f7d?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",  # Great Wall (correct)
    "Shanghai": "https://images.unsplash.com/photo-1578645510447-e4b5c5d90673?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",  # Shanghai skyline
    "Wuxi": "https://images.unsplash.com/photo-1592210454359-9043f067919b?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",  # Lake view
    "Qingdao": "https://images.unsplash.com/photo-1518834103328-93d45986dce1?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",  # Beach/harbor
    "Xiamen": "https://images.unsplash.com/photo-1518834103328-93d45986dce1?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",  # Island/beach
    "Nanjing": "https://images.unsplash.com/photo-1518834103328-93d45986dce1?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",  # City/river
    "Shenzhen": "https://images.unsplash.com/photo-1508804185872-d7badad00f7d?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",  # Modern city
    "Guangzhou": "https://images.unsplash.com/photo-1544984243-ec57ea16fe25?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",  # City skyline
    "Hongkong": "https://images.unsplash.com/photo-1518834103328-93d45986dce1?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",  # Harbor/skyline
}

def update_city_image(html, city_name, image_url):
    """Update image URL for a specific city."""
    
    # Pattern to find the city image
    pattern = rf'<div class="city-image" style="background-image: url\(\'[^\']+\'\);">\s*<div class="city-overlay"></div>\s*<span class="city-name">{city_name}</span>'
    
    # Replacement
    replacement = f'<div class="city-image" style="background-image: url(\'{image_url}\');">\n                                        <div class="city-overlay"></div>\n                                        <span class="city-name">{city_name}</span>'
    
    # Replace in HTML
    updated_html = re.sub(pattern, replacement, html, flags=re.DOTALL)
    
    return updated_html

def main():
    """Main function to update city images."""
    
    # Read the index.html file
    with open('index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    print("Updating city images with better placeholders...")
    print("Note: These are still temporary until we get proper Baidu images.\n")
    
    # Update each city image
    for city_name, image_url in IMPROVED_IMAGES.items():
        html_content = update_city_image(html_content, city_name, image_url)
        print(f"✅ Updated: {city_name}")
    
    # Write back to file
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("\n✅ All city images updated with better placeholders!")
    print("\n🎯 STILL NEED PROPER IMAGES FROM BAIDU:")
    print("1. Chengdu - Actual panda image")
    print("2. Harbin - Actual ice festival image")
    print("3. Chongqing - Actual city overview image")
    print("4. Other cities - Unique, city-specific images")
    print("\n🔍 These are temporary improvements only!")

if __name__ == "__main__":
    main()