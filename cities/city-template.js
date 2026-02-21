/**
 * City Template JavaScript
 * Dynamically loads city data from JSON and renders the page
 */

// Get city ID from URL parameter or use default
function getCityId() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('city') || 'beijing'; // Default to Beijing if no parameter
}

// Load city data from individual JSON file
async function loadCityData(cityId) {
    try {
        const response = await fetch(`../data/${cityId}.json`);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error loading city data:', error);
        return null;
    }
}

// Food icons for each city
const foodIcons = {
    'beijing': 'https://kimi-web-img.moonshot.cn/img/media.istockphoto.com/f85a35c490a0365984f5cae797a7b97baf1c12d9.jpg',
    'shanghai': 'https://kimi-web-img.moonshot.cn/img/res.cloudinary.com/cba8e20ff85d2079666043972be31a3e21c558f0',
    'guangzhou': 'https://kimi-web-img.moonshot.cn/img/global.gcdn.top/a2fc4a87a659bd32ba3a8668ff07b656abdedf08.png',
    'shenzhen': 'https://kimi-web-img.moonshot.cn/img/thumbs.dreamstime.com/a46896599053ccf6a41c92f6478461057552ae08.jpg',
    'chengdu': 'https://kimi-web-img.moonshot.cn/img/png.pngtree.com/eb17d663950cef01201995f92b5acc7129edc699.png',
    'hangzhou': 'https://kimi-web-img.moonshot.cn/img/static.vecteezy.com/22d926968c143cc9eda53eaa63628d4388e1cba5.JPG',
    'wuhan': 'https://kimi-web-img.moonshot.cn/img/img08.weeecdn.net/18815de2c5a2e2d6f9f9533005b63a310387a82a.auto',
    'xian': 'https://kimi-web-img.moonshot.cn/img/blog.themalamarket.com/bf8adcb9bbadcb127de7b96d7df39af86fc11a12.jpg',
    'nanjing': 'https://kimi-web-img.moonshot.cn/img/img08.weeecdn.net/60fd9787c6cc569593d8707076368f3942b88730.auto',
    'chongqing': 'https://kimi-web-img.moonshot.cn/img/www.sichuantravelguide.com/0601534cc99d48c9203e76fafccfbe20769dcbfd.jpg',
    'tianjin': 'https://kimi-web-img.moonshot.cn/img/cdn.tasteatlas.com/4a70974c49034ffa3d90ad77d4f51fe482f8a3a0.jpg',
    'suzhou': 'https://kimi-web-img.moonshot.cn/img/png.pngtree.com/24f2aeafbd2dbffe1680fcff0daef6d1f3164cbf.jpg',
    'qingdao': 'https://kimi-web-img.moonshot.cn/img/steemitimages.com/071b2d6450277250af4f7aa77525af1f6c412be0.jpg',
    'harbin': 'https://kimi-web-img.moonshot.cn/img/upload.wikimedia.org/f7ca13b9da6dfe9fa8fb6ce5d61d435c8ad432a5.jpg',
    'hongkong': 'https://kimi-web-img.moonshot.cn/img/cdn.coconuts.co/b5b526a9ce89aaadeb71765f08313e697dce2581.jpg',
    'kunming': 'https://kimi-web-img.moonshot.cn/img/www.topchinatravel.com/733c3a77c29d86c14a51997cf7050e6aa8fdcb45.JPG',
    'xiamen': 'https://kimi-web-img.moonshot.cn/img/thewoksoflife.com/31740f440a658cfba93fad42c441a669bd9cc815.jpg',
    'dali': 'https://kimi-web-img.moonshot.cn/img/s.alicdn.com/5acb1d3ba632b05587e81fcf96dc1d6783d35368.jpg',
    'datong': 'https://kimi-web-img.moonshot.cn/img/www.chinaeducationaltours.com/d0387b656343bc76f740501b965d69c50b74c745.jpg',
    'guilin': 'https://kimi-web-img.moonshot.cn/img/ik.imagekit.io/50004b7895d40e8b100cb85e79359f3fa726f910.png',
    'guiyang': 'https://kimi-web-img.moonshot.cn/img/lvyinfood.com/22973b03d2dd5f1a8d634d7c358eba2b0948ab2e.png',
    'jinan': 'https://kimi-web-img.moonshot.cn/img/subsites.chinadaily.com.cn/3dbb7dd5ef71e21179d62fdd32aab5f49995023d.jpg',
    'kaifeng': 'https://kimi-web-img.moonshot.cn/img/www.shutterstock.com/2ced93624c861ef5983251a7c802db3f14407969.jpg',
    'kashi': 'https://kimi-web-img.moonshot.cn/img/phototravelasia.com/af278f498e7b0f8beedb11150da0aab0eade423f.jpg',
    'linyi': 'https://kimi-web-img.moonshot.cn/img/www.xindb.com/f57c18ae873ade31fe7688d3fa0b57f979c9d015.jpg',
    'taiyuan': 'https://kimi-web-img.moonshot.cn/img/www.chinaeducationaltours.com/dc4bbe4dea12b43732d92a8bb13401f9ad609582.jpg',
    'urumqi': 'https://kimi-web-img.moonshot.cn/img/cdn.shopify.com/f8b49da32883be260c7b921ff7ba309684dbda81.jpg',
    'wuxi': 'https://kimi-web-img.moonshot.cn/img/cdn-akamai.lkk.com/43126db2f94f41e1ac0a5afb3b2fcc5d04521171.jpg'
};

