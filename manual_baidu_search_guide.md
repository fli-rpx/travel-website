# Manual Baidu Image Search Guide

Since we're having browser automation issues, here's how to manually search for images using the tools I've created.

## 📋 What You Need

1. **Chrome browser** with Clawdbot extension turned ON
2. **Access to Baidu** (China IP or VPN with Chinese server)
3. **The search links** I've already generated

## 🚀 Quick Start - Search for Beijing Images

### Step 1: Open Search Page
Open this file in Chrome:
```
file:///Users/fudongli/clawd/travel-website/baidu_image_search.html
```

### Step 2: Click Beijing Search Links
On the page, find the **Beijing** section and click:
- **🔍 Search on Baidu** - General Beijing tourism images
- **🏞️ Scenery** - Beijing scenery images
- **🏛️ Architecture** - Beijing architecture images
- **🌃 Night View** - Beijing night views

### Step 3: Download Images
On Baidu Image Search page:
1. Find an image you like
2. **Right-click** → **图片另存为** (Save image as)
3. Save with descriptive name: `beijing_great_wall_1.jpg`

### Step 4: Host the Image
**Option A: Image Hosting Service**
1. Go to https://imgbb.com/ or similar
2. Upload your image
3. Get direct image URL

**Option B: Local Hosting**
1. Create folder: `travel-website/images/baidu/`
2. Save image there
3. Use path: `images/baidu/beijing_great_wall_1.jpg`

### Step 5: Update Your Website
1. Edit `baidu_image_replacements.json`
2. Replace `"REPLACE_WITH_BAIDU_IMAGE_URL"` with your actual URL
3. Run: `python3 update_with_baidu.py`

## 🔗 Direct Search Links (Copy & Paste)

### Beijing
- Great Wall: https://image.baidu.com/search/index?tn=baiduimage&word=%E5%8C%97%E4%BA%AC%20%E9%95%BF%E5%9F%8E
- Forbidden City: https://image.baidu.com/search/index?tn=baiduimage&word=%E5%8C%97%E4%BA%AC%20%E6%95%85%E5%AE%AB
- Scenery: https://image.baidu.com/search/index?tn=baiduimage&word=%E5%8C%97%E4%BA%AC%20%E6%97%85%E6%B8%B8%20%E6%99%AF%E7%82%B9%20%E9%A3%8E%E6%99%AF

### Shanghai
- Bund: https://image.baidu.com/search/index?tn=baiduimage&word=%E4%B8%8A%E6%B5%B7%20%E5%A4%96%E6%BB%A9
- Skyline: https://image.baidu.com/search/index?tn=baiduimage&word=%E4%B8%8A%E6%B5%B7%20%E4%B8%9C%E6%96%B9%E6%98%8E%E7%8F%A0
- Night View: https://image.baidu.com/search/index?tn=baiduimage&word=%E4%B8%8A%E6%B5%B7%20%E5%A4%9C%E6%99%AF

### Chengdu
- Pandas: https://image.baidu.com/search/index?tn=baiduimage&word=%E6%88%90%E9%83%BD%20%E7%86%8A%E7%8C%AB
- Panda Base: https://image.baidu.com/search/index?tn=baiduimage&word=%E6%88%90%E9%83%BD%20%E5%A4%A7%E7%86%8A%E7%8C%AB%E5%9F%BA%E5%9C%B0

## 🎯 Recommended Search Strategy

### Phase 1: Test with 1 City
1. Search for Beijing Great Wall images
2. Download 1-2 best images
3. Update website for Beijing only
4. Verify it works

### Phase 2: Complete 5 Main Cities
1. Beijing ✓
2. Shanghai
3. Chengdu
4. Harbin
5. Chongqing

### Phase 3: Remaining 7 Cities
1. Wuxi
2. Qingdao
3. Xiamen
4. Nanjing
5. Shenzhen
6. Guangzhou
7. Hongkong

## ⚠️ Troubleshooting

### Can't Access Baidu?
- Use VPN with Chinese server
- Try different Chinese VPN provider
- Check if Baidu is blocked in your region

### Images Not Loading?
- Check image URL is correct
- Test URL in browser directly
- Try different image format (jpg, png)

### Update Script Not Working?
- Check `baidu_image_replacements.json` format
- Make sure URLs are replaced (not "REPLACE_WITH_BAIDU_IMAGE_URL")
- Run with: `cd travel-website && python3 update_with_baidu.py`

## ✅ Success Checklist

- [ ] Opened `baidu_image_search.html`
- [ ] Clicked Beijing search links
- [ ] Downloaded 1-2 Beijing images
- [ ] Hosted images (ImgBB or local)
- [ ] Updated `baidu_image_replacements.json`
- [ ] Ran `update_with_baidu.py`
- [ ] Verified Beijing image updated on website

## 📞 Need Help?

If you're stuck:
1. Try searching manually first
2. Start with just Beijing
3. Use the HTML search page for easy clicking
4. The system is set up - just need to search/download images

Good luck! The authentic Baidu images will make your travel website much more authentic and appealing to Chinese travelers.