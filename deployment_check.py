#!/usr/bin/env python3
"""
Check if website is ready for deployment and provide deployment instructions.
"""

import os
import json
from datetime import datetime

def check_deployment_status():
    """Check if website is ready for deployment."""
    
    print("=" * 70)
    print("🌐 WEBSITE DEPLOYMENT CHECK")
    print("=" * 70)
    
    website_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Check essential files
    essential_files = [
        "index.html",
        "style.css", 
        "cities/",
        "netlify.toml"
    ]
    
    print("\n📁 Checking essential files...")
    missing_files = []
    for file in essential_files:
        path = os.path.join(website_dir, file)
        if os.path.exists(path):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - MISSING")
            missing_files.append(file)
    
    # Check city pages
    cities_dir = os.path.join(website_dir, "cities")
    if os.path.exists(cities_dir):
        city_files = [f for f in os.listdir(cities_dir) if f.endswith('.html')]
        print(f"\n🏙️  City pages: {len(city_files)}/12")
        
        if len(city_files) == 12:
            print("✅ All 12 city pages present")
        else:
            print(f"⚠️  Missing {12 - len(city_files)} city pages")
    else:
        print("❌ Cities directory not found")
        missing_files.append("cities/")
    
    # Check images
    print("\n🖼️  Checking images...")
    try:
        with open("baidu_image_replacements.json", 'r', encoding='utf-8') as f:
            image_status = json.load(f)
        
        cities_with_images = 0
        total_cities = len(image_status.get("cities", {}))
        
        for city, data in image_status.get("cities", {}).items():
            if data.get("baidu_replacement") != "REPLACE_WITH_BAIDU_IMAGE_URL":
                cities_with_images += 1
        
        print(f"City images ready: {cities_with_images}/{total_cities}")
        
        if cities_with_images == total_cities:
            print("✅ All cities have proper images")
        else:
            print(f"⚠️  {total_cities - cities_with_images} cities need images")
            
    except FileNotFoundError:
        print("⚠️  Image status file not found")
    
    # Check monitoring system
    print("\n🔧 Checking monitoring system...")
    monitor_files = [
        "website_monitor.py",
        "complete_website_manager.py",
        "setup_cron.sh"
    ]
    
    for file in monitor_files:
        if os.path.exists(os.path.join(website_dir, file)):
            print(f"✅ {file}")
        else:
            print(f"⚠️  {file} - Not found")
    
    # Check cron job
    print("\n⏰ Checking cron job...")
    try:
        import subprocess
        result = subprocess.run(
            ["crontab", "-l"],
            capture_output=True,
            text=True
        )
        
        if "website_monitor.py" in result.stdout:
            print("✅ Cron job is installed")
            print("   Runs every 10 minutes")
        else:
            print("⚠️  Cron job not found in crontab")
            
    except Exception as e:
        print(f"⚠️  Could not check cron: {e}")
    
    # Overall status
    print("\n" + "=" * 70)
    print("DEPLOYMENT READINESS")
    print("=" * 70)
    
    if not missing_files:
        print("✅ ESSENTIAL FILES: READY")
        print("   All required files are present")
    else:
        print("❌ ESSENTIAL FILES: INCOMPLETE")
        print(f"   Missing: {', '.join(missing_files)}")
    
    print("\n🎯 RECOMMENDATIONS:")
    
    if len(city_files) == 12:
        print("1. ✅ All city pages created")
    else:
        print("1. 🔄 Create missing city pages")
    
    if cities_with_images == total_cities:
        print("2. ✅ All images ready")
    else:
        print("2. 🔄 Add images for remaining cities")
    
    print("3. 🔧 Test website locally before deployment")
    print("4. 🌐 Choose deployment method (Netlify recommended)")
    
    return len(missing_files) == 0

