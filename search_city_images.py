#!/usr/bin/env python3
"""
Search for better city-specific images using web search.
This script helps find appropriate images for each Chinese city.
"""

import re
import json

# City-specific search queries for better images
CITY_SEARCH_QUERIES = {
    "Beijing": ["Beijing Great Wall", "Beijing Forbidden City", "Beijing Tiananmen Square", "Beijing Temple of Heaven"],
    "Shanghai": ["Shanghai skyline", "Shanghai Bund", "Shanghai Oriental Pearl Tower", "Shanghai modern architecture"],
    "Chengdu": ["Chengdu pandas", "Chengdu Jinli Street", "Chengdu Giant Panda Breeding Research Base", "Chengdu tea houses"],
    "Harbin": ["Harbin Ice Festival", "Harbin ice sculptures", "Harbin Saint Sophia Cathedral", "Harbin winter"],
    "Chongqing": ["Chongqing cityscape", "Chongqing mountains", "Chongqing Hongya Cave", "Chongqing night view"],
    "Wuxi": ["Wuxi Taihu Lake", "Wuxi Lingshan Grand Buddha", "Wuxi gardens", "Wuxi traditional architecture"],
    "Qingdao": ["Qingdao beaches", "Qingdao Tsingtao Brewery", "Qingdao Zhanqiao Pier", "Qingdao German architecture"],
    "Xiamen": ["Xiamen Gulangyu Island", "Xiamen beaches", "Xiamen University", "Xiamen coastal view"],
    "Nanjing": ["Nanjing Confucius Temple", "Nanjing Sun Yat-sen Mausoleum", "Nanjing city wall", "Nanjing Qinhuai River"],
    "Shenzhen": ["Shenzhen modern skyline", "Shenzhen technology district", "Shenzhen Window of the World", "Shenzhen contemporary architecture"],
    "Guangzhou": ["Guangzhou Canton Tower", "Guangzhou Pearl River", "Guangzhou Chen Clan Ancestral Hall", "Guangzhou modern city"],
    "Hongkong": ["Hong Kong skyline", "Hong Kong Victoria Harbour", "Hong Kong night view", "Hong Kong cityscape"]
}

# Unsplash API endpoint (free, no API key needed for basic search)
UNSPLASH_SEARCH_URL = "https://api.unsplash.com/search/photos"
# Note: For production, you'd need an Unsplash API key. This is for demonstration.

# Alternative: Use a simpler approach with direct image URLs from known sources
CITY_IMAGE_SUGGESTIONS = {
    "Beijing": [
        "https://images.unsplash.com/photo-1508804185872-d7badad00f7d?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80",  # Great Wall
        "https://images.unsplash.com/photo-1599576838688-8a6c1137febb?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80",  # Forbidden City
    ],
    "Shanghai": [
        "https://images.unsplash.com/photo-1578645510447-e4b5c5d90673?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80",  # Skyline
        "https://images.unsplash.com/photo-1544984243-ec57ea16fe25?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80",  # Bund
    ],
    "Chengdu": [
        "https://images.unsplash.com/photo-1564349683136-77e08dba1ef7?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80",  # Panda
        "https://images.unsplash.com/photo-1591261730799-ee4e6c2d16d7?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80",  # Traditional street
    ],
    "Harbin": [
        "https://images.unsplash.com/photo-1517299321609-52687d1bc55a?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80",  # Ice/snow
        "https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80",  # Winter city
    ],
    "Chongqing": [
        "https://images.unsplash.com/photo-1518834103328-93d45986dce1?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80",  # City/harbor
        "https://images.unsplash.com/photo-1544984243-ec57ea16fe25?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80",  # Mountain city
    ]
}

def search_images_for_city(city_name, queries):
    """Search for images for a specific city."""
    print(f"\n🔍 Searching for images: {city_name}")
    print(f"   Search queries: {', '.join(queries[:2])}...")
    
    # For now, return suggested images
    if city_name in CITY_IMAGE_SUGGESTIONS:
        print(f"   Found {len(CITY_IMAGE_SUGGESTIONS[city_name])} suggested images")
        return CITY_IMAGE_SUGGESTIONS[city_name]
    
    return []

def generate_image_report():
    """Generate a report of current and suggested images."""
    
    print("=" * 60)
    print("CITY IMAGE ANALYSIS REPORT")
    print("=" * 60)
    
    # Read current images from index.html
    with open('index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Extract current city images (simplified approach)
    import re
    
    # Pattern to find city images
    pattern = r'<div class="city-image" style="background-image: url\(\'([^\']+)\'\);">\s*<div class="city-overlay"></div>\s*<span class="city-name">([^<]+)</span>'
    matches = re.findall(pattern, html_content, re.DOTALL)
    
    print("\n📊 CURRENT IMAGE STATUS:")
    print("-" * 40)
    
    current_images = {}
    for image_url, city_name in matches:
        current_images[city_name.strip()] = image_url
        print(f"{city_name.strip():<12} → {image_url[:50]}...")
    
    print("\n🎯 RECOMMENDED IMAGE SEARCHES:")
    print("-" * 40)
    
    for city_name, queries in CITY_SEARCH_QUERIES.items():
        if city_name in current_images:
            print(f"\n{city_name}:")
            print(f"  Current: {current_images[city_name][:60]}...")
            print(f"  Search for: {', '.join(queries[:3])}")
            
            # Get suggested images
            suggested = search_images_for_city(city_name, queries)
            if suggested:
                print(f"  Suggested alternatives:")
                for i, img_url in enumerate(suggested[:2], 1):
                    print(f"    {i}. {img_url[:60]}...")
    
    print("\n" + "=" * 60)
    print("NEXT STEPS:")
    print("=" * 60)
    print("1. Review the suggested image URLs above")
    print("2. Manually verify image quality and relevance")
    print("3. Update update_city_images.py with chosen URLs")
    print("4. Run: python3 update_city_images.py")
    print("5. Run: python3 update_city_page_images.py")
    print("\n💡 TIP: For authentic Chinese city images, consider:")
    print("   - Baidu Image Search (requires Chinese IP/access)")
    print("   - Local Chinese photography websites")
    print("   - Tourism board official images")
    print("   - Creative Commons licensed photos from Chinese photographers")

def main():
    """Main function to search for city images."""
    
    print("🔍 City Image Search Assistant")
    print("=" * 40)
    
    generate_image_report()
    
    print("\n📝 To manually search for better images:")
    print("   - Visit: https://unsplash.com/s/photos/")
    print("   - Search for: 'city-name china tourism'")
    print("   - Look for high-quality, relevant images")
    print("   - Copy the image URL (right-click → Copy image address)")
    print("\n🔄 To update with new images:")
    print("   1. Edit update_city_images.py")
    print("   2. Update the IMPROVED_IMAGES dictionary")
    print("   3. Run the update scripts")

if __name__ == "__main__":
    main()