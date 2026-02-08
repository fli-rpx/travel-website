#!/usr/bin/env python3
"""
FIX: Update city page images to match main page - CORRECT VERSION
This script actually updates the existing image URLs in city pages.
"""

import os
import re

# Same images as used in main page (from update_city_images_v2.py)
CITY_IMAGES = {
    "beijing": "https://images.unsplash.com/photo-1508804185872-d7badad00f7d?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80",
    "shanghai": "https://images.unsplash.com/photo-1578645510447-e4b5c5d90673?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80",
    "chengdu": "https://images.unsplash.com/photo-1564349683136-77e08dba1ef7?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80",
    "harbin": "https://images.unsplash.com/photo-1517299321609-52687d1bc55a?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80",
    "chongqing": "https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80",
}

def update_city_page_images(city_file, image_url):
    """Update ALL image URLs in city page to match the new high-quality image."""
    
    with open(city_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"\n📁 Processing: {city_file}")
    
    # Count how many image URLs we're replacing
    old_urls = re.findall(r'https://images\.unsplash\.com/[^\s"\']+', content)
    print(f"   Found {len(old_urls)} Unsplash image URLs in file")
    
    # Update hero image (in style attribute)
    hero_pattern = r"(style=\"--hero-image: url\(')(https://images\.unsplash\.com/[^']+)('\)\")"
    
    def replace_hero(match):
        return f"{match.group(1)}{image_url}{match.group(3)}"
    
    content, hero_count = re.subn(hero_pattern, replace_hero, content)
    if hero_count > 0:
        print(f"   ✅ Updated hero image")
    
    # Update gallery images (in img src attributes)
    gallery_pattern = r"(<img[^>]+src=\")(https://images\.unsplash\.com/[^\"]+)(\"[^>]*>)"
    
    def replace_gallery(match):
        return f"{match.group(1)}{image_url}{match.group(3)}"
    
    content, gallery_count = re.subn(gallery_pattern, replace_gallery, content)
    if gallery_count > 0:
        print(f"   ✅ Updated {gallery_count} gallery images")
    
    # Also update any other Unsplash URLs in the page
    unsplash_pattern = r"(https://images\.unsplash\.com/[^\s\"']+)"
    
    def replace_unsplash(match):
        # Only replace if it's an image URL (not checking full pattern, but good enough)
        if 'unsplash.com/photo-' in match.group(1):
            return image_url
        return match.group(1)
    
    content, unsplash_count = re.subn(unsplash_pattern, replace_unsplash, content)
    if unsplash_count > hero_count + gallery_count:
        print(f"   ✅ Updated {unsplash_count - hero_count - gallery_count} additional images")
    
    # Write back to file
    with open(city_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return hero_count + gallery_count

def main():
    """Fix all city page images to match main page."""
    
    print("=" * 60)
    print("FIXING CITY PAGE IMAGES - CORRECT VERSION")
    print("=" * 60)
    print("Updating city pages to use correct, high-quality images...\n")
    
    total_updates = 0
    
    for city_id, image_url in CITY_IMAGES.items():
        city_file = f"cities/{city_id}.html"
        if os.path.exists(city_file):
            updates = update_city_page_images(city_file, image_url)
            total_updates += updates
        else:
            print(f"⚠️  Not found: {city_file}")
    
    print("\n" + "=" * 60)
    print("FIX COMPLETE")
    print("=" * 60)
    print(f"Total image updates: {total_updates}")
    
    print("\n🔍 Verification needed:")
    print("1. Open each city page in browser")
    print("2. Check that images load correctly")
    print("3. Verify images match the main page")
    
    print("\n📸 Expected images:")
    print("   • Beijing: Great Wall (1508804185872)")
    print("   • Shanghai: Skyline (1578645510447)")
    print("   • Chengdu: Panda (1564349683136)")
    print("   • Harbin: Ice/Snow (1517299321609)")
    print("   • Chongqing: Mountain city (1544551763)")

if __name__ == "__main__":
    main()