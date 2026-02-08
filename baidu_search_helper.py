#!/usr/bin/env python3
"""
Baidu Search Helper - Run this on your local machine to assist with Baidu image searches.
This script helps you organize and track your Baidu image searches.
"""

import json
import os
import webbrowser
from datetime import datetime

class BaiduSearchHelper:
    def __init__(self):
        self.search_data = self.load_search_data()
        self.image_folder = "downloaded_baidu_images"
        
        # Create image folder if it doesn't exist
        if not os.path.exists(self.image_folder):
            os.makedirs(self.image_folder)
            print(f"📁 Created folder: {self.image_folder}")
    
    def load_search_data(self):
        """Load search data from JSON file."""
        try:
            with open('baidu_image_replacements.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print("❌ baidu_image_replacements.json not found!")
            print("   Run setup_baidu_images.py first")
            return None
    
    def show_city_menu(self):
        """Show menu of cities to search for."""
        if not self.search_data:
            return
        
        print("\n" + "=" * 60)
        print("🏙️  SELECT CITY TO SEARCH")
        print("=" * 60)
        
        cities = list(self.search_data['cities'].keys())
        for i, city in enumerate(cities, 1):
            status = "🔍" if self.search_data['cities'][city]['baidu_replacement'] == 'REPLACE_WITH_BAIDU_IMAGE_URL' else "✅"
            print(f"{i}. {status} {city}")
        
        print(f"\n{len(cities)+1}. 🔄 Search ALL cities")
        print(f"{len(cities)+2}. 📊 Show search progress")
        print(f"{len(cities)+3}. 🚪 Exit")
        
        return cities
    
    def open_baidu_search(self, city_name):
        """Open Baidu search for a city in browser."""
        if city_name not in self.search_data['cities']:
            print(f"❌ City '{city_name}' not found!")
            return
        
        city_data = self.search_data['cities'][city_name]
        
        print(f"\n🔍 Searching for: {city_name}")
        print(f"   Description: {city_data['description']}")
        print(f"   Search queries: {', '.join(city_data['search_queries'])}")
        
        # Create search URLs
        base_url = "https://image.baidu.com/search/index?tn=baiduimage&word="
        
        print("\n📎 Search URLs (copy and paste into browser):")
        for query in city_data['search_queries']:
            # URL encode the query
            encoded_query = query.replace(' ', '%20')
            url = f"{base_url}{encoded_query}"
            print(f"   • {query}: {url}")
        
        # Try to open in browser
        try:
            first_query = city_data['search_queries'][0]
            encoded_query = first_query.replace(' ', '%20')
            url = f"{base_url}{encoded_query}"
            
            print(f"\n🌐 Opening browser with: {first_query}")
            webbrowser.open(url)
            
            # Log the search
            self.log_search(city_name, url)
            
        except Exception as e:
            print(f"⚠️  Could not open browser automatically: {e}")
            print("   Please copy and paste the URLs above into your browser")
    
    def log_search(self, city_name, url):
        """Log search activity."""
        log_file = "baidu_search_log.txt"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] Searched: {city_name} - {url}\n")
        
        print(f"📝 Logged search to: {log_file}")
    
    def show_progress(self):
        """Show search and download progress."""
        if not self.search_data:
            return
        
        print("\n" + "=" * 60)
        print("📊 SEARCH PROGRESS")
        print("=" * 60)
        
        total = len(self.search_data['cities'])
        completed = 0
        pending = 0
        
        for city, data in self.search_data['cities'].items():
            if data['baidu_replacement'] == 'REPLACE_WITH_BAIDU_IMAGE_URL':
                status = "🔍 Pending"
                pending += 1
            else:
                status = "✅ Completed"
                completed += 1
            
            print(f"{city:<12} - {status}")
        
        print(f"\n📈 Progress: {completed}/{total} cities ({completed/total*100:.1f}%)")
        
        # Check downloaded images
        if os.path.exists(self.image_folder):
            image_files = [f for f in os.listdir(self.image_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
            print(f"📁 Downloaded images: {len(image_files)} files in '{self.image_folder}'")
    
    def update_image_url(self, city_name, image_url):
        """Update a city's image URL in the JSON file."""
        if city_name not in self.search_data['cities']:
            print(f"❌ City '{city_name}' not found!")
            return
        
        self.search_data['cities'][city_name]['baidu_replacement'] = image_url
        
        with open('baidu_image_replacements.json', 'w', encoding='utf-8') as f:
            json.dump(self.search_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Updated {city_name} with new image URL")
        print(f"   URL: {image_url}")
    
    def run(self):
        """Main interactive loop."""
        if not self.search_data:
            print("❌ Cannot run without search data.")
            print("   Make sure baidu_image_replacements.json exists.")
            return
        
        print("=" * 60)
        print("🔍 BAIDU IMAGE SEARCH HELPER")
        print("=" * 60)
        print("\nThis tool helps you search Baidu for authentic Chinese city images.")
        print("It will open search links in your browser and help track progress.")
        
        while True:
            cities = self.show_city_menu()
            if not cities:
                break
            
            try:
                choice = input("\n📝 Enter your choice (1-{}): ".format(len(cities) + 3))
                
                if choice == str(len(cities) + 1):  # Search ALL
                    print("\n🔍 Opening searches for ALL cities...")
                    for city in cities:
                        if self.search_data['cities'][city]['baidu_replacement'] == 'REPLACE_WITH_BAIDU_IMAGE_URL':
                            self.open_baidu_search(city)
                            input(f"\n⏸️  Press Enter to continue to next city...")
                
                elif choice == str(len(cities) + 2):  # Show progress
                    self.show_progress()
                
                elif choice == str(len(cities) + 3):  # Exit
                    print("\n👋 Goodbye! Happy image searching!")
                    break
                
                elif 1 <= int(choice) <= len(cities):  # Specific city
                    city_index = int(choice) - 1
                    city_name = cities[city_index]
                    self.open_baidu_search(city_name)
                    
                    # Ask if they want to update image URL
                    update = input(f"\n📝 Did you find an image for {city_name}? (y/n): ").lower()
                    if update == 'y':
                        image_url = input("   Enter image URL: ").strip()
                        if image_url:
                            self.update_image_url(city_name, image_url)
                
                else:
                    print("❌ Invalid choice. Please try again.")
            
            except ValueError:
                print("❌ Please enter a valid number.")
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break

def main():
    """Main function."""
    helper = BaiduSearchHelper()
    helper.run()
    
    print("\n" + "=" * 60)
    print("🎯 NEXT STEPS")
    print("=" * 60)
    print("\nAfter searching and updating image URLs:")
    print("1. Run: python3 update_with_baidu.py")
    print("2. Check your website for updated images")
    print("3. Repeat for remaining cities")
    
    print("\n💡 Tip: Start with 1 city (Beijing) to test the workflow!")

if __name__ == "__main__":
    main()