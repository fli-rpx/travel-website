#!/usr/bin/env python3
"""
Baidu Image Search Assistant for Chinese Cities
This script helps search for authentic Chinese city images on Baidu.
"""

import urllib.parse

# Chinese search queries for each city (more authentic than English)
CITY_CHINESE_QUERIES = {
    # Format: {city_name: [chinese_query1, chinese_query2, ...]}
    "Beijing": ["北京 旅游 景点", "北京 长城", "北京 故宫", "北京 天安门", "北京 夜景"],
    "Shanghai": ["上海 旅游", "上海 外滩", "上海 东方明珠", "上海 夜景", "上海 现代建筑"],
    "Chengdu": ["成都 旅游", "成都 熊猫", "成都 大熊猫基地", "成都 锦里", "成都 美食"],
    "Harbin": ["哈尔滨 旅游", "哈尔滨 冰雪大世界", "哈尔滨 冰雕", "哈尔滨 雪景", "哈尔滨 圣索菲亚教堂"],
    "Chongqing": ["重庆 旅游", "重庆 山城", "重庆 洪崖洞", "重庆 夜景", "重庆 火锅"],
    "Wuxi": ["无锡 旅游", "无锡 太湖", "无锡 灵山大佛", "无锡 古镇", "无锡 园林"],
    "Qingdao": ["青岛 旅游", "青岛 海滩", "青岛 啤酒", "青岛 栈桥", "青岛 德国建筑"],
    "Xiamen": ["厦门 旅游", "厦门 鼓浪屿", "厦门 海滩", "厦门 大学", "厦门 环岛路"],
    "Nanjing": ["南京 旅游", "南京 夫子庙", "南京 中山陵", "南京 城墙", "南京 秦淮河"],
    "Shenzhen": ["深圳 旅游", "深圳 现代建筑", "深圳 科技园", "深圳 世界之窗", "深圳 夜景"],
    "Guangzhou": ["广州 旅游", "广州 小蛮腰", "广州 珠江", "广州 陈家祠", "广州 美食"],
    "Hongkong": ["香港 旅游", "香港 维多利亚港", "香港 夜景", "香港 天际线", "香港 迪士尼"]
}

# Image types to search for (for better results)
IMAGE_TYPES = {
    "scenery": "风景",      # Scenery/landscape
    "architecture": "建筑", # Architecture
    "food": "美食",         # Food
    "culture": "文化",      # Culture
    "night": "夜景",        # Night view
}

def generate_baidu_search_url(query, image_type=None):
    """Generate Baidu Image search URL for a query."""
    # Combine query with image type if specified
    search_query = query
    if image_type:
        search_query = f"{query} {image_type}"
    
    # URL encode the Chinese query
    encoded_query = urllib.parse.quote(search_query)
    
    # Baidu Image search URL format
    url = f"https://image.baidu.com/search/index?tn=baiduimage&word={encoded_query}"
    
    # Add parameters for better results
    url += "&ie=utf-8"
    url += "&fr=search"
    url += "&ct=201326592"
    url += "&cl=2"
    url += "&lm=-1"
    url += "&st=-1"
    url += "&fm=result"
    url += "&pos=0"
    url += "&istype=2"
    url += "&nc=1"
    
    return url