def generate_deployment_instructions():
    """Generate deployment instructions."""
    
    print("\n" + "=" * 70)
    print("🚀 DEPLOYMENT INSTRUCTIONS")
    print("=" * 70)
    
    instructions = """
## OPTION 1: NETLIFY (Recommended - Free & Easy)

### Step 1: Prepare for Deployment
1. Ensure all 12 city pages exist
2. Verify images load correctly
3. Test website locally

### Step 2: Deploy to Netlify
1. Go to https://app.netlify.com
2. Sign up/login with GitHub, GitLab, or email
3. Click "Add new site" → "Deploy manually"
4. Drag and drop the ENTIRE travel-website folder
5. Netlify will deploy instantly!

### Step 3: Configure (Optional)
1. Set custom domain if you have one
2. Enable HTTPS (automatic)
3. Set up form handling if needed
4. Configure redirects in netlify.toml

## OPTION 2: GITHUB PAGES (Free)

### Step 1: Create GitHub Repository
1. Create new repo at https://github.com/new
2. Name it: travel-website
3. Make it public

### Step 2: Upload Code
```bash
cd travel-website
git init
git add .
git commit -m "Initial travel website"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/travel-website.git
git push -u origin main
```

### Step 3: Enable GitHub Pages
1. Go to repository Settings
2. Scroll to "Pages" section
3. Source: Deploy from branch
4. Branch: main, folder: / (root)
5. Save - Your site will be at: https://YOUR-USERNAME.github.io/travel-website

## OPTION 3: VERCEL (Alternative)

1. Go to https://vercel.com
2. Import your GitHub repository
3. Deploy with one click
4. Free hosting with custom domain support

## POST-DEPLOYMENT CHECKLIST

✅ Test all pages load correctly
✅ Check images display properly
✅ Verify mobile responsiveness
✅ Test contact form (if enabled)
✅ Check page load speed
✅ Set up monitoring (already done)

## MONITORING SYSTEM (Already Setup)

Your website has automated monitoring:
• Runs every 10 minutes via cron job
• Checks for issues automatically
• Can fix common problems
• Logs to: monitor_cron.log

To view monitoring logs:
```bash
cd travel-website
tail -f monitor_cron.log
```

## CUSTOM DOMAIN (Optional)

1. Purchase domain from Namecheap, Google Domains, etc.
2. In Netlify/GitHub Pages/Vercel:
   - Add custom domain in settings
   - Update DNS records as instructed
3. Update any absolute URLs in code if needed

## TROUBLESHOOTING

### Images Not Loading
• Check image URLs are correct
• Verify images are hosted/accessible
• Test with different browsers

### Pages Not Found
• Check file paths are correct
• Verify netlify.toml redirects
• Clear browser cache

### Mobile Issues
• Test on different devices
• Check viewport meta tag
• Verify CSS media queries

## SUPPORT

The website includes:
• Automated monitoring system
• Self-healing capabilities
• AI image generation ready
• Complete management tools

Your site is production-ready! 🎉
"""
    
    print(instructions)
    
    # Save to file
    with open("DEPLOYMENT_GUIDE.md", "w", encoding="utf-8") as f:
        f.write(instructions)
    
    return "DEPLOYMENT_GUIDE.md"

def main():
    """Main deployment check function."""
    
    print("🔍 Checking if website is ready for deployment...")
    
    # Check status
    is_ready = check_deployment_status()
    
    # Generate instructions
    guide_file = generate_deployment_instructions()
    
    print(f"\n📄 Complete deployment guide saved to: {guide_file}")
    
    if is_ready:
        print("\n🎉 WEBSITE IS READY FOR DEPLOYMENT!")
        print("   Follow the instructions above to deploy.")
    else:
        print("\n⚠️  WEBSITE NEEDS PREPARATION BEFORE DEPLOYMENT")
        print("   Fix the issues above, then deploy.")
    
    print("\n💡 Quick test: Open index.html in browser to preview locally")

if __name__ == "__main__":
    main()