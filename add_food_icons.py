#!/usr/bin/env python3
"""
Script to add food_icon URL to each city JSON file
"""

import json
import os

# Food icons mapping
food_icons = {
    'beijing': 'https://kimi-web-img.moonshot.cn/img/media.istockphoto.com/f85a35c490a0365984f5cae797a7b97baf1c12d9.jpg',
    'shanghai': 'https://kimi-web-img.moonshot.cn/img/res.cloudinary.com/cba8e20ff85d2079666043972be31a3e21c558f0',
    'guangzhou': 'https://kimi-web-img.moonshot.cn/img/global.gcdn.top/a2fc4a87a659bd32ba3a8668ff07b656abdedf08.png',
    'shenzhen': 'https://kimi-web-img.moonshot.cn/img/thumbs.dreamstime.com/a46896599053ccf6a41c92f6478461057552ae08.jpg',
    'chengdu': 'https://kimi-web-img.moonshot.cn/img/png.pngtree.com/eb17d663950cef01201995f92b5acc7129edc699.png',
    'hangzhou': 'https://kimi-web-img.moonshot.cn/img/static.vecteezy.com/22d926968c143cc9eda53eaa63628d4388e1cba5.JPG',
    'wuhan': 'https://kimi-web-img.moonshot.cn/img/img08.weeecdn.net/18815de2c5a2e2d6f9f9533005b63a310387a82a.auto',
    'xian': 'https://kimi-web-img.moonshot.cn/img/blog.themalamarket.com/bf8adcb9bbadcb127de7b96d7df39af86fc11a12.jpg',
    'nanjing': 'https://kimi-web-img.moonshot.cn/img/img08.weeecdn.net/60fd9787c6cc569593d8707076368f3942b88730.auto',
    'chongqing': 'https://kimi-web-img.moonshot.cn/img/www.sichuantravelguide.com/0601534cc99d48c9203e76fafccfbe20769dcbfd.jpg',
    'tianjin': 'https://kimi-web-img.moonshot.cn/img/cdn.tasteatlas.com/4a70974c49034ffa3d90ad77d4f51fe482f8a3a0.jpg',
    'suzhou': 'https://kimi-web-img.moonshot.cn/img/png.pngtree.com/24f2aeafbd2dbffe1680fcff0daef6d1f3164cbf.jpg',
    'qingdao': 'https://kimi-web-img.moonshot.cn/img/steemitimages.com/071b2d6450277250af4f7aa77525af1f6c412be0.jpg',
    'harbin': 'https://kimi-web-img.moonshot.cn/img/upload.wikimedia.org/f7ca13b9da6dfe9fa8fb6ce5d61d435c8ad432a5.jpg',
    'hongkong': 'https://kimi-web-img.moonshot.cn/img/cdn.coconuts.co/b5b526a9ce89aaadeb71765f08313e697dce2581.jpg',
    'kunming': 'https://kimi-web-img.moonshot.cn/img/www.topchinatravel.com/733c3a77c29d86c14a51997cf7050e6aa8fdcb45.JPG',
    'xiamen': 'https://kimi-web-img.moonshot.cn/img/thewoksoflife.com/31740f440a658cfba93fad42c441a669bd9cc815.jpg',
    'dali': 'https://kimi-web-img.moonshot.cn/img/s.alicdn.com/5acb1d3ba632b05587e81fcf96dc1d6783d35368.jpg',
    'datong': 'https://kimi-web-img.moonshot.cn/img/www.chinaeducationaltours.com/d0387b656343bc76f740501b965d69c50b74c745.jpg',
    'guilin': 'https://kimi-web-img.moonshot.cn/img/ik.imagekit.io/50004b7895d40e8b100cb85e79359f3fa726f910.png',
    'guiyang': 'https://kimi-web-img.moonshot.cn/img/lvyinfood.com/22973b03d2dd5f1a8d634d7c358eba2b0948ab2e.png',
    'jinan': 'https://kimi-web-img.moonshot.cn/img/subsites.chinadaily.com.cn/3dbb7dd5ef71e21179d62fdd32aab5f49995023d.jpg',
    'kaifeng': 'https://kimi-web-img.moonshot.cn/img/www.shutterstock.com/2ced93624c861ef5983251a7c802db3f14407969.jpg',
    'kashi': 'https://kimi-web-img.moonshot.cn/img/phototravelasia.com/af278f498e7b0f8beedb11150da0aab0eade423f.jpg',
    'linyi': 'https://kimi-web-img.moonshot.cn/img/www.xindb.com/f57c18ae873ade31fe7688d3fa0b57f979c9d015.jpg',
    'taiyuan': 'https://kimi-web-img.moonshot.cn/img/www.chinaeducationaltours.com/dc4bbe4dea12b43732d92a8bb13401f9ad609582.jpg',
    'urumqi': 'https://kimi-web-img.moonshot.cn/img/cdn.shopify.com/f8b49da32883be260c7b921ff7ba309684dbda81.jpg',
    'wuxi': 'https://kimi-web-img.moonshot.cn/img/cdn-akamai.lkk.com/43126db2f94f41e1ac0a5afb3b2fcc5d04521171.jpg'
}

# Update each city JSON file
data_dir = '/root/.openclaw/workspace/travel-website/data'

cities = [
    'beijing', 'shanghai', 'guangzhou', 'shenzhen', 'chengdu', 'hangzhou', 'wuhan', 'xian',
    'nanjing', 'chongqing', 'tianjin', 'suzhou', 'qingdao', 'harbin', 'hongkong', 'kunming',
    'xiamen', 'dali', 'datong', 'guilin', 'guiyang', 'jinan', 'kaifeng', 'kashi', 'linyi',
    'taiyuan', 'urumqi', 'wuxi'
]

for city in cities:
    json_file = os.path.join(data_dir, f'{city}.json')
    if os.path.exists(json_file):
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Add food_icon to cuisine section
        if 'cuisine' not in data:
            data['cuisine'] = {}
        
        data['cuisine']['food_icon'] = food_icons.get(city, '')
        
        # Write back
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"Added food_icon to {city}.json")
    else:
        print(f"File not found: {json_file}")

print("\nAll cities updated with food_icon!")
