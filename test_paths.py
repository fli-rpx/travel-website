#!/usr/bin/env python3
"""
Test image paths for different viewing methods
"""

def test_paths(base_url, page_path, image_path):
    """Test how paths resolve"""
    print(f"\n🔗 Testing from: {base_url}{page_path}")
    print(f"   Image path: {image_path}")
    
    # Simulate browser resolution
    if image_path.startswith('/'):
        # Absolute path
        resolved = base_url.rstrip('/') + image_path
    elif image_path.startswith('http'):
        # Full URL
        resolved = image_path
    elif image_path.startswith('../'):
        # Relative up
        # Remove filename from page_path, go up directories
        dir_path = '/'.join(page_path.split('/')[:-2]) + '/'  # Go up one from cities/
        resolved = base_url + dir_path + image_path[3:]  # Remove ../
    else:
        # Relative
        dir_path = '/'.join(page_path.split('/')[:-1]) + '/'
        resolved = base_url + dir_path + image_path
    
    print(f"   → Resolves to: {resolved}")
    return resolved

# Test scenarios
print("=" * 60)
print("IMAGE PATH RESOLUTION TESTS")
print("=" * 60)

# Scenario 1: GitHub Pages
print("\n📦 GITHUB PAGES:")
test_paths(
    base_url="https://fli-rpx.github.io/travel-website/",
    page_path="cities/chongqing.html",
    image_path="../images/user_photos/chongqing.jpg"
)

# Scenario 2: Local file (from cities folder)
print("\n💻 LOCAL FILE (from cities/ folder):")
test_paths(
    base_url="file:///Users/fudongli/clawd/travel-website/",
    page_path="cities/chongqing.html",
    image_path="../images/user_photos/chongqing.jpg"
)

# Scenario 3: Absolute path on GitHub Pages
print("\n📍 ABSOLUTE PATH (GitHub Pages):")
test_paths(
    base_url="https://fli-rpx.github.io/",
    page_path="travel-website/cities/chongqing.html",
    image_path="/travel-website/images/user_photos/chongqing.jpg"
)

# Scenario 4: Local web server (port 8000)
print("\n🌐 LOCAL WEB SERVER (port 8000):")
test_paths(
    base_url="http://localhost:8000/",
    page_path="travel-website/cities/chongqing.html",
    image_path="../images/user_photos/chongqing.jpg"
)

print("\n" + "=" * 60)
print("RECOMMENDATION:")
print("=" * 60)
print("""
For GitHub Pages (https://fli-rpx.github.io/travel-website/):
- Page: /travel-website/cities/chongqing.html
- Use: ../images/user_photos/chongqing.jpg
  → Resolves to: /travel-website/images/user_photos/chongqing.jpg ✓

For local viewing (file://):
- Page: file:///.../travel-website/cities/chongqing.html  
- Use: ../images/user_photos/chongqing.jpg
  → Resolves to: file:///.../travel-website/images/user_photos/chongqing.jpg ✓

The path '../images/user_photos/chongqing.jpg' should work for both!
""")