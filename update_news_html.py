#!/usr/bin/env python3
"""
Script to update travel news directly in index.html
"""

import re
import os
from datetime import datetime, timedelta

# Sample travel news database
TRAVEL_NEWS_POOL = [
    {
        "title": "China Expands Visa-Free Transit to 240 Hours",
        "excerpt": "Foreign travelers can now enjoy visa-free stays up to 10 days in 60+ cities across China, making multi-city tours easier than ever."
    },
    {
        "title": "New Direct Flights Connect US and China",
        "excerpt": "Major airlines announce new direct routes between Los Angeles, New York and Beijing, Shanghai with increased weekly frequency."
    },
    {
        "title": "Spring Festival Travel Sets New Records",
        "excerpt": "Over 9 billion trips made during Chinese New Year 2026, with tourism revenue up 15% compared to last year."
    },
    {
        "title": "High-Speed Rail Adds New Routes to Western China",
        "excerpt": "New connections to Chengdu, Xi'an, and Urumqi make exploring western China faster and more convenient for tourists."
    },
    {
        "title": "UNESCO Adds Three New Chinese Heritage Sites",
        "excerpt": "Ancient tea routes, traditional villages, and cultural landscapes receive world heritage status, boosting tourism appeal."
    },
    {
        "title": "Digital Yuan Now Accepted at Major Tourist Sites",
        "excerpt": "International visitors can now use China's digital currency at the Forbidden City, Great Wall, and other attractions."
    },
    {
        "title": "New Airport Opens in Southwest China",
        "excerpt": "Chengdu Tianfu International Airport opens with direct flights to Europe, America, and Asia, easing access to Sichuan and Yunnan."
    },
    {
        "title": "China Launches 'Night Tourism' Initiative",
        "excerpt": "Extended hours at major attractions, night markets, and cultural performances aim to boost evening tourism economy."
    },
    {
        "title": "Eco-Tourism Booms in Rural China",
        "excerpt": "Sustainable travel options expand with new eco-lodges, farm stays, and conservation programs in picturesque villages."
    },
    {
        "title": "AI-Powered Translation Services Launch at Airports",
        "excerpt": "Real-time translation kiosks and apps help international travelers navigate Chinese airports and train stations with ease."
    },
    {
        "title": "Panda Sanctuaries Expand Visitor Programs",
        "excerpt": "Chengdu and Wolong panda bases offer new volunteer programs and behind-the-scenes experiences for wildlife enthusiasts."
    },
    {
        "title": "Ancient Silk Road Routes Revived for Tourism",
        "excerpt": "New guided tours follow historic trade routes through Xinjiang, Gansu, and Shaanxi with authentic cultural experiences."
    },
    {
        "title": "Chinese Cuisine Tours Gain Popularity",
        "excerpt": "Food-focused itineraries highlighting regional specialties from Sichuan spice to Cantonese dim sum attract culinary tourists."
    },
    {
        "title": "Winter Sports Tourism Surges in Northeast China",
        "excerpt": "Harbin Ice Festival and new ski resorts in Heilongjiang draw record numbers of domestic and international visitors."
    },
    {
        "title": "Smart Hotels Transform Chinese Hospitality",
        "excerpt": "AI concierge, facial recognition check-in, and robot services become standard at new hotels in major tourist cities."
    }
]

def update_travel_news_html():
    """Update travel news directly in index.html"""
    
    html_file = '/root/.openclaw/workspace/travel-website/index.html'
    
    # Get today's date
    today = datetime.now()
    
    # Select 3 news items based on day of month (rotating)
    day_offset = today.day % len(TRAVEL_NEWS_POOL)
    selected_news = []
    
    for i in range(3):
        idx = (day_offset + i) % len(TRAVEL_NEWS_POOL)
        news_item = TRAVEL_NEWS_POOL[idx].copy()
        # Set date (today, yesterday, day before)
        news_date = today - timedelta(days=i)
        news_item['date'] = news_date.strftime('%b %d, %Y')
        selected_news.append(news_item)
    
    # Read current HTML
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Build new news section HTML
    news_html = '''    <!-- NEWS SECTION -->
    <section id="news" class="news-section">
        <div class="container">
            <h2 class="section-title">Latest Travel News</h2>
            <div id="news-grid" class="news-grid">
                <div class="news-card">
                    <div class="news-date">{date0}</div>
                    <h3 class="news-title">{title0}</h3>
                    <p class="news-excerpt">{excerpt0}</p>
                    <a href="#" class="news-link">Read more →</a>
                </div>
                
                <div class="news-card">
                    <div class="news-date">{date1}</div>
                    <h3 class="news-title">{title1}</h3>
                    <p class="news-excerpt">{excerpt1}</p>
                    <a href="#" class="news-link">Read more →</a>
                </div>
                
                <div class="news-card">
                    <div class="news-date">{date2}</div>
                    <h3 class="news-title">{title2}</h3>
                    <p class="news-excerpt">{excerpt2}</p>
                    <a href="#" class="news-link">Read more →</a>
                </div>
            </div>
        </div>
    </section>'''.format(
        date0=selected_news[0]['date'],
        title0=selected_news[0]['title'],
        excerpt0=selected_news[0]['excerpt'],
        date1=selected_news[1]['date'],
        title1=selected_news[1]['title'],
        excerpt1=selected_news[1]['excerpt'],
        date2=selected_news[2]['date'],
        title2=selected_news[2]['title'],
        excerpt2=selected_news[2]['excerpt']
    )
    
    # Replace old news section with new one
    pattern = r'<!-- NEWS SECTION -->.*?<!-- CONTACT SECTION -->'
    replacement = news_html + '''
    
    <!-- CONTACT SECTION -->'''
    
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    # Save updated HTML
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Updated travel news in index.html for {today.strftime('%Y-%m-%d')}")
    print(f"Selected news items:")
    for item in selected_news:
        print(f"  - {item['date']}: {item['title']}")

if __name__ == '__main__':
    update_travel_news_html()
