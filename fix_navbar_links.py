#!/usr/bin/env python3
"""
Fix navbar links in city pages that point to main page sections
"""

import os

def fix_navbar_links():
    """Fix navbar links in all city pages"""
    cities = [
        "beijing", "shanghai", "chengdu", "harbin", "chongqing",
        "wuxi", "qingdao", "xiamen", "nanjing", "shenzhen", 
        "guangzhou", "hongkong"
    ]
    
    for city in cities:
        html_file = f"cities/{city}.html"
        if not os.path.exists(html_file):
            print(f"⚠️  Skipping {city}: {html_file} not found")
            continue
            
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix navbar links - they should point to ../index.html#section
        # Replace /travel-website/index.html# with ../index.html#
        
        old_nav_links = [
            'href="/travel-website/index.html#home"',
            'href="/travel-website/index.html#about"',
            'href="/travel-website/index.html#services"',
            'href="/travel-website/index.html#destinations"',
            'href="/travel-website/index.html#contact"',
            'href="/travel-website/index.html#news"'  # Added news section
        ]
        
        new_nav_links = [
            'href="../index.html#home"',
            'href="../index.html#about"',
            'href="../index.html#services"',
            'href="../index.html#destinations"',
            'href="../index.html#contact"',
            'href="../index.html#news"'
        ]
        
        for old, new in zip(old_nav_links, new_nav_links):
            if old in content:
                content = content.replace(old, new)
                print(f"✅ Fixed navbar link in {city}.html: {old} -> {new}")
        
        # Write updated content
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)

def main():
    print("=" * 60)
    print("Fixing Navbar Links in City Pages")
    print("=" * 60)
    
    fix_navbar_links()
    print("\n🎉 Navbar links fixed successfully!")

if __name__ == "__main__":
    main()