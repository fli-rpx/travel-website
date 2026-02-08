# Travel Website

A modern travel website for Chinese cities with automated monitoring, AI image generation, and dynamic news updates.

## Features

- 12 complete city pages (Beijing, Shanghai, Chengdu, Harbin, Chongqing, etc.)
- Latest China Travel News section with daily updates
- Automated monitoring system (runs every 10 minutes)
- AI image generation ready
- Self-improving capabilities
- Mobile responsive design
- Consistent styling across all pages

## Deployment

This site is deployed via GitHub Pages at: https://fli-rpx.github.io/travel-website/

## News Section

The website features a dynamic "Latest China Travel News" section that:
- Replaces the static Popular Destinations section
- Shows 3 updated news cards daily
- Includes travel policies, tips, and destination updates
- Features color-coded tags for easy categorization
- Validated by the monitoring system for consistency

## Monitoring System

The website includes an automated monitoring system that:
- Checks every 10 minutes for issues
- Verifies images, pages, and styling consistency
- Validates news section functionality
- Can auto-fix common problems
- Logs all activities

## City Pages

All city pages are located in the `cities/` directory:
- `beijing.html` - Beijing city page
- `shanghai.html` - Shanghai city page
- `chengdu.html` - Chengdu city page
- `harbin.html` - Harbin city page
- `chongqing.html` - Chongqing city page
- `wuxi.html` - Wuxi city page
- `qingdao.html` - Qingdao city page
- `xiamen.html` - Xiamen city page
- `nanjing.html` - Nanjing city page
- `shenzhen.html` - Shenzhen city page
- `guangzhou.html` - Guangzhou city page
- `hongkong.html` - Hong Kong city page

## Development

To run locally:
```bash
python3 -m http.server 8000
```

Then open: http://localhost:8000

## License

Free to use for personal and commercial projects.