// Render city content
function renderCityContent(cityData, cityId) {
    const city = cityData; // City data is at root level in individual JSON files
    if (!city) {
        document.getElementById('city-content').innerHTML = '<div class="error">City not found</div>';
        return;
    }

    // Update page title and hero section
    document.title = city.title;
    document.getElementById('city-title').textContent = city.title;
    document.getElementById('city-name').textContent = city.heroTitle;
    document.getElementById('city-subtitle').textContent = city.heroSubtitle;
    document.getElementById('nav-city-name').textContent = `Explore ${city.name}`;
    
    // Set hero background image
    const heroSection = document.getElementById('city-hero');
    heroSection.style.setProperty('--hero-image', `url('${city.heroImage}')`);

    // Get food icon for this city
    const foodIcon = foodIcons[cityId] || '';
    const foodIconHtml = foodIcon ? `<img src="${foodIcon}" alt="${city.name} food" style="width: 24px; height: 24px; border-radius: 50%; object-fit: cover; margin-right: 8px; vertical-align: middle;">` : '<i class="fas fa-star me-2"></i>';

    // Generate content HTML
    const contentHTML = `
        <!-- Overview -->
        <section id="overview" class="city-section">
            <h2><i class="fas fa-info-circle me-3"></i>Overview</h2>
            <p>${city.overview}</p>
        </section>
        
        <!-- Highlights -->
        <section id="highlights" class="city-section">
            <h2><i class="fas fa-star me-3"></i>Must-See Highlights</h2>
            <div class="city-highlight">
                <h3><i class="fas fa-landmark me-2"></i>Top Attractions</h3>
                <p>${city.highlights.attractions}</p>
            </div>
            <div class="city-highlight">
                <h3><i class="fas fa-calendar-alt me-2"></i>Best Time to Visit</h3>
                <p>${city.highlights.bestTime}</p>
            </div>
        </section>

        <!-- Local Cuisine -->
        <section id="cuisine" class="city-section">
            <h2><i class="fas fa-utensils me-3"></i>Local Cuisine</h2>
            ${city.cuisine.signature_dishes ? `
            <div class="city-highlight">
                <h3>${foodIconHtml}Signature Dishes</h3>
                ${city.cuisine.signature_dishes.map(dish => `
                    <p><strong>${dish.name}:</strong> ${dish.description}</p>
                `).join('')}
            </div>
            ` : ''}
            ${city.cuisine.street_food ? `
            <div class="city-highlight">
                <h3><i class="fas fa-fire me-2"></i>Street Food</h3>
                <p>${city.cuisine.street_food.join(', ')}</p>
            </div>
            ` : ''}
            ${city.cuisine.famous_restaurants ? `
            <div class="city-highlight">
                <h3><i class="fas fa-store me-2"></i>Famous Restaurants</h3>
                <p>${city.cuisine.famous_restaurants.join(', ')}</p>
            </div>
            ` : ''}
            <div class="city-highlight">
                <h3><i class="fas fa-pepper-hot me-2"></i>Must-Try Dishes</h3>
                ${city.cuisine.dishes.map(dish => `
                    <p><strong>${dish.name}:</strong> ${dish.description}</p>
                `).join('')}
            </div>
            <div class="city-highlight">
                <h3><i class="fas fa-map-marker-alt me-2"></i>Best Food Streets</h3>
                ${city.cuisine.foodStreets.map(street => `
                    <p><strong>${street.name}:</strong> ${street.description}</p>
                `).join('')}
            </div>
        </section>

        <!-- Transportation -->
        <section id="transport" class="city-section">
            <h2><i class="fas fa-subway me-3"></i>Transportation</h2>
            <div class="city-highlight">
                <h3><i class="fas fa-plane me-2"></i>Getting There</h3>
                ${city.transportation.gettingThere.map(item => `<p>${item}</p>`).join('')}
            </div>
            <div class="city-highlight">
                <h3><i class="fas fa-bus me-2"></i>Getting Around</h3>
                ${city.transportation.gettingAround.map(item => `<p>${item}</p>`).join('')}
            </div>
        </section>

        <!-- Suggested Itinerary -->
        <section id="itinerary" class="city-section">
            <h2><i class="fas fa-calendar-alt me-3"></i>Suggested Itinerary</h2>
            ${city.itinerary.map(day => `
                <div class="city-highlight">
                    <h3><i class="fas fa-sun me-2"></i>${day.day}</h3>
                    ${day.activities.map(activity => `<p>${activity}</p>`).join('')}
                </div>
            `).join('')}
        </section>

        <!-- Gallery -->
        <section id="gallery" class="city-section">
            <h2><i class="fas fa-camera-retro me-3"></i>Gallery</h2>
            <div class="city-gallery">
                ${city.gallery.map((image, index) => `
                    <img src="${image}" alt="${city.name} view ${index + 1}" class="gallery-img" loading="lazy">
                `).join('')}
            </div>
        </section>
        
        <!-- Patent Data -->
        <section id="patent-data" class="city-section">
            <h2><i class="fas fa-file-alt me-3"></i>Patent Data</h2>
            <div class="patent-table">
                <table class="table table-bordered">
                    <thead>
                        <tr>
                            <th>Patent Number</th>
                            <th>Title</th>
                            <th>Current Assignee</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${city.patents.map(patent => `
                            <tr>
                                <td>${patent.number}</td>
                                <td>${patent.title}</td>
                                <td>${patent.assignee}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        </section>
    `;

    document.getElementById('city-content').innerHTML = contentHTML;
    
    // Update breadcrumb with city name
    document.getElementById('breadcrumb-city-name').textContent = city.name;
    
    // Update prev/next navigation
    updatePrevNextNavigation(cityId);
}

// Update previous/next city navigation
function updatePrevNextNavigation(currentCityId) {
    const currentIndex = availableCities.findIndex(city => city.id === currentCityId);
    if (currentIndex === -1) return;
    
    const prevCity = currentIndex > 0 ? availableCities[currentIndex - 1] : null;
    const nextCity = currentIndex < availableCities.length - 1 ? availableCities[currentIndex + 1] : null;
    
    const prevLink = document.getElementById('prev-city');
    const nextLink = document.getElementById('next-city');
    
    if (prevCity) {
        prevLink.href = `city-template.html?city=${prevCity.id}`;
        prevLink.innerHTML = `<i class="fas fa-arrow-left"></i><span>${prevCity.name}</span>`;
        prevLink.style.visibility = 'visible';
    } else {
        prevLink.style.visibility = 'hidden';
    }
    
    if (nextCity) {
        nextLink.href = `city-template.html?city=${nextCity.id}`;
        nextLink.innerHTML = `<span>${nextCity.name}</span><i class="fas fa-arrow-right"></i>`;
        nextLink.style.visibility = 'visible';
    } else {
        nextLink.style.visibility = 'hidden';
    }
}

// List of available cities
const availableCities = [
    { id: 'beijing', name: 'Beijing' },
    { id: 'shanghai', name: 'Shanghai' },
    { id: 'guangzhou', name: 'Guangzhou' },
    { id: 'shenzhen', name: 'Shenzhen' },
    { id: 'chengdu', name: 'Chengdu' },
    { id: 'hangzhou', name: 'Hangzhou' },
    { id: 'wuhan', name: 'Wuhan' },
    { id: 'xian', name: "Xi'an" },
    { id: 'nanjing', name: 'Nanjing' },
    { id: 'chongqing', name: 'Chongqing' },
    { id: 'tianjin', name: 'Tianjin' },
    { id: 'suzhou', name: 'Suzhou' },
    { id: 'qingdao', name: 'Qingdao' },
    { id: 'harbin', name: 'Harbin' },
    { id: 'hongkong', name: 'Hong Kong' },
    { id: 'kunming', name: 'Kunming' },
    { id: 'xiamen', name: 'Xiamen' },
    { id: 'dali', name: 'Dali' },
    { id: 'datong', name: 'Datong' },
    { id: 'guilin', name: 'Guilin' },
    { id: 'guiyang', name: 'Guiyang' },
    { id: 'jinan', name: 'Jinan' },
    { id: 'kaifeng', name: 'Kaifeng' },
    { id: 'kashi', name: 'Kashi' },
    { id: 'linyi', name: 'Linyi' },
    { id: 'taiyuan', name: 'Taiyuan' },
    { id: 'urumqi', name: 'Urumqi' },
    { id: 'wuxi', name: 'Wuxi' }
];

// Render city navigation links
function renderCityNavigation(currentCityId) {
    const cityLinksContainer = document.getElementById('city-links');
    
    const linksHTML = availableCities.map(city => {
        return `<a href="city-template.html?city=${city.id}" class="city-link">${city.name}</a>`;
    }).join('');
    
    cityLinksContainer.innerHTML = linksHTML;
}

// Initialize smooth scrolling for navigation
function initializeNavigation() {
    // Smooth scrolling for navigation links
    document.querySelectorAll('.jump-nav-link').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
                
                // Update active state
                document.querySelectorAll('.jump-nav-link').forEach(link => link.classList.remove('active'));
                this.classList.add('active');
            }
        });
    });

    // Update active navigation on scroll
    window.addEventListener('scroll', function() {
        const sections = document.querySelectorAll('.city-section');
        const navLinks = document.querySelectorAll('.jump-nav-link');
        
        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            if (window.scrollY >= sectionTop - 200) {
                current = section.getAttribute('id');
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === '#' + current) {
                link.classList.add('active');
            }
        });
    });
}

// Main initialization function
async function initializeCityPage() {
    const cityId = getCityId();
    const cityData = await loadCityData(cityId);
    
    if (cityData) {
        renderCityContent(cityData, cityId);
        renderCityNavigation(cityId);
        initializeNavigation();
    } else {
        document.getElementById('city-content').innerHTML = '<div class="error">Failed to load city data. Please try again later.</div>';
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', initializeCityPage);