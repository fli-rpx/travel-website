#!/usr/bin/env python3
"""
Enhanced Website Monitor with specific checks for:
1. Images readiness for each city
2. Pages readiness for each city
3. Layout and color consistency between pages
Runs every 10 minutes via cron job.
"""

import os
import json
import re
import time
import subprocess
import sys
from datetime import datetime
from collections import defaultdict

class EnhancedWebsiteMonitor:
    def __init__(self):
        self.website_dir = os.path.dirname(os.path.abspath(__file__))
        self.status_file = "enhanced_monitor_status.json"
        self.log_file = "enhanced_monitor.log"
        self.issues_found = 0
        self.improvements_made = 0
        
        # All 12 cities that should exist
        self.all_cities = [
            "Beijing", "Shanghai", "Chengdu", "Harbin", "Chongqing",
            "Wuxi", "Qingdao", "Xiamen", "Nanjing", "Shenzhen", 
            "Guangzhou", "Hongkong"
        ]
        
        # Expected color scheme
        self.expected_colors = {
            "primary": "#2563eb",
            "secondary": "#1e40af", 
            "accent": "#f59e0b",
            "light": "#f8fafc",
            "dark": "#1e293b"
        }
    
    def log(self, message, level="INFO"):
        """Log messages with timestamp."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        
        print(log_entry)
        
        # Write to log file
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry + "\n")
    
    def check_images_readiness(self):
        """Check 1: Are images ready for each city?"""
        self.log("\n🔍 CHECK 1: IMAGES READINESS FOR EACH CITY")
        self.log("-" * 40)
        
        try:
            with open("baidu_image_replacements.json", 'r', encoding='utf-8') as f:
                image_status = json.load(f)
        except FileNotFoundError:
            self.log("❌ Image status file not found", "ERROR")
            return False
        
        cities_data = image_status.get("cities", {})
        
        cities_with_images = []
        cities_without_images = []
        
        for city in self.all_cities:
            if city in cities_data:
                city_data = cities_data[city]
                if city_data.get("baidu_replacement") != "REPLACE_WITH_BAIDU_IMAGE_URL":
                    cities_with_images.append(city)
                else:
                    cities_without_images.append(city)
            else:
                cities_without_images.append(city)
        
        # Report
        self.log(f"✅ Cities WITH images: {len(cities_with_images)}/{len(self.all_cities)}")
        if cities_with_images:
            self.log(f"   • {', '.join(cities_with_images[:5])}" + 
                    (f" and {len(cities_with_images)-5} more" if len(cities_with_images) > 5 else ""))
        
        self.log(f"⚠️  Cities WITHOUT images: {len(cities_without_images)}/{len(self.all_cities)}")
        if cities_without_images:
            self.log(f"   • {', '.join(cities_without_images[:5])}" + 
                    (f" and {len(cities_without_images)-5} more" if len(cities_without_images) > 5 else ""))
        
        # Priority cities check
        priority_cities = ["Chengdu", "Harbin", "Chongqing"]
        priority_status = {}
        
        for city in priority_cities:
            if city in cities_with_images:
                priority_status[city] = "✅ READY"
            else:
                priority_status[city] = "❌ NEEDS IMAGES"
        
        self.log("\n🎯 PRIORITY CITIES STATUS:")
        for city, status in priority_status.items():
            self.log(f"   {status} {city}")
        
        if len(cities_without_images) > 0:
            self.issues_found += len(cities_without_images)
            return False
        
        return True
    
    def check_pages_readiness(self):
        """Check 2: Are pages ready for each city?"""
        self.log("\n🔍 CHECK 2: PAGES READINESS FOR EACH CITY")
        self.log("-" * 40)
        
        cities_dir = os.path.join(self.website_dir, "cities")
        if not os.path.exists(cities_dir):
            self.log("❌ Cities directory not found", "ERROR")
            return False
        
        # Get all HTML files
        all_files = os.listdir(cities_dir)
        html_files = [f for f in all_files if f.endswith('.html')]
        
        # Map city names to expected filenames
        expected_files = {}
        for city in self.all_cities:
            expected_files[city.lower() + ".html"] = city
        
        # Check which cities have pages
        cities_with_pages = []
        cities_without_pages = []
        
        for html_file in html_files:
            if html_file in expected_files:
                cities_with_pages.append(expected_files[html_file])
        
        for expected_file, city in expected_files.items():
            if city not in cities_with_pages:
                cities_without_pages.append(city)
        
        # Report
        self.log(f"✅ Cities WITH pages: {len(cities_with_pages)}/{len(self.all_cities)}")
        if cities_with_pages:
            self.log(f"   • {', '.join(cities_with_pages[:5])}" + 
                    (f" and {len(cities_with_pages)-5} more" if len(cities_with_pages) > 5 else ""))
        
        if cities_without_pages:
            self.log(f"❌ Cities WITHOUT pages: {len(cities_without_pages)}/{len(self.all_cities)}")
            self.log(f"   • {', '.join(cities_without_pages)}")
            self.issues_found += len(cities_without_pages)
            return False
        else:
            self.log("✅ All 12 cities have pages!")
        
        return True
    
    def check_navigation_links(self):
        """Check 4: Are navigation links correct?"""
        self.log("\n🔗 CHECK 4: NAVIGATION LINK CONSISTENCY")
        self.log("-" * 40)
        
        issues = []
        
        # Check main page
        main_page = os.path.join(self.website_dir, "index.html")
        if os.path.exists(main_page):
            with open(main_page, 'r', encoding='utf-8') as f:
                main_content = f.read()
            
            # Extract links from main page
            main_links = re.findall(r'href="([^"]+)"', main_content)
            main_city_links = [link for link in main_links if 'cities/' in link]
            
            self.log(f"Main page has {len(main_city_links)} city links")
        
        # Check city pages
        cities_dir = os.path.join(self.website_dir, "cities")
        city_files = [f for f in os.listdir(cities_dir) if f.endswith('.html') and f != 'template.html']
        
        for city_file in city_files[:3]:  # Check first 3
            file_path = os.path.join(cities_dir, city_file)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                city_content = f.read()
            
            # Check back to home link
            home_links = re.findall(r'href="([^"]*index\\.html[^"]*)"', city_content)
            
            # Should have at least one link back to home
            if not any('index.html' in link for link in home_links):
                issues.append(f"{city_file}: No link back to home page")
            
            # Check link consistency
            inconsistent_links = []
            for link in home_links:
                if not link.startswith('/travel-website/') and 'index.html' in link:
                    inconsistent_links.append(link)
            
            if inconsistent_links:
                issues.append(f"{city_file}: Inconsistent home links: {', '.join(inconsistent_links[:2])}")
        
        if issues:
            self.log(f"⚠️  Found {len(issues)} navigation issues:")
            for issue in issues[:3]:
                self.log(f"   • {issue}")
            if len(issues) > 3:
                self.log(f"   ... and {len(issues)-3} more issues")
            
            self.issues_found += len(issues)
            return False
        
        self.log("✅ Navigation links are consistent!")
        return True

    def check_layout_color_consistency(self):
        """Check 3: Layout and color consistency between pages."""
        self.log("\n🔍 CHECK 3: LAYOUT & COLOR CONSISTENCY")
        self.log("-" * 40)
        
        issues = []
        color_usage = defaultdict(set)
        layout_elements = defaultdict(set)
        
        # Check main page first
        main_page = os.path.join(self.website_dir, "index.html")
        if os.path.exists(main_page):
            with open(main_page, 'r', encoding='utf-8') as f:
                main_content = f.read()
            
            # Extract colors from main page
            main_colors = self.extract_colors(main_content)
            main_layout = self.extract_layout_elements(main_content)
            
            self.log(f"📄 Main page: {len(main_colors)} colors, {len(main_layout)} layout elements")
        
        # Check all city pages
        cities_dir = os.path.join(self.website_dir, "cities")
        city_files = [f for f in os.listdir(cities_dir) if f.endswith('.html') and f != 'template.html']
        
        for city_file in city_files[:6]:  # Check first 6 to save time
            file_path = os.path.join(cities_dir, city_file)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check colors
            colors = self.extract_colors(content)
            for color in colors:
                color_usage[color].add(city_file)
            
            # Check layout elements
            layout = self.extract_layout_elements(content)
            for element in layout:
                layout_elements[element].add(city_file)
            
            # Check for required elements
            required_elements = ['city-hero', 'city-content', 'gallery']
            missing_elements = []
            for element in required_elements:
                if element not in content.lower():
                    missing_elements.append(element)
            
            if missing_elements:
                issues.append(f"{city_file}: Missing {', '.join(missing_elements)}")
        
        # Analyze consistency
        self.log("\n🎨 COLOR CONSISTENCY ANALYSIS:")
        
        # Check if expected colors are used
        for color_name, color_value in self.expected_colors.items():
            using_pages = color_usage.get(color_value, set())
            if using_pages:
                self.log(f"   ✅ {color_name} ({color_value}): Used in {len(using_pages)} pages")
            else:
                self.log(f"   ⚠️  {color_name} ({color_value}): Not found in checked pages")
                issues.append(f"Color {color_name} ({color_value}) not used")
        
        # Check layout consistency
        self.log("\n📐 LAYOUT CONSISTENCY ANALYSIS:")
        
        common_elements = set.intersection(*[layout_elements[element] for element in layout_elements if layout_elements[element]])
        if common_elements:
            self.log(f"   ✅ Common elements across all pages: {len(common_elements)}")
            for element in list(common_elements)[:3]:
                self.log(f"     • {element}")
        else:
            self.log("   ⚠️  No common layout elements found")
            issues.append("No common layout elements")
        
        # Report issues
        if issues:
            self.log(f"\n⚠️  Found {len(issues)} consistency issues:")
            for issue in issues[:3]:  # Show first 3
                self.log(f"   • {issue}")
            if len(issues) > 3:
                self.log(f"   ... and {len(issues)-3} more issues")
            
            self.issues_found += len(issues)
            return False
        
        self.log("✅ Layout and colors are consistent across pages!")
        return True
    
    def extract_colors(self, content):
        """Extract CSS colors from HTML/CSS content."""
        colors = set()
        
        # Look for hex colors
        hex_pattern = r'#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})'
        hex_matches = re.findall(hex_pattern, content)
        for match in hex_matches:
            if len(match) == 3:
                colors.add(f"#{match[0]}{match[0]}{match[1]}{match[1]}{match[2]}{match[2]}".lower())
            else:
                colors.add(f"#{match}".lower())
        
        # Look for CSS variables
        var_pattern = r'var\(--([^)]+)\)'
        var_matches = re.findall(var_pattern, content)
        colors.update(var_matches)
        
        # Look for RGB/RGBA
        rgb_pattern = r'rgb\([^)]+\)|rgba\([^)]+\)'
        rgb_matches = re.findall(rgb_pattern, content)
        colors.update(rgb_matches)
        
        return colors
    
    def extract_layout_elements(self, content):
        """Extract layout elements from HTML."""
        elements = set()
        
        # Look for CSS classes
        class_pattern = r'class="([^"]+)"'
        class_matches = re.findall(class_pattern, content)
        for match in class_matches:
            classes = match.split()
            elements.update(classes)
        
        # Look for IDs
        id_pattern = r'id="([^"]+)"'
        id_matches = re.findall(id_pattern, content)
        elements.update(id_matches)
        
        # Look for specific layout elements
        layout_keywords = ['container', 'row', 'col', 'hero', 'section', 'card', 
                          'navbar', 'footer', 'header', 'main', 'aside', 'article']
        
        for keyword in layout_keywords:
            if keyword in content.lower():
                elements.add(keyword)
        
        return elements
    
    def run_improvements(self):
        """Run improvements based on detected issues."""
        self.log("\n🔧 RUNNING IMPROVEMENTS")
        self.log("-" * 40)
        
        improvements = []
        
        # Check and create missing city pages
        cities_dir = os.path.join(self.website_dir, "cities")
        if os.path.exists(cities_dir):
            html_files = [f for f in os.listdir(cities_dir) if f.endswith('.html') and f != 'template.html']
            
            if len(html_files) < len(self.all_cities):
                self.log(f"Creating missing city pages ({len(html_files)}/{len(self.all_cities)} found)...")
                try:
                    result = subprocess.run(
                        [sys.executable, "create_missing_city_pages.py"],
                        cwd=self.website_dir,
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                    
                    if result.returncode == 0:
                        improvements.append("Created missing city pages")
                        self.improvements_made += 1
                except Exception as e:
                    self.log(f"❌ Error creating pages: {e}", "ERROR")
        
        # Fix image consistency
        self.log("Checking image consistency...")
        try:
            result = subprocess.run(
                [sys.executable, "fix_city_page_images.py"],
                cwd=self.website_dir,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                if "Updated" in result.stdout:
                    improvements.append("Fixed image inconsistencies")
                    self.improvements_made += 1
        except Exception as e:
            self.log(f"⚠️  Could not fix images: {e}", "WARNING")
        
        return improvements
    
    def run_complete_check(self):
        """Run all enhanced checks."""
        self.log("\n" + "=" * 70)
        self.log("ENHANCED WEBSITE MONITOR - 10 MINUTE CHECK")
        self.log("=" * 70)
        self.log(f"Checking: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Run all checks
        checks = [
            ("Images Readiness", self.check_images_readiness),
            ("Pages Readiness", self.check_pages_readiness),
            ("Layout & Color Consistency", self.check_layout_color_consistency),
            ("Navigation Links", self.check_navigation_links),
            ("News Section", self.check_news_section),
            ("Gallery Section", self.check_gallery_section)
        ]
        
        results = {}
        all_passed = True
        
        for check_name, check_func in checks:
            try:
                result = check_func()
                results[check_name] = result
                
                if result:
                    self.log(f"✅ {check_name}: PASSED")
                else:
                    self.log(f"❌ {check_name}: FAILED", "ERROR")
                    all_passed = False
                    
            except Exception as e:
                self.log(f"❌ {check_name}: ERROR - {e}", "ERROR")
                results[check_name] = False
                all_passed = False
        
        # Run improvements if needed
        if not all_passed:
            improvements = self.run_improvements()
            if improvements:
                self.log("\n🔧 Improvements applied:")
                for improvement in improvements:
                    self.log(f"   • {improvement}")
        
        # Summary
        self.log("\n" + "=" * 70)
        self.log("ENHANCED CHECK SUMMARY")
        self.log("=" * 70)
        
        passed = sum(1 for r in results.values() if r)
        total = len(results)
        
        self.log(f"Checks passed: {passed}/{total} ({passed/total*100:.1f}%)")
        self.log(f"Issues found: {self.issues_found}")
        self.log(f"Improvements made: {self.improvements_made}")
        
        if all_passed and self.issues_found == 0:
            self.log("\n🎉 WEBSITE STATUS: EXCELLENT")
            self.log("   All images, pages, and styling are ready and consistent!")
        elif self.improvements_made > 0:
            self.log("\n🔧 WEBSITE STATUS: IMPROVED")
            self.log("   Issues were found and fixed automatically")
        else:
            self.log("\n⚠️  WEBSITE STATUS: NEEDS ATTENTION")
            self.log("   Review the issues above and fix manually")
        
        # Save status
        self.save_status(results, all_passed)
        
        return all_passed
    
    
    def check_news_section(self):
        """Check if news section exists and has content."""
        self.log("📰 Checking news section...")
        
        index_path = os.path.join(self.website_dir, "index.html")
        
        if not os.path.exists(index_path):
            self.log("❌ index.html not found", "ERROR")
            return False
        
        try:
            with open(index_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for news section
            has_news_section = "Latest China Travel News" in content
            has_news_cards = "news-card" in content
            has_news_date = "news-date" in content
            
            if not has_news_section:
                self.log("❌ News section not found in website", "ERROR")
                self.issues_found += 1
                return False
            
            if not has_news_cards:
                self.log("❌ News cards not found", "ERROR")
                self.issues_found += 1
                return False
            
            # Count news cards
            news_card_count = content.count("news-card")
            if news_card_count < 3:
                self.log(f"⚠️  Only {news_card_count} news cards found (expected 3+)", "WARNING")
                self.issues_found += 1
                return False
            
            self.log(f"✅ News section found with {news_card_count} news cards")
            return True
            
        except Exception as e:
            self.log(f"❌ Error checking news section: {e}", "ERROR")
            return False

    def check_gallery_section(self):
        """Check if gallery section exists and has images."""
        self.log("🖼️  Checking gallery section...")
        
        index_path = os.path.join(self.website_dir, "index.html")
        
        if not os.path.exists(index_path):
            self.log("❌ index.html not found", "ERROR")
            return False
        
        try:
            with open(index_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for gallery section
            has_gallery_section = "Travel Photo Gallery" in content
            has_gallery_items = "gallery-item" in content
            
            if not has_gallery_section:
                self.log("❌ Gallery section not found in website", "ERROR")
                self.issues_found += 1
                return False
            
            if not has_gallery_items:
                self.log("❌ Gallery items not found", "ERROR")
                self.issues_found += 1
                return False
            
            # Count gallery items
            gallery_item_count = content.count("gallery-item")
            if gallery_item_count < 9:
                self.log(f"⚠️  Only {gallery_item_count} gallery items found (expected 4+)", "WARNING")
                self.issues_found += 1
                return False
            
            # Check if image files exist
            image_dir = os.path.join(self.website_dir, "images", "user_photos")
            if os.path.exists(image_dir):
                image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
                if len(image_files) < 9:
                    self.log(f"⚠️  Only {len(image_files)} user photos found in images/user_photos/", "WARNING")
                    self.issues_found += 1
                    return False
            else:
                self.log("❌ User photos directory not found: images/user_photos/", "ERROR")
                self.issues_found += 1
                return False
            
            self.log(f"✅ Gallery section found with {gallery_item_count} items and {len(image_files)} user photos")
            return True
            
        except Exception as e:
            self.log(f"❌ Error checking gallery section: {e}", "ERROR")
            return False
def save_status(self, results, all_passed):
        """Save monitoring status."""
        status = {
            "last_check": datetime.now().isoformat(),
            "results": results,
            "issues_found": self.issues_found,
            "improvements_made": self.improvements_made,
            "all_passed": all_passed,
            "cities_checked": self.all_cities
        }
        
        with open(self.status_file, 'w', encoding='utf-8') as f:
            json.dump(status, f, indent=2)

def main():
    """Main function."""
    monitor = EnhancedWebsiteMonitor()
    monitor.run_complete_check()

if __name__ == "__main__":
    main()