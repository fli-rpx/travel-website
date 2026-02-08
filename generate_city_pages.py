#!/usr/bin/env python3
"""
Generate city pages for the travel website.
This script creates individual city pages with introductions and proper images.
"""

import os
import json

# City data with descriptions and image placeholders
CITIES = {
    "chengdu": {
        "name": "Chengdu",
        "tagline": "Home of Giant Pandas & Sichuan Cuisine",
        "overview": "Chengdu, the capital of Sichuan province, is famous for its laid-back teahouse culture, spicy Sichuan cuisine, and of course, the Chengdu Research Base of Giant Panda Breeding. This vibrant city combines ancient history with modern development, offering visitors a unique blend of traditional Sichuanese culture and contemporary urban life.",
        "attractions": "Chengdu Research Base of Giant Panda Breeding, Jinli Ancient Street, Wuhou Temple, Dujiangyan Irrigation System, Mount Qingcheng",
        "food": "Hot Pot, Mapo Tofu, Kung Pao Chicken, Dan Dan Noodles, Sichuan Peppercorn Dishes",
        "best_time": "Spring (March-May) and Autumn (September-November) with mild temperatures",
        "population": "20.9 million",
        "province": "Sichuan",
        "dialect": "Sichuanese Mandarin",
        "airport": "Chengdu Shuangliu International Airport (CTU) / Chengdu Tianfu International Airport (TFU)",
        "transport": "Metro, buses, and taxis are convenient for getting around the city",
        "image_placeholder": "https://images.unsplash.com/photo-1544984243-ec57ea16fe25?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
    },
    "harbin": {
        "name": "Harbin",
        "tagline": "Ice City of Northeast China",
        "overview": "Harbin, known as the 'Ice City', is famous for its spectacular Ice and Snow Festival held every winter. Located in Northeast China, the city showcases unique Russian architecture from its history as a major railway hub. Harbin offers a fascinating blend of Chinese and Russian cultures, with stunning ice sculptures, European-style buildings, and hearty Northeastern cuisine.",
        "attractions": "Harbin Ice and Snow World, Saint Sophia Cathedral, Central Street, Sun Island, Siberian Tiger Park",
        "food": "Harbin Sausage, Russian Bread, Dongbei Dumplings, Hot Pot, Smoked Fish",
        "best_time": "Winter (December-February) for the Ice Festival, Summer (June-August) for mild weather",
        "population": "10.6 million",
        "province": "Heilongjiang",
        "dialect": "Northeastern Mandarin",
        "airport": "Harbin Taiping International Airport (HRB)",
        "transport": "Metro, buses, and walking in the city center",
        "image_placeholder": "https://images.unsplash.com/photo-1528164344705-47542687000d?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
    },
    "chongqing": {
        "name": "Chongqing",
        "tagline": "Mountain City & Hot Pot Capital",
        "overview": "Chongqing, known as the 'Mountain City', is built on hills along the Yangtze River. This massive municipality is famous for its hot pot, stunning night views, and unique urban landscape with buildings constructed on steep slopes. As one of China's four direct-controlled municipalities, Chongqing offers a vibrant mix of traditional culture and rapid modernization.",
        "attractions": "Hongya Cave, Ciqikou Ancient Town, Yangtze River Cableway, Jiefangbei CBD, Three Gorges Museum",
        "food": "Chongqing Hot Pot, Spicy Noodles, Jiangtuan Fish, La Zi Ji (Spicy Chicken)",
        "best_time": "Spring (March-May) and Autumn (September-November) with comfortable temperatures",
        "population": "32.1 million",
        "province": "Chongqing Municipality",
        "dialect": "Southwestern Mandarin (Chongqing dialect)",
        "airport": "Chongqing Jiangbei International Airport (CKG)",
        "transport": "Monorail, metro, buses, and taxis (be prepared for hills!)",
        "image_placeholder": "https://images.unsplash.com/photo-1578645510447-e4b5c5d90673?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
    },
    "beijing": {
        "name": "Beijing",
        "tagline": "Ancient Capital & Modern Metropolis",
        "overview": "Beijing, China's capital for over 800 years, is a city where ancient history meets modern innovation. From the majestic Forbidden City to the contemporary architecture of the CBD, Beijing offers a journey through China's imperial past and dynamic present.",
        "attractions": "Forbidden City, Great Wall, Temple of Heaven, Summer Palace, Tiananmen Square",
        "food": "Peking Duck, Zhajiangmian, Mongolian Hot Pot, Beijing Yogurt",
        "best_time": "Autumn (September-October) with clear skies and pleasant temperatures",
        "population": "21.9 million",
        "province": "Beijing Municipality",
        "dialect": "Beijing Mandarin",
        "airport": "Beijing Capital International Airport (PEK) / Beijing Daxing International Airport (PKX)",
        "transport": "Extensive metro system, buses, and taxis",
        "image_placeholder": "https://images.unsplash.com/photo-1508804185872-d7badad00f7d?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
    },
    "shanghai": {
        "name": "Shanghai",
        "tagline": "Paris of the East & Financial Hub",
        "overview": "Shanghai, China's largest city and global financial center, blends colonial architecture with futuristic skyscrapers. The Huangpu River divides the city into historic Puxi and modern Pudong, creating a fascinating contrast between old and new.",
        "attractions": "The Bund, Yu Garden, Shanghai Tower, Nanjing Road, French Concession",
        "food": "Xiaolongbao (Soup Dumplings), Shengjianbao, Shanghai Noodles, Drunken Chicken",
        "best_time": "Spring (April-May) and Autumn (October-November) with mild weather",
        "population": "26.3 million",
        "province": "Shanghai Municipality",
        "dialect": "Shanghainese",
        "airport": "Shanghai Pudong International Airport (PVG) / Shanghai Hongqiao International Airport (SHA)",
        "transport": "Metro, Maglev train, buses, and taxis",
        "image_placeholder": "https://images.unsplash.com/photo-1578645510447-e4b5c5d90673?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
    }
}

