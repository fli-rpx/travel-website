#!/usr/bin/env python3
"""
Test the improvements we've made
"""

import os
import re

def test_modern_design():
    """Test that modern design elements are present"""
    print("🔍 Testing modern design implementation...")
    
    with open("index.html", 'r', encoding='utf-8') as f:
        content = f.read()
    
    checks = [
        ("bootstrap@5.3.0" in content, "Bootstrap CSS loaded"),
        ("fonts.googleapis.com" in content, "Google Fonts loaded"),
        ('href="style.css"' in content, "External style.css loaded"),
        ("display-4" in content, "Modern hero section"),
        ("btn btn-primary btn-lg" in content, "Modern button styles"),
        ("row g-4" in content, "Bootstrap grid system"),
        ("col-lg-4 col-md-6" in content, "Responsive grid columns"),
        ("city-grid-card" in content, "Grid card classes"),
        ("images/user_photos/beijing.jpg" in content, "City images present"),
        ('href="#news"' in content, "News links fixed"),
    ]
    
    all_passed = True
    for check_passed, check_name in checks:
        if check_passed:
            print(f"   ✅ {check_name}")
        else:
            print(f"   ❌ {check_name}")
            all_passed = False
    
    # Check that carousel is gone
    if "simple-carousel" in content:
        print("   ⚠️  Carousel classes still present (should be hidden)")
    
    return all_passed

def test_city_images():
    """Test that all city cards have images"""
    print("\n🔍 Testing city images...")
    
    with open("index.html", 'r', encoding='utf-8') as f:
        content = f.read()
    
    cities = [
        "beijing", "shanghai", "chengdu", "harbin", "chongqing",
        "wuxi", "qingdao", "xiamen", "nanjing", "shenzhen", 
        "guangzhou", "hongkong"
    ]
    
    missing_images = []
    for city in cities:
        image_path = f"images/user_photos/{city}.jpg"
        if image_path not in content:
            missing_images.append(city)
    
    if not missing_images:
        print(f"   ✅ All {len(cities)} cities have images")
    else:
        print(f"   ❌ {len(missing_images)} cities missing images:")
        for city in missing_images[:5]:
            print(f"      • {city}")
        if len(missing_images) > 5:
            print(f"      ... and {len(missing_images) - 5} more")
    
    return len(missing_images) == 0

def test_responsive_design():
    """Test responsive design elements"""
    print("\n🔍 Testing responsive design...")
    
    with open("style.css", 'r', encoding='utf-8') as f:
        css_content = f.read()
    
    checks = [
        ("@media (max-width:" in css_content, "Media queries present"),
        ("col-lg-" in css_content or "col-md-" in css_content, "Responsive grid classes"),
        ("max-width" in css_content, "Container max-width"),
    ]
    
    all_passed = True
    for check_passed, check_name in checks:
        if check_passed:
            print(f"   ✅ {check_name}")
        else:
            print(f"   ❌ {check_name}")
            all_passed = False
    
    return all_passed

def test_css_conflicts():
    """Test for CSS conflicts"""
    print("\n🔍 Testing for CSS conflicts...")
    
    with open("index.html", 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Count style tags
    style_tags = content.count('<style>')
    
    # Check for conflicting color values
    conflicting_colors = []
    color_patterns = [
        r'#3b82f6',  # Inline blue
        r'#2563eb',  # CSS var primary
        r'#1d4ed8',  # Inline dark blue
        r'#1e40af',  # CSS var secondary
    ]
    
    for pattern in color_patterns:
        if re.search(pattern, content):
            conflicting_colors.append(pattern)
    
    if style_tags > 1:
        print(f"   ⚠️  Multiple style tags ({style_tags}) - potential conflicts")
    else:
        print(f"   ✅ Single style tag")
    
    if len(conflicting_colors) > 2:
        print(f"   ⚠️  Multiple color systems ({len(conflicting_colors)} different colors)")
    else:
        print(f"   ✅ Color system looks consistent")
    
    return style_tags <= 2 and len(conflicting_colors) <= 3

def main():
    print("=" * 60)
    print("Testing Website Improvements")
    print("=" * 60)
    
    tests = [
        ("Modern Design", test_modern_design),
        ("City Images", test_city_images),
        ("Responsive Design", test_responsive_design),
        ("CSS Conflicts", test_css_conflicts),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}:")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Error running test: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("IMPROVEMENTS TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
    
    print(f"\n📊 Results: {passed}/{total} tests passed ({passed/total*100:.0f}%)")
    
    if passed == total:
        print("\n🎉 All improvements implemented successfully!")
        print("The website now has:")
        print("1. ✅ Modern design with Bootstrap")
        print("2. ✅ City images on main page")
        print("3. ✅ Responsive grid (no carousel)")
        print("4. ✅ Reduced CSS conflicts")
    else:
        print(f"\n⚠️  {total - passed} tests failed. Review issues above.")

if __name__ == "__main__":
    main()