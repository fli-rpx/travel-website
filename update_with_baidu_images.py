#!/usr/bin/env python3
"""
Helper script to update website with Baidu images once downloaded.
This script helps replace Unsplash images with Baidu images.
"""

import os
import json

def create_baidu_image_template():
    """Create a template file to track Baidu image replacements."""
    
    template = {
        "instructions": "Replace the Unsplash URLs below with your Baidu image URLs",
        "note": "After downloading images from Baidu, update the URLs here and run update script",
        "cities": {
            "Beijing": {
                "current_unsplash": "https://images.unsplash.com/photo-1508804185872-d7badad00f7d?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80",
                "baidu_replacement": "REPLACE_WITH_BAIDU_IMAGE_URL",
                "description": "Great Wall or Forbidden City image from Baidu",
                "search_queries": ["北京 长城", "北京 故宫", "北京 旅游 景点"]
            },
            "Shanghai": {
                "current_unsplash": "https://images.unsplash.com/photo-1578645510447-e4b5c5d90673?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80",
                "baidu_replacement": "REPLACE_WITH_BAIDU_IMAGE_URL",
                "description": "Shanghai skyline or Bund image from Baidu",
                "search_queries": ["上海 外滩", "上海 东方明珠", "上海 夜景"]
            },
            "Chengdu": {
                "current_unsplash": "https://images.unsplash.com/photo-1564349683136-77e08dba1ef7?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80",
                "baidu_replacement": "REPLACE_WITH_BAIDU_IMAGE_URL",
                "description": "Panda or Chengdu street image from Baidu",
                "search_queries": ["成都 熊猫", "成都 大熊猫基地", "成都 锦里"]
            },
            "Harbin": {
                "current_unsplash": "https://images.unsplash.com/photo-1517299321609-52687d1bc55a?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80",
                "baidu_replacement": "REPLACE_WITH_BAIDU_IMAGE_URL",
                "description": "Ice festival or snow scene from Baidu",
                "search_queries": ["哈尔滨 冰雪大世界", "哈尔滨 冰雕", "哈尔滨 雪景"]
            },
            "Chongqing": {
                "current_unsplash": "https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80",
                "baidu_replacement": "REPLACE_WITH_BAIDU_IMAGE_URL",
                "description": "Mountain city or Hongya Cave from Baidu",
                "search_queries": ["重庆 山城", "重庆 洪崖洞", "重庆 夜景"]
            }
        }
    }
    
    with open('baidu_image_replacements.json', 'w', encoding='utf-8') as f:
        json.dump(template, f, indent=2, ensure_ascii=False)
    
    return 'baidu_image_replacements.json'

def generate_update_instructions():
    """Generate instructions for updating with Baidu images."""
    
    print("=" * 70)
    print("BAIDU IMAGE UPDATE INSTRUCTIONS")
    print("=" * 70)
    
    print("\n📋 STEP 1: Search and Download Images")
    print("-" * 40)
    print("1. Open baidu_image_search.html in your browser")
    print("2. Click search links (requires China access/VPN)")
    print("3. Download high-quality images (1920x1080 or larger)")
    print("4. Save images with descriptive names:")
    print("   • beijing_great_wall.jpg")
    print("   • shanghai_bund.jpg")
    print("   • chengdu_panda.jpg")
    print("   • etc.")
    
    print("\n📋 STEP 2: Host Images")
    print("-" * 40)
    print("Option A: Upload to image hosting service")
    print("   • ImgBB, PostImage, or similar")
    print("   • Get direct image URLs")
    print("\nOption B: Host locally in website")
    print("   • Create folder: travel-website/images/baidu/")
    print("   • Place images there")
    print("   • Use relative paths: images/baidu/beijing_great_wall.jpg")
    
    print("\n📋 STEP 3: Update Image URLs")
    print("-" * 40)
    print("1. Edit baidu_image_replacements.json")
    print("2. Replace 'REPLACE_WITH_BAIDU_IMAGE_URL' with actual URLs")
    print("3. Save the file")
    
    print("\n📋 STEP 4: Run Update Script")
    print("-" * 40)
    print("1. Create update script (see below)")
    print("2. Run it to replace all Unsplash images with Baidu images")
    print("3. Verify the updates")
    
    print("\n" + "=" * 70)
    print("SAMPLE UPDATE SCRIPT")
    print("=" * 70)
    
    sample_script = '''#!/usr/bin/env python3
"""
Update website with Baidu images.
Run this after updating baidu_image_replacements.json.
"""

import json
import re

def update_images():'''
    # Load Baidu image replacements
    with open('baidu_image_replacements.json', 'r', encoding='utf-8') as f:
        replacements = json.load(f)
    
    # Update index.html (main page)
    print("Updating main page images...")
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    for city, data in replacements['cities'].items():
        if data['baidu_replacement'] != 'REPLACE_WITH_BAIDU_IMAGE_URL':
            # Replace in main page
            html = html.replace(data['current_unsplash'], data['baidu_replacement'])
            print(f"  ✅ Updated {city}")
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    # Update city pages
    print("\\nUpdating city pages...")
    city_pages = {
        'Beijing': 'beijing.html',
        'Shanghai': 'shanghai.html',
        'Chengdu': 'chengdu.html',
        'Harbin': 'harbin.html',
        'Chongqing': 'chongqing.html'
    }
    
    for city, page in city_pages.items():
        if city in replacements['cities']:
            data = replacements['cities'][city]
            if data['baidu_replacement'] != 'REPLACE_WITH_BAIDU_IMAGE_URL':
                page_path = f'cities/{page}'
                with open(page_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Replace all occurrences
                content = content.replace(data['current_unsplash'], data['baidu_replacement'])
                
                with open(page_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"  ✅ Updated {page_path}")
    
    print("\\n✅ Update complete!")
    print("\\n🔍 Next steps:")
    print("1. Open index.html in browser to verify changes")
    print("2. Check each city page")
    print("3. Test image loading and quality")

if __name__ == "__main__":
    update_images()
'''
    
    print(sample_script)
    
    print("\n" + "=" * 70)
    print("QUICK START")
    print("=" * 70)
    
    print("\nTo get started immediately:")
    print("1. python3 baidu_image_search.py")
    print("2. Open baidu_image_search.html")
    print("3. Search and download 1-2 images as test")
    print("4. Update baidu_image_replacements.json")
    print("5. Create and run update script")
    print("6. Verify the changes work")

def main():
    """Main function to set up Baidu image update system."""
    
    print("🔧 Baidu Image Update Setup")
    print("=" * 50)
    
    # Create template file
    template_file = create_baidu_image_template()
    print(f"✅ Created: {template_file}")
    print("   Edit this file to add your Baidu image URLs")
    
    # Generate instructions
    generate_update_instructions()
    
    print("\n🎯 Summary:")
    print("1. Template file created: baidu_image_replacements.json")
    print("2. Search page available: baidu_image_search.html")
    print("3. Sample update script provided above")
    print("\n📝 Next: Search Baidu, download images, update template, run update")

if __name__ == "__main__":
    main()