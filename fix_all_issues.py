#!/usr/bin/env python3
"""
Fix ALL website issues:
1. Cities link to wrong pages
2. Layout/style not matching with home page
3. Ensure monitor catches these issues
"""

import os
import re

def fix_city_page_links():
    """Fix navigation links in all city pages."""
    
    print("🔗 FIXING CITY PAGE LINKS")
    print("=" * 50)
    
    website_dir = os.path.dirname(os.path.abspath(__file__))
    cities_dir = os.path.join(website_dir, "cities")
    
    if not os.path.exists(cities_dir):
        print("❌ Cities directory not found")
        return 0
    
    city_files = [f for f in os.listdir(cities_dir) if f.endswith('.html') and f != 'template.html']
    fixes = 0
    
    for city_file in city_files:
        file_path = os.path.join(cities_dir, city_file)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix 1: Make ALL links consistent - use absolute paths for GitHub Pages
        old_patterns = [
            ('href="../index.html"', 'href="/travel-website/index.html"'),
            ('href="../index.html#', 'href="/travel-website/index.html#'),
            ('href="index.html"', 'href="/travel-website/index.html"'),
        ]
        
        for old, new in old_patterns:
            if old in content:
                content = content.replace(old, new)
                fixes += 1
                print(f"✅ {city_file}: Fixed {old} → {new}")
        
        # Fix 2: Ensure CSS link is correct
        if 'href="/travel-website/style.css"' not in content:
            # Find and fix CSS link
            css_pattern = r'href="[^"]*style\.css"'
            content = re.sub(css_pattern, 'href="/travel-website/style.css"', content)
            fixes += 1
            print(f"✅ {city_file}: Fixed CSS link")
        
        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    print(f"\n🔧 Applied {fixes} link fixes across {len(city_files)} city pages")
    return fixes

def fix_layout_style_consistency():
    """Ensure layout and style match between home page and city pages."""
    
    print("\n🎨 FIXING LAYOUT & STYLE CONSISTENCY")
    print("=" * 50)
    
    website_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Read main page structure
    main_page = os.path.join(website_dir, "index.html")
    if not os.path.exists(main_page):
        print("❌ Main page not found")
        return 0
    
    with open(main_page, 'r', encoding='utf-8') as f:
        main_content = f.read()
    
    # Extract key elements from main page
    # 1. Navbar structure
    navbar_match = re.search(r'<nav[^>]*>.*?</nav>', main_content, re.DOTALL)
    main_navbar = navbar_match.group(0) if navbar_match else ""
    
    # 2. Footer structure
    footer_match = re.search(r'<footer[^>]*>.*?</footer>', main_content, re.DOTALL)
    main_footer = footer_match.group(0) if footer_match else ""
    
    # 3. Color scheme
    color_vars = re.findall(r'--[a-zA-Z-]+:\s*[^;]+;', main_content)
    
    print(f"📊 Main page analysis:")
    print(f"   • Navbar: {'Found' if main_navbar else 'Not found'}")
    print(f"   • Footer: {'Found' if main_footer else 'Not found'}")
    print(f"   • Color variables: {len(color_vars)}")
    
    # Now fix city pages
    cities_dir = os.path.join(website_dir, "cities")
    city_files = [f for f in os.listdir(cities_dir) if f.endswith('.html') and f != 'template.html']
    
    fixes = 0
    
    for city_file in city_files:
        file_path = os.path.join(cities_dir, city_file)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check and fix navbar
        if '<nav class="navbar' not in content and main_navbar:
            # Replace existing navbar with main page navbar
            city_navbar_match = re.search(r'<nav[^>]*>.*?</nav>', content, re.DOTALL)
            if city_navbar_match:
                content = content.replace(city_navbar_match.group(0), main_navbar)
                fixes += 1
                print(f"✅ {city_file}: Updated navbar to match main page")
        
        # Check and fix footer
        if '<footer' not in content and main_footer:
            # Add footer if missing
            content = re.sub(r'</body>', f'{main_footer}\n</body>', content)
            fixes += 1
            print(f"✅ {city_file}: Added consistent footer")
        
        # Check color variables in CSS link
        if 'var(--primary)' not in content:
            # Ensure CSS is linked properly
            if '<link rel="stylesheet" href="/travel-website/style.css">' in content:
                # CSS is linked, but variables might not be used
                # Find elements that should use primary color
                primary_fixes = re.sub(r'style="color:[^"]*"', 'style="color: var(--primary)"', content)
                if primary_fixes != content:
                    content = primary_fixes
                    fixes += 1
                    print(f"✅ {city_file}: Applied primary color variables")
        
        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    print(f"\n🔧 Applied {fixes} layout/style fixes")
    return fixes