def generate_city_page(city_data):
    """Generate HTML for a city page from template."""
    
    # Read the template
    with open('cities/template.html', 'r', encoding='utf-8') as f:
        template = f.read()
    
    # Replace placeholders with actual data
    html = template
    html = html.replace('CITY_NAME', city_data['name'])
    html = html.replace('CITY_TAGLINE', city_data['tagline'])
    html = html.replace('CITY_OVERVIEW_TEXT', city_data['overview'])
    html = html.replace('ATTRACTION_1, ATTRACTION_2, ATTRACTION_3', city_data['attractions'])
    html = html.replace('FOOD_1, FOOD_2, FOOD_3', city_data['food'])
    html = html.replace('BEST_SEASON with IDEAL_CONDITIONS', city_data['best_time'])
    html = html.replace('CITY_POPULATION', city_data['population'])
    html = html.replace('PROVINCE_NAME', city_data['province'])
    html = html.replace('LOCAL_DIALECT', city_data['dialect'])
    html = html.replace('AIRPORT_NAME (AIRPORT_CODE)', city_data['airport'])
    html = html.replace('RECOMMENDED_TRANSPORT', city_data['transport'])
    html = html.replace('CITY_IMAGE_URL', city_data['image_placeholder'])
    
    # Use the same image for gallery (in real implementation, these would be different)
    html = html.replace('GALLERY_IMAGE_1', city_data['image_placeholder'])
    html = html.replace('GALLERY_IMAGE_2', city_data['image_placeholder'])
    html = html.replace('GALLERY_IMAGE_3', city_data['image_placeholder'])
    
    # Add travel tips specific to each city
    tips = ""
    if city_data['name'] == 'Chengdu':
        tips = """<li>Visit the Panda Base early in the morning when pandas are most active</li>
            <li>Try Sichuan hot pot but ask for mild spice level if you're not used to spicy food</li>
            <li>Experience traditional tea culture at a local teahouse in People's Park</li>
            <li>Use Didi (Chinese Uber) or metro to navigate the city efficiently</li>"""
    elif city_data['name'] == 'Harbin':
        tips = """<li>Dress in layers with thermal clothing for the Ice Festival (temperatures can drop to -30°C)</li>
            <li>Visit Saint Sophia Cathedral to see beautiful Russian Orthodox architecture</li>
            <li>Try Harbin beer and Russian-style bread on Central Street</li>
            <li>Book Ice Festival tickets in advance during peak season</li>"""
    elif city_data['name'] == 'Chongqing':
        tips = """<li>Wear comfortable shoes for walking on hills and stairs</li>
            <li>Take the Yangtze River Cableway for amazing city views</li>
            <li>Try Chongqing hot pot but be prepared for extreme spiciness</li>
            <li>Visit Hongya Cave at night for spectacular illuminated views</li>"""
    elif city_data['name'] == 'Beijing':
        tips = """<li>Book Forbidden City tickets online in advance (they sell out quickly)</li>
            <li>Visit the Great Wall at Mutianyu or Jinshanling for fewer crowds</li>
            <li>Try Peking Duck at a traditional restaurant like Quanjude</li>
            <li>Use Beijing's extensive metro system to avoid traffic</li>"""
    elif city_data['name'] == 'Shanghai':
        tips = """<li>Walk along the Bund in the evening for beautiful skyline views</li>
            <li>Try xiaolongbao (soup dumplings) at a local restaurant</li>
            <li>Visit the French Concession for charming cafes and boutiques</li>
            <li>Take the Maglev train from Pudong Airport for a high-speed experience</li>"""
    
    html = html.replace('TIP_1</li>\n                            <li>TIP_2</li>\n                            <li>TIP_3</li>\n                            <li>TIP_4</li>', tips)
    
    return html

def main():
    """Main function to generate city pages."""
    
    # Create cities directory if it doesn't exist
    os.makedirs('cities', exist_ok=True)
    
    print("Generating city pages...")
    
    # Generate pages for each city
    for city_id, city_data in CITIES.items():
        filename = f"cities/{city_id}.html"
        html_content = generate_city_page(city_data)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Generated: {filename} - {city_data['name']}")
    
    print("\n🎯 Next steps:")
    print("1. Update main page city cards with proper image URLs")
    print("2. Search for specific images: Chengdu panda, Harbin ice festival, Chongqing city view")
    print("3. Update image placeholders with actual Unsplash URLs")
    print("4. Add links to all city cards in index.html")

if __name__ == "__main__":
    main()