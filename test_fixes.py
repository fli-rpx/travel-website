#!/usr/bin/env python3
"""
Test that our fixes are working correctly
"""

import os
import re

def test_image_fixes():
    """Test that image fixes are in place"""
    print("🔍 Testing image fixes...")
    
    cities = [
        "beijing", "shanghai", "chengdu", "harbin", "chongqing",
        "wuxi", "qingdao", "xiamen", "nanjing", "shenzhen", 
        "guangzhou", "hongkong"
    ]
    
    all_good = True
    
    for city in cities:
        html_file = f"cities/{city}.html"
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check that there are no Unsplash images in gallery
        if "unsplash.com" in content and "city-gallery" in content:
            # Find the gallery section
            gallery_start = content.find('<div class="city-gallery">')
            if gallery_start != -1:
                gallery_end = content.find('</div>', gallery_start)
                gallery_section = content[gallery_start:gallery_end]
                if "unsplash.com" in gallery_section:
                    print(f"❌ {city}: Still has Unsplash images in gallery")
                    all_good = False
                    continue
        
        # Check that local image is used somewhere
        local_image = f"../images/user_photos/{city}.jpg"
        if local_image not in content:
            print(f"⚠️  {city}: Local image not found in HTML")
            # Not necessarily an error if only used in CSS
        
        print(f"✅ {city}: Image checks passed")
    
    # Check baidu_image_replacements.json exists
    if os.path.exists("baidu_image_replacements.json"):
        print("✅ baidu_image_replacements.json exists")
    else:
        print("❌ baidu_image_replacements.json missing")
        all_good = False
    
    return all_good

def test_navigation_fixes():
    """Test that navigation fixes are in place"""
    print("\n🔍 Testing navigation fixes...")
    
    cities = [
        "beijing", "shanghai", "chengdu", "harbin", "chongqing",
        "wuxi", "qingdao", "xiamen", "nanjing", "shenzhen", 
        "guangzhou", "hongkong"
    ]
    
    all_good = True
    
    for city in cities:
        html_file = f"cities/{city}.html"
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for absolute paths (should be none)
        if '/travel-website/' in content:
            print(f"❌ {city}: Still has absolute paths")
            all_good = False
            continue
        
        # Check for back-to-home link
        if 'href="../index.html"' not in content:
            print(f"❌ {city}: Missing back-to-home link")
            all_good = False
            continue
        
        print(f"✅ {city}: Navigation checks passed")
    
    # Check main page
    with open("index.html", 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for absolute city links (should be none)
    if '/travel-website/cities/' in content:
        print("❌ index.html: Still has absolute city links")
        all_good = False
    else:
        print("✅ index.html: Navigation checks passed")
    
    return all_good

def test_cleanup():
    """Test that backup files are cleaned up"""
    print("\n🔍 Testing cleanup...")
    
    # Check for backup files
    backup_files = []
    for root, dirs, files in os.walk("cities"):
        for file in files:
            if any(term in file.lower() for term in ['backup', 'fixed', 'improved', 'old']):
                backup_files.append(os.path.join(root, file))
    
    if backup_files:
        print(f"❌ Found {len(backup_files)} backup files:")
        for file in backup_files[:5]:  # Show first 5
            print(f"   • {file}")
        if len(backup_files) > 5:
            print(f"   ... and {len(backup_files) - 5} more")
        return False
    else:
        print("✅ No backup files found")
        return True

def test_404_page():
    """Test that 404 page exists"""
    print("\n🔍 Testing 404 page...")
    
    if os.path.exists("404.html"):
        print("✅ 404.html exists")
        
        # Check it has basic structure
        with open("404.html", 'r', encoding='utf-8') as f:
            content = f.read()
        
        checks = [
            ("404" in content, "Contains '404'"),
            ("Page Not Found" in content, "Has 'Page Not Found' title"),
            ('href="index.html"' in content, "Has link back to home"),
        ]
        
        all_passed = True
        for check_passed, check_name in checks:
            if check_passed:
                print(f"   ✅ {check_name}")
            else:
                print(f"   ❌ {check_name}")
                all_passed = False
        
        return all_passed
    else:
        print("❌ 404.html missing")
        return False

def main():
    print("=" * 60)
    print("Testing Website Fixes")
    print("=" * 60)
    
    tests = [
        ("Image Fixes", test_image_fixes),
        ("Navigation Fixes", test_navigation_fixes),
        ("Cleanup", test_cleanup),
        ("404 Page", test_404_page),
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
    print("TEST SUMMARY")
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
        print("\n🎉 All tests passed! The high-priority fixes are complete.")
    else:
        print(f"\n⚠️  {total - passed} tests failed. Review the issues above.")

if __name__ == "__main__":
    main()