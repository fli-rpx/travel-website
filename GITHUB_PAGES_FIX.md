# GitHub Pages Deployment Instructions

## Current Issue
Your site is deployed at: https://fli-rpx.github.io/travel-website/
But city pages return 404: https://fli-rpx.github.io/travel-website/cities/guangzhou.html

## Solution

### Step 1: Update GitHub Repository
```bash
cd /Users/fudongli/clawd/travel-website

# Add all files
git add .

# Commit changes
git commit -m "Fix GitHub Pages deployment"

# Push to GitHub
git push origin main
```

### Step 2: Enable GitHub Pages (if not already)
1. Go to: https://github.com/fli-rpx/travel-website/settings/pages
2. Source: Deploy from branch
3. Branch: main
4. Folder: / (root)
5. Save

### Step 3: Wait for Deployment
GitHub Pages takes 1-2 minutes to deploy after push.

### Step 4: Test
1. Main page: https://fli-rpx.github.io/travel-website/
2. City page: https://fli-rpx.github.io/travel-website/cities/guangzhou.html

## Alternative: Use Relative Paths (Better)

If absolute paths don't work, use relative paths:

### In city pages (cities/*.html):
Change: `href="../index.html"`
To: `href="../index.html"` (keep as is for relative)

### In main page (index.html):
Change: `href="cities/guangzhou.html"`
To: `href="./cities/guangzhou.html"` (add ./ for clarity)

## Files Created for GitHub Pages:
1. `.nojekyll` - Disables Jekyll processing
2. `.gitignore` - Ignores logs and config files
3. Updated `README.md` - Documentation

## Testing Locally Before Push
```bash
cd /Users/fudongli/clawd/travel-website
python3 -m http.server 8000
# Open: http://localhost:8000/cities/guangzhou.html
```

## Need Help?
Check GitHub Pages documentation: https://docs.github.com/en/pages
