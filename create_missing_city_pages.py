#!/usr/bin/env python3
"""
Create missing city pages for the travel website.
This creates pages for the 7 cities that don't have individual pages yet.
"""

import os
import shutil

# Cities that need pages (don't exist yet)
MISSING_CITIES = [
    "wuxi",
    "qingdao", 
    "xiamen",
    "nanjing",
    "shenzhen",
    "guangzhou",
    "hongkong"
]

# City display names and descriptions
CITY_INFO = {
    "wuxi": {
        "display_name": "Wuxi",
        "description": "Known for its beautiful Taihu Lake and ancient Grand Buddha",
        "tagline": "The Pearl of Taihu Lake"
    },
    "qingdao": {
        "display_name": "Qingdao", 
        "description": "Famous for its beaches, Tsingtao Beer, and European architecture",
        "tagline": "Where East Meets West"
    },
    "xiamen": {
        "display_name": "Xiamen",
        "description": "A coastal city with beautiful Gulangyu Island and beaches",
        "tagline": "The Garden on the Sea"
    },
    "nanjing": {
        "display_name": "Nanjing",
        "description": "Ancient capital with rich history and cultural heritage",
        "tagline": "The Ancient Capital of Six Dynasties"
    },
    "shenzhen": {
        "display_name": "Shenzhen",
        "description": "Modern tech hub and China's Silicon Valley",
        "tagline": "China's Innovation Capital"
    },
    "guangzhou": {
        "display_name": "Guangzhou",
        "description": "Vibrant metropolis known as the Southern Gate of China",
        "tagline": "The Flower City"
    },
    "hongkong": {
        "display_name": "Hong Kong",
        "description": "Dynamic international hub with stunning skyline and harbor",
        "tagline": "Asia's World City"
    }
}

def create_city_page(city_id):
    """Create a city page from template."""
    
    if city_id not in CITY_INFO:
        print(f"❌ No info for city: {city_id}")
        return False
    
    city_info = CITY_INFO[city_id]
    template_file = "cities/template.html"
    output_file = f"cities/{city_id}.html"
    
    # Check if file already exists
    if os.path.exists(output_file):
        print(f"⚠️  Skipping {city_id}: Page already exists")
        return False
    
    # Read template
    with open(template_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace placeholders
    content = content.replace("City Name", city_info["display_name"])
    content = content.replace("CITY_DESCRIPTION", city_info["description"])
    content = content.replace("CITY_TAGLINE", city_info["tagline"])
    
    # Use current Unsplash image as placeholder (will be replaced later)
    # For now, use a generic China image
    placeholder_image = "https://images.unsplash.com/photo-1508804185872-d7badad00f7d?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80"
    content = content.replace("CITY_IMAGE_URL", placeholder_image)
    
    # Write output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def update_main_page_links():
    """Update main page to include links to new city pages."""
    
    main_page = "index.html"
    
    with open(main_page, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We'll need to update the city cards section
    # For now, just note that main page needs updating
    print("\n📝 Note: Main page city cards need to be updated")
    print("   Currently only shows 12 cities, need to ensure all are linked")
    
    return True

def main():
    """Create all missing city pages."""
    
    print("=" * 60)
    print("CREATE MISSING CITY PAGES")
    print("=" * 60)
    
    print(f"\n🎯 Creating pages for {len(MISSING_CITIES)} missing cities:")
    for city in MISSING_CITIES:
        print(f"  • {CITY_INFO[city]['display_name']}")
    
    print("\n📁 Starting creation...")
    
    created_count = 0
    for city_id in MISSING_CITIES:
        if create_city_page(city_id):
            print(f"✅ Created: {city_id}.html")
            created_count += 1
        else:
            print(f"⚠️  Skipped: {city_id}.html")
    
    print(f"\n📊 Created {created_count} new city pages")
    
    if created_count > 0:
        print("\n🎨 Next steps:")
        print("1. Update images for all city pages")
        print("2. Ensure consistent styling")
        print("3. Update main page links")
        print("4. Test all pages")
        
        print("\n🔧 Run these scripts next:")
        print("   python3 update_city_page_images.py  # Update images")
        print("   python3 verify_images.py           # Check consistency")
    
    print("\n✅ Phase 1 Complete: All city pages created!")
    print("   Now we need to find/generate proper images for each city.")

if __name__ == "__main__":
    main()