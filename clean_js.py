#!/usr/bin/env python3
"""
Clean JavaScript - remove all carousel code
"""

import re

def clean_javascript():
    """Remove all carousel JavaScript."""
    print("🧹 Cleaning JavaScript...")
    
    filepath = "/Users/fudongli/clawd/travel-website/index.html"
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Remove carousel variables and functions
    patterns_to_remove = [
        # Carousel variables
        r'// Carousel variables[\s\S]*?let currentIndex = 0;',
        
        # showCityGroup function
        r'function showCityGroup\(index\)[\s\S]*?currentIndex = index;',
        
        # Next button click handler
        r'// Next button click[\s\S]*?showCityGroup\(nextIndex\);',
        
        # Previous button click handler
        r'// Previous button click[\s\S]*?showCityGroup\(prevIndex\);',
        
        # Dot click handlers
        r'// Dot click handlers[\s\S]*?showCityGroup\(index\);',
        
        # Auto-rotate
        r'// Auto-rotate carousel[\s\S]*?showCityGroup\(nextIndex\);',
        
        # Initialization
        r'// Initialize with first group[\s\S]*?showCityGroup\(0\);',
        
        # Forceful initialization
        r'// FORCEFUL INITIALIZATION[\s\S]*?console\.log\(\'Forceful initialization complete\'\);',
        
        # Diagnostic
        r'// IMMEDIATE DIAGNOSTIC[\s\S]*?slides visible\.\'\);',
    ]
    
    for pattern in patterns_to_remove:
        content = re.sub(pattern, '', content, flags=re.DOTALL)
    
    print("✅ Removed carousel JavaScript")
    
    # Add simple static grid logging
    simple_js = '''
    // Simple static grid loaded
    document.addEventListener('DOMContentLoaded', function() {
        console.log('✅ Static grid loaded - all 12 cities visible');
        const cityCards = document.querySelectorAll('.city-card');
        console.log('City cards found:', cityCards.length);
        
        // Verify all cards are visible
        const visibleCards = Array.from(cityCards).filter(card => 
            window.getComputedStyle(card).display !== 'none'
        );
        console.log('Visible city cards:', visibleCards.length);
        
        if (visibleCards.length === 12) {
            console.log('✅ SUCCESS: All 12 cities visible in grid layout!');
        }
    });
    '''
    
    # Add before closing </script>
    script_end = content.rfind('</script>')
    if script_end != -1:
        content = content[:script_end] + simple_js + content[script_end:]
        print("✅ Added static grid logging")
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ JavaScript cleaned")
        return True
    else:
        print("⚠️  No changes were applied")
        return False

if __name__ == "__main__":
    clean_javascript()