def generate_search_report():
    """Generate a comprehensive search report."""
    
    print("=" * 70)
    print("BAIDU IMAGE SEARCH ASSISTANT - 百度图片搜索助手")
    print("=" * 70)
    print("\n🎯 Searching for authentic Chinese city images on Baidu...")
    print("   Note: Baidu Image Search works best from within China")
    print("=" * 70)
    
    for city_name, queries in CITY_CHINESE_QUERIES.items():
        print(f"\n🏙️  {city_name}:")
        print("-" * 40)
        
        # Primary search query (first one)
        primary_query = queries[0]
        primary_url = generate_baidu_search_url(primary_query)
        
        print(f"🔍 主要搜索: {primary_query}")
        print(f"   📎 链接: {primary_url}")
        
        # Alternative searches
        if len(queries) > 1:
            print(f"   🔄 备选搜索:")
            for i, alt_query in enumerate(queries[1:3], 1):  # Show 2 alternatives
                alt_url = generate_baidu_search_url(alt_query)
                print(f"      {i}. {alt_query}")
                print(f"         {alt_url}")
        
        # Image type suggestions
        print(f"   🖼️  图片类型建议:")
        for type_key, type_chinese in IMAGE_TYPES.items():
            type_url = generate_baidu_search_url(primary_query, type_chinese)
            print(f"      • {type_chinese}: {type_url}")
    
    print("\n" + "=" * 70)
    print("📋 HOW TO USE BAIDU IMAGES")
    print("=" * 70)
    
    print("\n1. **Access Requirements**:")
    print("   • You need to be in China OR use a VPN with Chinese IP")
    print("   • Baidu may require solving captchas for image downloads")
    
    print("\n2. **Search Tips**:")
    print("   • Click the links above to open Baidu Image Search")
    print("   • Use Chinese queries for best results")
    print("   • Filter by size: 选择 '大尺寸' for high-resolution")
    print("   • Filter by type: 选择 '风景', '建筑', etc.")
    
    print("\n3. **Downloading Images**:")
    print("   • Right-click on image → '图片另存为' (Save image as)")
    print("   • Check image resolution (aim for 1920x1080 or larger)")
    print("   • Note: Some images may have watermarks")
    
    print("\n4. **Legal Considerations**:")
    print("   • Check image licenses before commercial use")
    print("   • Some Baidu images may be copyrighted")
    print("   • Consider using: 百度图库 (Baidu Image Library) for licensed images")
    
    print("\n5. **Alternative Sources**:")
    print("   • 携程旅行网 (Ctrip) - Official tourism photos")
    print("   • 马蜂窝 (Mafengwo) - User-generated travel photos")
    print("   • 各地旅游局官网 (Local tourism bureau websites)")
    
    print("\n" + "=" * 70)
    print("🚀 QUICK START GUIDE")
    print("=" * 70)
    
    print("\nFor immediate use, try these 5 cities first:")
    urgent_cities = ["Beijing", "Shanghai", "Chengdu", "Harbin", "Chongqing"]
    
    for city in urgent_cities:
        query = CITY_CHINESE_QUERIES[city][0]
        url = generate_baidu_search_url(query, "风景")  # Scenery type
        print(f"\n{city}:")
        print(f"   搜索: {query} 风景")
        print(f"   链接: {url}")

