#!/usr/bin/env python3
"""
Setup for Baidu Image Search and Update System.
This script creates all necessary files for searching and updating with Baidu images.
"""

import json
import os

def create_baidu_template():
    """Create template JSON for Baidu image replacements."""
    
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

def create_update_script():
    """Create the actual update script."""
    
    script_content = '''#!/usr/bin/env python3
"""
Update website with Baidu images.
Run this after updating baidu_image_replacements.json.
"""

import json
import re

def update_images():
    """Update website images with Baidu replacements."""
    
    # Load Baidu image replacements
    try:
        with open('baidu_image_replacements.json', 'r', encoding='utf-8') as f:
            replacements = json.load(f)
    except FileNotFoundError:
        print("❌ Error: baidu_image_replacements.json not found!")
        print("   Run setup_baidu_images.py first")
        return
    
    # Update index.html (main page)
    print("Updating main page images...")
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    updates_made = 0
    for city, data in replacements['cities'].items():
        if data['baidu_replacement'] != 'REPLACE_WITH_BAIDU_IMAGE_URL':
            # Replace in main page
            old_count = html.count(data['current_unsplash'])
            html = html.replace(data['current_unsplash'], data['baidu_replacement'])
            new_count = html.count(data['baidu_replacement'])
            
            if new_count > 0:
                updates_made += 1
                print(f"  ✅ Updated {city}: {old_count} → {new_count} replacements")
    
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
                try:
                    with open(page_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Replace all occurrences
                    old_count = content.count(data['current_unsplash'])
                    content = content.replace(data['current_unsplash'], data['baidu_replacement'])
                    new_count = content.count(data['baidu_replacement'])
                    
                    with open(page_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    if new_count > 0:
                        updates_made += 1
                        print(f"  ✅ Updated {page_path}: {old_count} → {new_count} replacements")
                        
                except FileNotFoundError:
                    print(f"  ⚠️  Skipped {page_path}: File not found")
    
    print(f"\\n✅ Update complete! Made {updates_made} image updates.")
    
    if updates_made > 0:
        print("\\n🔍 Next steps:")
        print("1. Open index.html in browser to verify changes")
        print("2. Check each city page")
        print("3. Test image loading and quality")
    else:
        print("\\n⚠️  No updates made. Check baidu_image_replacements.json")
        print("   Make sure you replaced 'REPLACE_WITH_BAIDU_IMAGE_URL' with actual URLs")

if __name__ == "__main__":
    update_images()
'''
    
    with open('update_with_baidu.py', 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    # Make it executable
    os.chmod('update_with_baidu.py', 0o755)
    
    return 'update_with_baidu.py'

def main():
    """Main setup function."""
    
    print("=" * 70)
    print("BAIDU IMAGE SEARCH & UPDATE SYSTEM SETUP")
    print("=" * 70)
    
    print("\n🎯 Setting up Baidu image integration...")
    
    # Step 1: Create template
    template_file = create_baidu_template()
    print(f"✅ Step 1: Created {template_file}")
    print("   This file tracks which images to replace")
    
    # Step 2: Create update script
    update_script = create_update_script()
    print(f"✅ Step 2: Created {update_script}")
    print("   This script updates your website with Baidu images")
    
    # Step 3: Check for search script
    if os.path.exists('baidu_image_search.py'):
        print(f"✅ Step 3: Found baidu_image_search.py")
        print("   Run this to generate Baidu search links")
    else:
        print(f"⚠️  Step 3: baidu_image_search.py not found")
        print("   Run: python3 baidu_image_search.py (if available)")
    
    print("\n" + "=" * 70)
    print("WORKFLOW INSTRUCTIONS")
    print("=" * 70)
    
    print("\n📋 Complete Workflow:")
    print("1. Search: Run baidu_image_search.py or open baidu_image_search.html")
    print("2. Download: Get images from Baidu (requires China access/VPN)")
    print("3. Host: Upload images to hosting service or local server")
    print("4. Update: Edit baidu_image_replacements.json with new URLs")
    print("5. Apply: Run python3 update_with_baidu.py")
    print("6. Verify: Check website looks correct")
    
    print("\n📋 Quick Test (1 city):")
    print("1. Search Baidu for '北京 长城'")
    print("2. Download one Great Wall image")
    print("3. Host it (ImgBB or similar)")
    print("4. Update baidu_image_replacements.json for Beijing")
    print("5. Run update_with_baidu.py")
    print("6. Check if Beijing image updated correctly")
    
    print("\n" + "=" * 70)
    print("IMPORTANT NOTES")
    print("=" * 70)
    
    print("\n⚠️  Legal Considerations:")
    print("• Check image licenses before commercial use")
    print("• Some Baidu images may be copyrighted")
    print("• Consider official tourism board images")
    
    print("\n🌐 Access Requirements:")
    print("• Baidu Image Search requires China IP")
    print("• Use VPN with Chinese server if outside China")
    print("• May need to solve captchas")
    
    print("\n🖼️  Image Quality:")
    print("• Aim for 1920x1080 resolution or higher")
    print("• Choose images without watermarks")
    print("• Test loading speed on your website")
    
    print("\n✅ Setup complete! You're ready to search and update with Baidu images.")

if __name__ == "__main__":
    main()