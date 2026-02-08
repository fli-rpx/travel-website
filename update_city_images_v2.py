#!/usr/bin/env python3
"""
Update city images with more specific, high-quality images.
Version 2: Better, city-specific images from Unsplash.
"""

import re

# High-quality, city-specific images from Unsplash
# These are carefully selected to represent each city uniquely
CITY_SPECIFIC_IMAGES = {
    # Beijing - Great Wall (iconic)
    "Beijing": "https://images.unsplash.com/photo-1508804185872-d7badad00f7d?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80",
    
    # Shanghai - Modern skyline
    "Shanghai": "https://images.unsplash.com/photo-1578645510447-e4b5c5d90673?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80",
    
    # Chengdu - Pandas (what it's famous for)
    "Chengdu": "https://images.unsplash.com/photo-1564349683136-77e08dba1ef7?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80",
    
    # Harbin - Ice and snow (ice festival)
    "Harbin": "https://images.unsplash.com/photo-1517299321609-52687d1bc55a?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80",
    
    # Chongqing - Mountain city with rivers
    "Chongqing": "https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80",
    
    # Wuxi - Lake and traditional architecture
    "Wuxi": "https://images.unsplash.com/photo-1592210454359-9043f067919b?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80",
    
    # Qingdao - Beach and European architecture
    "Qingdao": "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80",
    
    # Xiamen - Island and coastal beauty
    "Xiamen": "https://images.unsplash.com/photo-1528164344705-47542687000d?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80",
    
    # Nanjing - Historical city with ancient walls
    "Nanjing": "https://images.unsplash.com/photo-1599576838688-8a6c1137febb?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80",
    
    # Shenzhen - Ultra-modern tech city
    "Shenzhen": "https://images.unsplash.com/photo-1518834103328-93d45986dce1?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80",
    
    # Guangzhou - Pearl River and modern towers
    "Guangzhou": "https://images.unsplash.com/photo-1591261730799-ee4e6c2d16d7?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80",
    
    # Hongkong - Iconic harbor skyline (unique)
    "Hongkong": "https://images.unsplash.com/photo-1544984243-ec57ea16fe25?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80",
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
    """Main function to update city images with better, specific images."""
    
    # Read the index.html file
    with open('index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    print("=" * 60)
    print("CITY IMAGE UPGRADE - VERSION 2")
    print("=" * 60)
    print("Updating city images with high-quality, city-specific images...\n")
    
    # Track which cities were updated
    updated_cities = []
    
    # Update each city image
    for city_name, image_url in CITY_SPECIFIC_IMAGES.items():
        # Check if city exists in HTML
        if city_name in html_content:
            html_content = update_city_image(html_content, city_name, image_url)
            updated_cities.append(city_name)
            print(f"✅ Updated: {city_name}")
            print(f"   Image: {image_url[:60]}...")
        else:
            print(f"⚠️  Skipped: {city_name} (not found in index.html)")
    
    # Write back to file
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total cities updated: {len(updated_cities)}")
    print("\nUpdated cities:")
    for city in updated_cities:
        print(f"  • {city}")
    
    print("\n" + "=" * 60)
    print("NEXT STEPS")
    print("=" * 60)
    print("1. Review the updated index.html in browser")
    print("2. Check that all images load properly")
    print("3. Update city pages with matching images:")
    print("   Run: python3 update_city_page_images.py")
    print("\n💡 Note: These are still placeholder images from Unsplash.")
    print("   For production, consider:")
    print("   - Licensing professional photos")
    print("   - Using official tourism board images")
    print("   - Hiring a photographer for original content")

if __name__ == "__main__":
    main()