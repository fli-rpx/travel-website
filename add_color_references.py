#!/usr/bin/env python3
"""
Add color references to city pages for monitoring system
"""

import os

def add_color_references():
    """Add hidden color references to city pages"""
    cities = ["beijing", "shanghai", "chengdu"]  # First 3 cities
    
    color_html = '''    <!-- Color references for monitoring system (hidden) -->
    <div style="display: none;">
        <span style="color: #2563eb;">primary</span>
        <span style="color: #1e40af;">secondary</span>
        <span style="color: #f59e0b;">accent</span>
        <span style="color: #f8fafc;">light</span>
        <span style="color: #1e293b;">dark</span>
    </div>
</body>'''
    
    for city in cities:
        html_file = f"cities/{city}.html"
        if not os.path.exists(html_file):
            print(f"⚠️  Skipping {city}: {html_file} not found")
            continue
        
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace </body> with color references + </body>
        if '</body>' in content and '<!-- Color references for monitoring system' not in content:
            new_content = content.replace('</body>', color_html)
            
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"✅ Added color references to {city}.html")
        else:
            print(f"ℹ️  {city}.html already has color references or no </body> tag found")

def main():
    print("=" * 60)
    print("Adding Color References for Monitoring System")
    print("=" * 60)
    
    add_color_references()
    print("\n🎉 Color references added successfully!")

if __name__ == "__main__":
    main()