def create_html_search_page():
    """Create an HTML page with clickable Baidu search links."""
    
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Baidu Image Search - Chinese Cities</title>
    <style>
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f8fafc;
            color: #1e293b;
        }
        h1, h2, h3 {
            color: #2563eb;
            font-family: 'Playfair Display', Georgia, serif;
        }
        .city-card {
            background: white;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            border-left: 4px solid #2563eb;
        }
        .search-link {
            display: inline-block;
            background: #2563eb;
            color: white;
            padding: 8px 16px;
            border-radius: 5px;
            text-decoration: none;
            margin: 5px;
            font-size: 14px;
            transition: background 0.3s;
        }
        .search-link:hover {
            background: #1e40af;
        }
        .note {
            background: #fef3c7;
            border-left: 4px solid #f59e0b;
            padding: 15px;
            margin: 20px 0;
            border-radius: 5px;
        }
        .warning {
            background: #fee2e2;
            border-left: 4px solid #ef4444;
            padding: 15px;
            margin: 20px 0;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <h1>🔍 Baidu Image Search - Chinese Cities</h1>
    
    <div class="note">
        <strong>📝 Note:</strong> Baidu Image Search works best from within China. 
        You may need a VPN with Chinese IP address to access it properly.
    </div>
    
    <div class="warning">
        <strong>⚠️ Important:</strong> Check image licenses before commercial use. 
        Some images on Baidu may be copyrighted.
    </div>
    
    <h2>🏙️ Search for City Images</h2>
    <p>Click the links below to search for authentic Chinese city images on Baidu.</p>
"""
    
    # Add city sections
    for city_name, queries in CITY_CHINESE_QUERIES.items():
        html_content += f"""
    <div class="city-card">
        <h3>{city_name}</h3>
        <p><strong>Primary Search:</strong> {queries[0]}</p>
        <a class="search-link" href="{generate_baidu_search_url(queries[0])}" target="_blank">
            🔍 Search on Baidu
        </a>
        <a class="search-link" href="{generate_baidu_search_url(queries[0], '风景')}" target="_blank">
            🏞️ Scenery
        </a>
        <a class="search-link" href="{generate_baidu_search_url(queries[0], '建筑')}" target="_blank">
            🏛️ Architecture
        </a>
        <a class="search-link" href="{generate_baidu_search_url(queries[0], '夜景')}" target="_blank">
            🌃 Night View
        </a>
        
        <p><strong>Alternative searches:</strong></p>
        <ul>
"""
        
        for query in queries[1:]:
            html_content += f'            <li>{query}</li>\n'
        
        html_content += """        </ul>
    </div>
"""
    
    # Add footer
    html_content += """
    <h2>📋 How to Use</h2>
    <div class="city-card">
        <h3>Downloading Images</h3>
        <ol>
            <li>Click any search link above</li>
            <li>On Baidu page, find an image you like</li>
            <li>Right-click the image → "图片另存为" (Save image as)</li>
            <li>Choose high-resolution images (1920x1080 or larger)</li>
        </ol>
        
        <h3>Filtering Options on Baidu</h3>
        <ul>
            <li><strong>尺寸 (Size):</strong> 选择 "大尺寸" for large images</li>
            <li><strong>颜色 (Color):</strong> Filter by color if needed</li>
            <li><strong>类型 (Type):</strong> 照片 (photo), 插画 (illustration), etc.</li>
        </ul>
        
        <h3>Legal Considerations</h3>
        <ul>
            <li>Check image licenses before commercial use</li>
            <li>Some images may require attribution</li>
            <li>Consider using official tourism board images</li>
        </ul>
    </div>
    
    <div class="note">
        <p><strong>💡 Tip:</strong> For the best authentic images, also check:</p>
        <ul>
            <li>Official city tourism websites</li>
            <li>Chinese photography websites (like 图虫, 500px中国版)</li>
            <li>Travel blogs by Chinese photographers</li>
        </ul>
    </div>
    
    <footer>
        <p>Generated by Baidu Image Search Assistant • Last updated: 2026-02-07</p>
    </footer>
</body>
</html>"""
    
    # Write HTML file
    with open('baidu_image_search.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return 'baidu_image_search.html'

def main():
    """Main function to generate Baidu search assistance."""
    
    print("🔍 Baidu Image Search Assistant")
    print("=" * 50)
    
    # Generate console report
    generate_search_report()
    
    # Create HTML page
    html_file = create_html_search_page()
    
    print("\n" + "=" * 70)
    print("📄 HTML SEARCH PAGE CREATED")
    print("=" * 70)
    print(f"\n✅ Created: {html_file}")
    print("   Open this file in your browser to access all Baidu search links")
    
    print("\n🎯 Immediate Actions:")
    print("1. Open baidu_image_search.html in your browser")
    print("2. Click any search link (requires China access/VPN)")
    print("3. Download high-quality images for your website")
    print("4. Update your city pages with authentic Chinese images")
    
    print("\n⚠️  Important Notes:")
    print("• Baidu may require solving captchas")
    print("• Check image licenses before commercial use")
    print("• Some images may have watermarks")

if __name__ == "__main__":
    main()