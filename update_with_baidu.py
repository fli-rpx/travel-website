#!/usr/bin/env python3
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
    print("\nUpdating city pages...")
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
    
    print(f"\n✅ Update complete! Made {updates_made} image updates.")
    
    if updates_made > 0:
        print("\n🔍 Next steps:")
        print("1. Open index.html in browser to verify changes")
        print("2. Check each city page")
        print("3. Test image loading and quality")
    else:
        print("\n⚠️  No updates made. Check baidu_image_replacements.json")
        print("   Make sure you replaced 'REPLACE_WITH_BAIDU_IMAGE_URL' with actual URLs")

if __name__ == "__main__":
    update_images()
