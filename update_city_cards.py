#!/usr/bin/env python3
"""
Update city cards in index.html with proper links and images.
"""

import re

# City data with image placeholders and links
CITY_UPDATES = {
    "Chengdu": {
        "link": "cities/chengdu.html",
        "image": "https://images.unsplash.com/photo-1544984243-ec57ea16fe25?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        "tag": "Pandas & Spicy Cuisine"
    },
    "Beijing": {
        "link": "cities/beijing.html",
        "image": "https://images.unsplash.com/photo-1508804185872-d7badad00f7d?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        "tag": "Great Wall & Forbidden City"
    },
    "Wuxi": {
        "link": "cities/wuxi.html",
        "image": "https://images.unsplash.com/photo-1592210454359-9043f067919b?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        "tag": "Taihu Lake & Gardens"
    },
    "Qingdao": {
        "link": "cities/qingdao.html",
        "image": "https://images.unsplash.com/photo-1518834103328-93d45986dce1?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        "tag": "Beer & Beaches"
    },
    "Xiamen": {
        "link": "cities/xiamen.html",
        "image": "https://images.unsplash.com/photo-1518834103328-93d45986dce1?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        "tag": "Gulangyu Island & Beaches"
    },
    "Harbin": {
        "link": "cities/harbin.html",
        "image": "https://images.unsplash.com/photo-1528164344705-47542687000d?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        "tag": "Ice Festival & Russian Architecture"
    },
    "Shanghai": {
        "link": "cities/shanghai.html",
        "image": "https://images.unsplash.com/photo-1578645510447-e4b5c5d90673?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        "tag": "The Bund & Skyscrapers"
    },
    "Nanjing": {
        "link": "cities/nanjing.html",
        "image": "https://images.unsplash.com/photo-1518834103328-93d45986dce1?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        "tag": "Ancient Capital & Yangtze River"
    },
    "Shenzhen": {
        "link": "cities/shenzhen.html",
        "image": "https://images.unsplash.com/photo-1508804185872-d7badad00f7d?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        "tag": "Tech Hub & Theme Parks"
    },
    "Guangzhou": {
        "link": "cities/guangzhou.html",
        "image": "https://images.unsplash.com/photo-1544984243-ec57ea16fe25?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        "tag": "Cantonese Food & Trade Center"
    },
    "Hongkong": {
        "link": "cities/hongkong.html",
        "image": "https://images.unsplash.com/photo-1518834103328-93d45986dce1?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        "tag": "Victoria Harbour & Skyline"
    },
    "Chongqing": {
        "link": "cities/chongqing.html",
        "image": "https://images.unsplash.com/photo-1508804185872-d7badad00f7d?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        "tag": "Mountain City & Hot Pot"
    }
}

def update_city_card(html, city_name, city_data):
    """Update a single city card with link and image."""
    
    # Pattern to find the city card
    pattern = rf'<div class="city-card">\s*(<a[^>]*>)?\s*<div class="city-image" style="background-image: url\(\'[^\']+\'\);">\s*<div class="city-overlay"></div>\s*<span class="city-name">{city_name}</span>\s*</div>\s*<div class="city-tag">[^<]+</div>\s*(</a>)?\s*</div>'
    
    # Replacement template with link
    replacement = f'''<div class="city-card">
                                <a href="{city_data['link']}" class="city-card-link">
                                    <div class="city-image" style="background-image: url('{city_data['image']}');">
                                        <div class="city-overlay"></div>
                                        <span class="city-name">{city_name}</span>
                                    </div>
                                    <div class="city-tag">{city_data['tag']}</div>
                                </a>
                            </div>'''
    
    # Replace in HTML
    updated_html = re.sub(pattern, replacement, html, flags=re.DOTALL)
    
    return updated_html

def main():
    """Main function to update city cards."""
    
    # Read the index.html file
    with open('index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    print("Updating city cards with links and images...")
    
    # Update each city card
    original_html = html_content
    for city_name, city_data in CITY_UPDATES.items():
        html_content = update_city_card(html_content, city_name, city_data)
        print(f"✅ Updated: {city_name}")
    
    # Write back to file
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("\n✅ All city cards updated!")
    print("\n🎯 Images still need improvement:")
    print("1. Chengdu needs panda image")
    print("2. Harbin needs ice festival image")
    print("3. Chongqing needs city view image")
    print("4. Other cities need unique images (not duplicates)")

if __name__ == "__main__":
    main()