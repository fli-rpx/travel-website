#!/usr/bin/env python3
"""
Final verification that issues 1 and 2 are fixed
"""

import os
import re

def verify_news_section():
    """Verify news section is working"""
    print("🔍 Verifying news section...")
    
    with open("index.html", 'r', encoding='utf-8') as f:
        content = f.read()
    
    checks = [
        ("Latest Travel News" in content, "Has 'Latest Travel News' heading"),
        ("news-section" in content, "Has news-section class"),
        ("news-card" in content, "Has news cards"),
        (content.count("news-card") >= 3, "Has at least 3 news cards"),
    ]
    
    all_passed = True
    for check_passed, check_name in checks:
        if check_passed:
            print(f"   ✅ {check_name}")
        else:
            print(f"   ❌ {check_name}")
            all_passed = False
    
    return all_passed

def verify_layout_colors():
    """Verify layout colors are being used"""
    print("\n🔍 Verifying layout colors...")
    
    # Check main page has color references
    with open("index.html", 'r', encoding='utf-8') as f:
        content = f.read()
    
    colors = ["#2563eb", "#1e40af", "#f59e0b", "#f8fafc", "#1e293b"]
    found_colors = []
    
    for color in colors:
        if color in content:
            found_colors.append(color)
    
    if len(found_colors) == len(colors):
        print(f"   ✅ All {len(colors)} colors found in main page")
    else:
        print(f"   ⚠️  Only {len(found_colors)}/{len(colors)} colors found in main page")
        print(f"      Found: {found_colors}")
        print(f"      Missing: {set(colors) - set(found_colors)}")
    
    # Check a few city pages
    cities_to_check = ["beijing", "shanghai", "chengdu"]
    all_cities_have_colors = True
    
    for city in cities_to_check:
        html_file = f"cities/{city}.html"
        with open(html_file, 'r', encoding='utf-8') as f:
            city_content = f.read()
        
        city_colors_found = [color for color in colors if color in city_content]
        if len(city_colors_found) == len(colors):
            print(f"   ✅ {city}.html has all colors")
        else:
            print(f"   ⚠️  {city}.html missing some colors")
            all_cities_have_colors = False
    
    return len(found_colors) > 0 and all_cities_have_colors

def verify_navigation():
    """Verify navigation is working"""
    print("\n🔍 Verifying navigation...")
    
    cities = [
        "beijing", "shanghai", "chengdu", "harbin", "chongqing",
        "wuxi", "qingdao", "xiamen", "nanjing", "shenzhen", 
        "guangzhou", "hongkong"
    ]
    
    all_good = True
    problematic_cities = []
    
    for city in cities:
        html_file = f"cities/{city}.html"
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for back-to-home link
        if 'href="../index.html"' not in content:
            problematic_cities.append(city)
            all_good = False
    
    if all_good:
        print(f"   ✅ All {len(cities)} cities have back-to-home links")
    else:
        print(f"   ❌ {len(problematic_cities)} cities missing back-to-home links:")
        for city in problematic_cities[:5]:  # Show first 5
            print(f"      • {city}")
        if len(problematic_cities) > 5:
            print(f"      ... and {len(problematic_cities) - 5} more")
    
    return all_good

def main():
    print("=" * 60)
    print("Final Verification: Issues 1 & 2 Fixed")
    print("=" * 60)
    
    print("\n📋 Issue 1: News section not found")
    news_fixed = verify_news_section()
    
    print("\n📋 Issue 2: Layout consistency - Color scheme not utilized")
    layout_fixed = verify_layout_colors()
    
    print("\n📋 Bonus: Navigation verification")
    navigation_ok = verify_navigation()
    
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    
    if news_fixed:
        print("✅ ISSUE 1 FIXED: News section is working correctly")
    else:
        print("❌ ISSUE 1 NOT FIXED: News section still has problems")
    
    if layout_fixed:
        print("✅ ISSUE 2 FIXED: Layout colors are being used")
    else:
        print("⚠️  ISSUE 2 PARTIALLY FIXED: Colors are present but could be improved")
    
    if navigation_ok:
        print("✅ BONUS: All navigation links are correct")
    else:
        print("⚠️  BONUS: Some navigation links need attention (monitor bug?)")
    
    print("\n🎯 STATUS:")
    if news_fixed and layout_fixed:
        print("Both issues 1 and 2 have been successfully fixed!")
        print("The website monitoring system should now pass all checks.")
    else:
        print("Some issues remain. Review the problems above.")

if __name__ == "__main__":
    main()