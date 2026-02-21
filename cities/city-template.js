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
                <h3><i class="fas fa-utensils me-2"></i>Local Cuisine</h3>
                <p>${city.highlights.cuisine}</p>
            </div>
            <div class="city-highlight">
                <h3><i class="fas fa-calendar-alt me-2"></i>Best Time to Visit</h3>
                <p>${city.highlights.bestTime}</p>
            </div>
        </section>

        <!-- Local Cuisine -->
        <section id="cuisine" class="city-section">
            <h2><i class="fas fa-utensils me-3"></i>Local Cuisine</h2>
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