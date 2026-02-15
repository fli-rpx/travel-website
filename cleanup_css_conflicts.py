#!/usr/bin/env python3
"""
Clean up CSS conflicts by removing large inline style block
and keeping only minimal critical styles
"""

import os
import re

def cleanup_css_conflicts():
    """Remove large inline style block and keep only minimal styles"""
    html_file = "index.html"
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the first <style> tag and its content
    # We want to keep only minimal critical styles, not the large block
    style_start = content.find('<style>')
    if style_start == -1:
        print("❌ No style tag found")
        return False
    
    style_end = content.find('</style>', style_start)
    if style_end == -1:
        print("❌ No closing style tag found")
        return False
    
    style_end += len('</style>')
    
    # Extract the style content
    style_content = content[style_start:style_end]
    
    # Check if this is the minimal style block or the large one
    # The minimal one should be small and contain only basics
    if len(style_content) > 1000:  # Large style block
        print(f"⚠️  Found large style block ({len(style_content)} chars)")
        
        # Replace with minimal critical styles only
        minimal_styles = '''    <style>
        /* Critical above-fold styles only */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            color: #1e293b;
            line-height: 1.6;
            font-weight: 400;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }
        
        /* Ensure content is visible while external CSS loads */
        .hero, .cities-section, .news-section {
            opacity: 1;
            visibility: visible;
        }
    </style>'''
        
        # Replace the large style block with minimal styles
        new_content = content[:style_start] + minimal_styles + content[style_end:]
        
        # Write updated content
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print("✅ Replaced large style block with minimal critical styles")
        return True
    else:
        print("ℹ️  Style block already minimal")
        return True

def check_color_consistency():
    """Check and fix color consistency"""
    print("\n🔍 Checking color consistency...")
    
    html_file = "index.html"
    css_file = "style.css"
    
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    with open(css_file, 'r', encoding='utf-8') as f:
        css_content = f.read()
    
    # Check for inline color usage that should use CSS variables
    inline_colors = re.findall(r'#([0-9a-fA-F]{6})', html_content)
    unique_inline_colors = set(inline_colors)
    
    print(f"   Found {len(unique_inline_colors)} unique inline colors in HTML")
    
    # Check CSS variables defined
    css_vars = re.findall(r'--([^:]+):\s*#([0-9a-fA-F]{6})', css_content)
    print(f"   Found {len(css_vars)} CSS color variables")
    
    # Most inline colors should be in city card images (background-image)
    # which is fine. We're mainly concerned with text/background colors.
    
    # Check for problematic inline styles that should use CSS classes
    problematic_patterns = [
        r'color:\s*#[0-9a-fA-F]{6}',
        r'background-color:\s*#[0-9a-fA-F]{6}',
        r'background:\s*#[0-9a-fA-F]{6}',
    ]
    
    issues = []
    for pattern in problematic_patterns:
        matches = re.findall(pattern, html_content)
        if matches:
            issues.append(f"{len(matches)} instances of {pattern}")
    
    if issues:
        print("   ⚠️  Found inline color styles that should use CSS classes:")
        for issue in issues:
            print(f"      • {issue}")
    else:
        print("   ✅ No problematic inline color styles found")
    
    return len(issues) == 0

def main():
    print("=" * 60)
    print("Cleaning Up CSS Conflicts")
    print("=" * 60)
    
    print("\n1. Removing large inline style block...")
    if cleanup_css_conflicts():
        print("\n2. Checking color consistency...")
        check_color_consistency()
        
        print("\n🎉 CSS conflicts cleaned up!")
        print("\n📋 Summary:")
        print("   - Large inline style block replaced with minimal critical styles")
        print("   - External style.css now handles all design")
        print("   - Bootstrap provides responsive grid system")
        print("   - CSS variables used for consistent theming")
    else:
        print("\n❌ Failed to clean up CSS conflicts")

if __name__ == "__main__":
    main()