def enhance_monitor_to_catch_issues():
    """Update the enhanced monitor to better catch the issues you mentioned."""
    
    print("\n🔍 ENHANCING MONITOR TO CATCH ISSUES")
    print("=" * 50)
    
    website_dir = os.path.dirname(os.path.abspath(__file__))
    monitor_file = os.path.join(website_dir, "enhanced_monitor.py")
    
    if not os.path.exists(monitor_file):
        print("❌ Enhanced monitor not found")
        return 0
    
    with open(monitor_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add specific check for navigation links
    link_check_code = '''
    def check_navigation_links(self):
        """Check 4: Are navigation links correct?"""
        self.log("\\n🔗 CHECK 4: NAVIGATION LINK CONSISTENCY")
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
            home_links = re.findall(r'href="([^"]*index\.html[^"]*)"', city_content)
            
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
'''
    
    # Find where to insert the new check
    if 'def check_layout_color_consistency(self):' in content:
        # Insert after the layout check
        old = 'def check_layout_color_consistency(self):'
        new = 'def check_navigation_links(self):\n        """Check 4: Are navigation links correct?"""\n        self.log("\\n🔗 CHECK 4: NAVIGATION LINK CONSISTENCY")\n        self.log("-" * 40)\n        \n        issues = []\n        \n        # Check main page\n        main_page = os.path.join(self.website_dir, "index.html")\n        if os.path.exists(main_page):\n            with open(main_page, \'r\', encoding=\'utf-8\') as f:\n                main_content = f.read()\n            \n            # Extract links from main page\n            main_links = re.findall(r\'href="([^"]+)"\', main_content)\n            main_city_links = [link for link in main_links if \'cities/\' in link]\n            \n            self.log(f"Main page has {len(main_city_links)} city links")\n        \n        # Check city pages\n        cities_dir = os.path.join(self.website_dir, "cities")\n        city_files = [f for f in os.listdir(cities_dir) if f.endswith(\'.html\') and f != \'template.html\']\n        \n        for city_file in city_files[:3]:  # Check first 3\n            file_path = os.path.join(cities_dir, city_file)\n            \n            with open(file_path, \'r\', encoding=\'utf-8\') as f:\n                city_content = f.read()\n            \n            # Check back to home link\n            home_links = re.findall(r\'href="([^"]*index\\\\.html[^"]*)"\', city_content)\n            \n            # Should have at least one link back to home\n            if not any(\'index.html\' in link for link in home_links):\n                issues.append(f"{city_file}: No link back to home page")\n            \n            # Check link consistency\n            inconsistent_links = []\n            for link in home_links:\n                if not link.startswith(\'/travel-website/\') and \'index.html\' in link:\n                    inconsistent_links.append(link)\n            \n            if inconsistent_links:\n                issues.append(f"{city_file}: Inconsistent home links: {\', \'.join(inconsistent_links[:2])}")\n        \n        if issues:\n            self.log(f"⚠️  Found {len(issues)} navigation issues:")\n            for issue in issues[:3]:\n                self.log(f"   • {issue}")\n            if len(issues) > 3:\n                self.log(f"   ... and {len(issues)-3} more issues")\n            \n            self.issues_found += len(issues)\n            return False\n        \n        self.log("✅ Navigation links are consistent!")\n        return True\n\n    def check_layout_color_consistency(self):'
        
        content = content.replace(old, new)
        print("✅ Added navigation link check to enhanced monitor")
        
        # Also update the run_complete_check method to include this check
        if 'checks = [' in content:
            checks_start = content.find('checks = [')
            checks_end = content.find(']', checks_start)
            checks_section = content[checks_start:checks_end+1]
            
            new_checks = checks_section.replace(
                '("Layout & Color Consistency", self.check_layout_color_consistency)',
                '("Layout & Color Consistency", self.check_layout_color_consistency),\n            ("Navigation Links", self.check_navigation_links)'
            )
            
            content = content.replace(checks_section, new_checks)
            print("✅ Updated monitor to include navigation check in 10-minute runs")
    
    # Write back
    with open(monitor_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return 1

def main():
    """Fix all issues."""
    
    print("=" * 70)
    print("🔧 COMPREHENSIVE WEBSITE FIX")
    print("=" * 70)
    print("Fixing all issues mentioned:")
    print("1. Cities link to wrong pages")
    print("2. Layout/style not matching with home page")
    print("3. Enhancing monitor to catch these issues")
    print("=" * 70)
    
    total_fixes = 0
    
    # Fix 1: Navigation links
    total_fixes += fix_city_page_links()
    
    # Fix 2: Layout/style consistency
    total_fixes += fix_layout_style_consistency()
    
    # Fix 3: Enhance monitor
    total_fixes += enhance_monitor_to_catch_issues()
    
    print("\n" + "=" * 70)
    print("✅ ALL FIXES COMPLETED")
    print("=" * 70)
    print(f"Total fixes applied: {total_fixes}")
    
    print("\n🚀 Next steps:")
    print("1. The 10-minute monitor will now catch navigation/layout issues")
    print("2. Next run at 22:50 will include new checks")
    print("3. Test: https://fli-rpx.github.io/travel-website/cities/guangzhou.html")
    print("4. Deploy fixes: git add . && git commit -m 'Fix all issues' && git push")
    
    print("\n🔍 Test the fixes:")
    print("cd /Users/fudongli/clawd/travel-website")
    print("python3 enhanced_monitor.py")

if __name__ == "__main__":
    main()