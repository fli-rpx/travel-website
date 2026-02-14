#!/usr/bin/env python3
"""
Fix navigation paths in city pages:
1. Change absolute paths to relative paths for GitHub Pages compatibility
2. Ensure all navigation links work both locally and on GitHub Pages
"""

import os
import re

def fix_city_page_navigation():
    """Fix navigation paths in all city pages"""
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
        
        # Fix 1: Change absolute back-to-home path to relative
        old_back_home = 'href="/travel-website/index.html"'
        new_back_home = 'href="../index.html"'
        content = content.replace(old_back_home, new_back_home)
        
        # Fix 2: Check and fix any other absolute paths
        # Pattern for absolute paths that should be relative
        absolute_path_pattern = r'href="/(travel-website/)?(cities/|images/)'
        
        def make_relative(match):
            path = match.group(0)
            # Convert /travel-website/cities/ to ../cities/
            # Convert /travel-website/images/ to ../images/
            # Convert /cities/ to ../cities/ (if no travel-website prefix)
            if 'travel-website/' in path:
                return path.replace('/travel-website/', '../')
            else:
                return path.replace('/', '../', 1)
        
        content = re.sub(absolute_path_pattern, make_relative, content)
        
        # Fix 3: Ensure CSS and JS links are correct
        # Bootstrap CSS should use CDN (already correct)
        # Font Awesome should use CDN (already correct)
        # Google Fonts should use CDN (already correct)
        # Local style.css should use correct path
        
        # Check if style.css link needs fixing
        style_pattern = r'<link rel="stylesheet" href="([^"]*style\.css[^"]*)"'
        style_match = re.search(style_pattern, content)
        if style_match:
            current_style = style_match.group(1)
            if current_style.startswith('/travel-website/'):
                new_style = current_style.replace('/travel-website/', '../')
                content = content.replace(current_style, new_style)
                print(f"✅ Fixed style.css path in {city}.html")
        
        # Write updated content
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Fixed navigation paths in {city}.html")

def fix_main_page_navigation():
    """Fix navigation paths in main index.html"""
    html_file = "index.html"
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix city links in main page
    # They should be relative: href="cities/beijing.html" not absolute
    
    # Check for any absolute paths to cities
    absolute_city_pattern = r'href="/(travel-website/)?cities/([^"]+)"'
    
    def make_city_relative(match):
        city_file = match.group(2)
        return f'href="cities/{city_file}"'
    
    content = re.sub(absolute_city_pattern, make_city_relative, content)
    
    # Write updated content
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Fixed navigation paths in index.html")

def verify_navigation():
    """Verify all navigation links are relative"""
    print("\n🔍 Verifying navigation paths:")
    
    issues_found = False
    
    # Check city pages
    cities = [
        "beijing", "shanghai", "chengdu", "harbin", "chongqing",
        "wuxi", "qingdao", "xiamen", "nanjing", "shenzhen", 
        "guangzhou", "hongkong"
    ]
    
    for city in cities:
        html_file = f"cities/{city}.html"
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for absolute paths
        absolute_patterns = [
            r'href="/travel-website/',
            r'src="/travel-website/',
            r'url\(/travel-website/'
        ]
        
        for pattern in absolute_patterns:
            if re.search(pattern, content):
                print(f"⚠️  {city}: Found absolute path pattern: {pattern}")
                issues_found = True
        
        # Check back-to-home link
        if 'href="../index.html"' not in content:
            print(f"⚠️  {city}: Back-to-home link may be incorrect")
            issues_found = True
    
    # Check main page
    with open("index.html", 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for absolute city links
    if re.search(r'href="/travel-website/cities/', content):
        print("⚠️  index.html: Found absolute city links")
        issues_found = True
    
    if not issues_found:
        print("✅ All navigation paths are relative and correct")
    
    return not issues_found

def main():
    print("=" * 60)
    print("Fixing Navigation Paths for GitHub Pages")
    print("=" * 60)
    
    # Step 1: Fix city page navigation
    print("\n1. Fixing city page navigation...")
    fix_city_page_navigation()
    
    # Step 2: Fix main page navigation
    print("\n2. Fixing main page navigation...")
    fix_main_page_navigation()
    
    # Step 3: Verify fixes
    print("\n3. Verifying navigation paths...")
    if verify_navigation():
        print("\n🎉 All navigation issues fixed successfully!")
    else:
        print("\n⚠️  Some navigation issues remain. Please check warnings above.")
    
    print("\n📋 Next steps:")
    print("1. Test navigation locally")
    print("2. Commit and push changes")
    print("3. Test on GitHub Pages")

if __name__ == "__main__":
    main()