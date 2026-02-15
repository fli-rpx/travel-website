#!/usr/bin/env python3
"""
Replace the carousel with a responsive grid for better mobile experience
"""

import os
import re

def replace_carousel_with_grid():
    """Replace carousel with responsive grid"""
    html_file = "index.html"
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the carousel section
    # We need to find from <!-- SIMPLE CAROUSEL --> to the end of the cities section
    # Look for the carousel section and all city cards
    carousel_start = content.find('<!-- SIMPLE CAROUSEL -->')
    if carousel_start == -1:
        print("❌ Could not find carousel section")
        return False
    
    # Find the end of the cities section (look for closing section tag after carousel)
    # We'll search for the next </section> after a reasonable amount
    section_end = content.find('</section>', carousel_start)
    if section_end == -1:
        print("❌ Could not find end of carousel section")
        return False
    
    section_end += len('</section>')
    
    # Extract the carousel section
    carousel_section = content[carousel_start:section_end]
    
    # Extract all city cards from the carousel
    # Pattern to find each city card block
    city_card_pattern = r'<div class="city-card">.*?</div>\s*</div>'
    city_cards = re.findall(city_card_pattern, carousel_section, re.DOTALL)
    
    if not city_cards:
        print("❌ Could not find city cards in carousel")
        return False
    
    print(f"✅ Found {len(city_cards)} city cards")
    
    # Create new responsive grid section
    new_section = '''    <!-- CITIES GRID - Responsive Design -->
    <section id="cities" class="cities-section py-5">
        <div class="container">
            <div class="row mb-5">
                <div class="col-12 text-center">
                    <h2 class="display-5 fw-bold mb-3">Explore China Cities</h2>
                    <p class="lead text-muted">Discover 12 incredible destinations with rich history, vibrant culture, and unforgettable experiences</p>
                </div>
            </div>
            
            <div class="row g-4">
'''
    
    # Add each city card to the grid
    for i, card in enumerate(city_cards):
        # Extract city name from card
        city_name_match = re.search(r'<div class="city-name">([^<]+)</div>', card)
        city_name = city_name_match.group(1) if city_name_match else f"City {i+1}"
        
        # Extract city tag/description
        city_tag_match = re.search(r'<div class="city-tag">([^<]+)</div>', card)
        city_tag = city_tag_match.group(1) if city_tag_match else ""
        
        # Extract city details (the p tags)
        details_matches = re.findall(r'<p>([^<]+)</p>', card)
        details = details_matches if details_matches else []
        
        # Extract image URL
        image_match = re.search(r"background-image: url\('([^']+)'\)", card)
        image_url = image_match.group(1) if image_match else ""
        
        # Extract city link
        link_match = re.search(r'href="([^"]+)" class="city-header-link"', card)
        city_link = link_match.group(1) if link_match else f"cities/{city_name.lower()}.html"
        
        # Create Bootstrap card for grid
        new_card = f'''                <!-- {city_name} -->
                <div class="col-lg-4 col-md-6">
                    <div class="card city-grid-card h-100 border-0 shadow-lg overflow-hidden">
                        <div class="city-grid-image" style="background-image: linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.3)), url('{image_url}');">
                            <div class="city-grid-overlay p-4 d-flex flex-column justify-content-end">
                                <h3 class="text-white mb-2">{city_name}</h3>
                                <p class="text-light mb-0">{city_tag}</p>
                            </div>
                        </div>
                        <div class="card-body p-4">
'''
        
        # Add details
        for detail in details[:3]:  # Limit to 3 details
            new_card += f'                            <p class="card-text mb-2"><i class="fas fa-circle text-primary me-2" style="font-size: 0.5rem;"></i>{detail}</p>\n'
        
        # Add link button
        new_card += f'''                        </div>
                        <div class="card-footer bg-transparent border-0 pt-0 pb-4 px-4">
                            <a href="{city_link}" class="btn btn-outline-primary w-100">
                                <i class="fas fa-map-marker-alt me-2"></i>Explore {city_name}
                            </a>
                        </div>
                    </div>
                </div>
'''
        
        new_section += new_card
    
    # Close the grid section
    new_section += '''            </div>
            
            <div class="row mt-5">
                <div class="col-12 text-center">
                    <div class="alert alert-info" role="alert">
                        <h4 class="alert-heading"><i class="fas fa-lightbulb me-2"></i>Travel Tip</h4>
                        <p class="mb-0">Each city has its own unique charm and best time to visit. Click on any city to see detailed guides, travel tips, and local recommendations.</p>
                    </div>
                </div>
            </div>
        </div>
    </section>'''
    
    # Replace the old carousel section with new grid section
    new_content = content[:carousel_start] + new_section + content[section_end:]
    
    # Write updated content
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✅ Replaced carousel with responsive grid")
    print(f"   - Converted {len(city_cards)} city cards to grid layout")
    print("   - Added Bootstrap grid system (col-lg-4 col-md-6)")
    print("   - Added improved card design with hover effects")
    print("   - Added travel tip section")
    
    return True

def add_grid_styles():
    """Add CSS styles for the grid layout"""
    css_file = "style.css"
    
    with open(css_file, 'a', encoding='utf-8') as f:
        grid_styles = '''

/* Cities Grid Styles */
.cities-section {
    background-color: var(--light);
}

.city-grid-card {
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    border-radius: 16px;
    overflow: hidden;
}

.city-grid-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15) !important;
}

.city-grid-image {
    height: 250px;
    background-size: cover;
    background-position: center;
    position: relative;
}

.city-grid-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(to top, rgba(0, 0, 0, 0.7), transparent 60%);
}

.city-grid-card .card-body {
    background-color: white;
}

.city-grid-card .card-footer {
    background-color: white;
}

/* Responsive adjustments for grid */
@media (max-width: 768px) {
    .city-grid-image {
        height: 200px;
    }
    
    .city-grid-card {
        margin-bottom: 20px;
    }
}

/* Remove old carousel styles if they exist */
.simple-carousel,
.carousel-track,
.carousel-slide {
    display: none;
}
'''
        f.write(grid_styles)
    
    print("✅ Added grid styles to style.css")

def main():
    print("=" * 60)
    print("Replacing Carousel with Responsive Grid")
    print("=" * 60)
    
    print("\n1. Replacing carousel with grid...")
    if replace_carousel_with_grid():
        print("\n2. Adding grid styles...")
        add_grid_styles()
        
        print("\n🎉 Successfully replaced carousel with responsive grid!")
        print("\n📋 Benefits:")
        print("   - Better mobile experience")
        print("   - Simpler code (no JavaScript needed)")
        print("   - All cities visible at once (scrolling)")
        print("   - Improved accessibility")
        print("   - Consistent with city page design")
    else:
        print("\n❌ Failed to replace carousel")

if __name__ == "__main__":
    main()