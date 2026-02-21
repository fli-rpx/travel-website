#!/usr/bin/env python3
"""
Script to update travel news daily - rotates which 3 news items show on homepage
"""

import json
import os
from datetime import datetime

# Update travel_news.json to rotate featured news
def update_featured_news():
    """Rotate which 3 news items appear first in the JSON"""
    
    data_dir = '/root/.openclaw/workspace/travel-website/data'
    news_file = os.path.join(data_dir, 'travel_news.json')
    
    # Load current news
    with open(news_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Rotate news items - move first 3 to end
    news = data['news']
    if len(news) > 3:
        # Rotate by day of month
        day_offset = datetime.now().day % (len(news) // 3)
        offset = day_offset * 3
        
        # Reorder: items from offset go first
        rotated = news[offset:] + news[:offset]
        data['news'] = rotated
    
    # Update timestamp
    data['last_updated'] = datetime.now().strftime('%Y-%m-%d')
    
    # Save
    with open(news_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Updated featured news for {datetime.now().strftime('%Y-%m-%d')}")
    print(f"Top 3 news items now:")
    for item in data['news'][:3]:
        print(f"  - {item['date']}: {item['title']}")

if __name__ == '__main__':
    update_featured_news()
