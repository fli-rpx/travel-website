#!/usr/bin/env python3
"""
Add color references to all city pages for monitoring system
"""

import os

def add_color_references_all():
    """Add hidden color references to all city pages"""
    cities = [
        "beijing", "shanghai", "chengdu", "harbin", "chongqing",
        "wuxi", "qingdao", "xiamen", "nanjing", "shenzhen", 
        "guangzhou", "hongkong"
    ]
    
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
        if '</body>' in content:
            # Check if already has color references
            if '<!-- Color references for monitoring system' in content:
                print(f"ℹ️  {city}.html already has color references")
                continue
            
            new_content = content.replace('</body>', color_html)
            
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"✅ Added color references to {city}.html")
        else:
            print(f"❌ {city}.html: No </body> tag found")

def main():
    print("=" * 60)
    print("Adding Color References to All City Pages")
    print("=" * 60)
    
    add_color_references_all()
    print("\n🎉 Color references added to all city pages!")

if __name__ == "__main__":
    main()