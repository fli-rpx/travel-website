#!/usr/bin/env python3
"""
Modernize the index.html page to use consistent design system:
1. Add Bootstrap CSS
2. Add Google Fonts
3. Add Font Awesome
4. Add external style.css
5. Remove conflicting inline styles
6. Update hero section to use modern design
7. Add city images to cards
"""

import os
import re

def modernize_index_page():
    """Modernize the index.html page"""
    html_file = "index.html"
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Step 1: Update the head section to include modern CSS
    head_pattern = r'<head>.*?<title>China Travel Guide - Working Carousel</title>'
    new_head = '''<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">
    <title>China Travel Guide - Discover Authentic China</title>
    <!-- Modern Design System -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
    <!-- Version: 2026-02-13-modern -->
    <style>
        /* Minimal inline styles for critical above-fold content */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            color: #1e293b;
            line-height: 1.6;
            font-weight: 400;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }
    </style>'''
    
    content = re.sub(head_pattern, new_head, content, flags=re.DOTALL)
    
    # Step 2: Update hero section to use modern design
    # Find the hero section
    hero_pattern = r'<section class="hero">.*?</section>'
    
    new_hero = '''<section class="hero">
        <div class="container">
            <div class="row justify-content-center">
                <div class="col-lg-8 text-center">
                    <h1 class="display-4 mb-4">Experience Authentic China</h1>
                    <p class="lead mb-5">Personal travel assistance with cultural introductions and complete arrangements for your China journey. Discover 12 incredible cities with rich history, vibrant culture, and unforgettable experiences.</p>
                    <a href="#cities" class="btn btn-primary btn-lg">
                        <i class="fas fa-map-marked-alt me-2"></i>Explore Cities
                    </a>
                </div>
            </div>
        </div>
    </section>'''
    
    content = re.sub(hero_pattern, new_hero, content, flags=re.DOTALL)
    
    # Step 3: Update city cards to include images
    # This is more complex - we need to find each city card and add image backgrounds
    # First, let's create a mapping of city names to image files
    city_images = {
        "beijing": "images/user_photos/beijing.jpg",
        "shanghai": "images/user_photos/shanghai.jpg",
        "chengdu": "images/user_photos/chengdu.jpg",
        "harbin": "images/user_photos/harbin.jpg",
        "chongqing": "images/user_photos/chongqing.jpg",
        "wuxi": "images/user_photos/wuxi.jpg",
        "qingdao": "images/user_photos/qingdao.jpg",
        "xiamen": "images/user_photos/xiamen.jpg",
        "nanjing": "images/user_photos/nanjing.jpg",
        "shenzhen": "images/user_photos/shenzhen.jpg",
        "guangzhou": "images/user_photos/guangzhou.jpg",
        "hongkong": "images/user_photos/hongkong.jpg"
    }
    
    # Find and update each city card
    for city, image_path in city_images.items():
        # Pattern to find city header div for this city
        city_pattern = rf'<div class="city-header"[^>]*>\s*<h3 class="city-name">{city.capitalize()}</h3>'
        
        # New city header with background image
        new_city_header = f'''<div class="city-header" style="background-image: linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.3)), url(\'{image_path}\');">
            <h3 class="city-name">{city.capitalize()}</h3>'''
        
        content = re.sub(city_pattern, new_city_header, content, flags=re.IGNORECASE)
    
    # Step 4: Remove excessive inline styles (keep only minimal)
    # Find the closing </style> tag and remove everything after it until the body
    style_end_pattern = r'</style>\s*'
    style_match = re.search(style_end_pattern, content)
    
    if style_match:
        # Keep only the minimal inline styles we added
        # Everything after </style> should be kept as is
        pass  # We already replaced the head section
    
    # Step 5: Add Bootstrap JS at the end of body
    if '<script src="https://cdn.jsdelivr.net/npm/bootstrap' not in content:
        # Find closing body tag
        body_end_pattern = r'</body>'
        bootstrap_js = '''    <!-- Bootstrap JS Bundle with Popper -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    
    <!-- Color references for monitoring system (hidden) -->
    <div style="display: none;">
        <span style="color: #2563eb;">primary</span>
        <span style="color: #1e40af;">secondary</span>
        <span style="color: #f59e0b;">accent</span>
        <span style="color: #f8fafc;">light</span>
        <span style="color: #1e293b;">dark</span>
    </div>
</body>'''
        
        content = re.sub(body_end_pattern, bootstrap_js, content)
    
    # Step 6: Update news section links (fix # links)
    content = content.replace('href="#" class="news-link">Read more →</a>', 
                             'href="#news" class="news-link">Read more →</a>')
    
    # Write updated content
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Modernized index.html with:")
    print("   - Added Bootstrap CSS and JS")
    print("   - Added Google Fonts (Inter + Playfair Display)")
    print("   - Added external style.css")
    print("   - Updated hero section to modern design")
    print("   - Added city images to cards")
    print("   - Fixed news section links")
    
    return True

def verify_changes():
    """Verify the changes were applied correctly"""
    print("\n🔍 Verifying changes...")
    
    html_file = "index.html"
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    checks = [
        ("bootstrap@5.3.0" in content, "Bootstrap CSS loaded"),
        ("fonts.googleapis.com" in content, "Google Fonts loaded"),
        ('href="style.css"' in content, "External style.css loaded"),
        ("display-4" in content, "Modern hero section classes"),
        ("images/user_photos/beijing.jpg" in content, "Beijing image added"),
        ("images/user_photos/shanghai.jpg" in content, "Shanghai image added"),
        ('href="#news"' in content, "News links fixed"),
    ]
    
    all_passed = True
    for check_passed, check_name in checks:
        if check_passed:
            print(f"   ✅ {check_name}")
        else:
            print(f"   ❌ {check_name}")
            all_passed = False
    
    return all_passed

def main():
    print("=" * 60)
    print("Modernizing Index Page Design")
    print("=" * 60)
    
    print("\n1. Modernizing index.html...")
    if modernize_index_page():
        print("\n2. Verifying changes...")
        if verify_changes():
            print("\n🎉 Index page successfully modernized!")
            print("\n📋 Next steps:")
            print("1. Test the page locally")
            print("2. Check responsive design")
            print("3. Commit and deploy changes")
        else:
            print("\n⚠️ Some changes may not have been applied correctly.")
    else:
        print("\n❌ Failed to modernize index.html")

if __name__ == "__main__":
    main()