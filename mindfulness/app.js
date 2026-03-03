// Mindfulness Therapy - Enhanced JavaScript with Emotion Ribbon Integration
// Features: Power-Possession Cycle, AI Assessment with Emotion Ribbon, Micro-Interventions
// Copyright © 2026 Mindfulness Therapy. All rights reserved.

const app = {
    currentTab: 'home',
    currentStep: 0,
    answers: {},
    timerInterval: null,
    timerSeconds: 0,
    timerTotal: 0,
    isRunning: false,
    currentIntervention: null,

    // Emotion Ribbon Integration
    emotionRibbon: null,
    ribbonVisualizer: null,
    chatMessages: [],

            security: {
                sanitize: (str) => {
                    if (!str) return '';
                    const temp = document.createElement('div');
                    temp.textContent = str;
                    return temp.innerHTML;
                },
                validate: (str, maxLength = 500) => {
                    if (!str) return { isValid: false, message: 'Input cannot be empty.' };
                    if (str.length > maxLength) return { isValid: false, message: `Input cannot exceed ${maxLength} characters.` };
                    // Add more validation rules as needed
                    return { isValid: true };
                }
            },

    // Power-Possession Cycle Data
    cycleStates: {
        power: {
            name: 'Power',
            color: '#8B0000',
            bgColor: '#450a0a',
            description: 'External validation, feeling in control',
            triggers: ['Achievement', 'Recognition', 'Status gain'],
            strategies: ['Values grounding', 'Internal validation', 'Preventive balance']
        },
        possession: {
            name: 'Possession',
            color: '#FF6B35',
            bgColor: '#3b0764',
            description: 'Owning phase, attachment to external power',
            triggers: ['Control behaviors', 'Territoriality', 'Acquisition'],
            strategies: ['Letting go practice', 'Non-attachment', 'Impermanence awareness']
        },
        loss: {
            name: 'Loss',
            color: '#191970',
            bgColor: '#172554',
            description: 'Inevitable decline, external power fading',
            triggers: ['Status loss', 'Rejection', 'Failure'],
            strategies: ['Acceptance', 'Grief processing', 'Reality orientation']
        },
        emptiness: {
            name: 'Emptiness',
            color: '#36454F',
            bgColor: '#111827',
            description: 'Collapse, void when external validation gone',
            triggers: ['Isolation', 'Meaninglessness', 'Disconnection'],
            strategies: ['Somatic anchoring', 'Presence', 'Self-compassion']
        },
        craving: {
            name: 'Craving',
            color: '#DC143C',
            bgColor: '#451a03',
            description: 'Compulsive urge for substitute satisfaction',
            triggers: ['Emptiness', 'Boredom', 'Restlessness'],
            strategies: ['Urge surfing', 'Pattern interruption', 'Alternative satisfaction']
        },
        return: {
            name: 'Return',
            color: '#2E8B57',
            bgColor: '#052e16',
            description: 'Power-seeking behavior restarting cycle',
            triggers: ['Hope', 'Opportunity', 'New validation source'],
            strategies: ['Cycle awareness', 'Conscious choice', 'Break pattern']
        }
    },

    hoverTimeout: null,
    currentHoverState: null,

    // Salad Questions
    spicyQuestions: [
        { id: 'emotion_now', text: 'What emotion am I feeling most right now?', options: ['Anger', 'Fear', 'Shame', 'Emptiness', 'Powerlessness', 'Anxiety', 'Sadness'] },
        { id: 'body_location', text: 'Where in my body do I feel this emotion?', options: ['Chest tightness', 'Stomach knot', 'Heat in face', 'Cold hands', 'Tension in shoulders', 'Lump in throat', 'Cannot feel anything'] },
        { id: 'intensity', text: 'On a scale of 1-10, how intense is this feeling?', options: ['1-3 (Mild)', '4-6 (Moderate)', '7-8 (Strong)', '9-10 (Overwhelming)'] },
        { id: 'trigger', text: 'What just happened before this feeling arose?', options: ['A loss', 'Rejection', 'Failure', 'Reminded of past', 'Conflict', 'Uncertainty', 'Nothing specific'] },
        { id: 'familiar', text: 'Does this feeling remind me of any past situation?', options: ['Childhood', 'Past relationship', 'Work situation', 'Family pattern', 'This is new', 'Happens often'] },
        { id: 'story', text: 'What story is my mind telling me?', options: ['I am not enough', 'I am losing control', 'I need to fix this', 'I am being abandoned', 'I must prove myself', 'Something else'] },
        { id: 'need', text: 'If this emotion could speak, what would it say it needs?', options: ['Safety', 'Connection', 'Recognition', 'Rest', 'Control', 'Love', 'Just to be heard'] }
    ],

    greasyQuestions: [
        { id: 'urge', text: 'What do I urgently want to do right now?', options: ['Reach out to someone', 'Seek attention', 'Escape/avoid', 'Control something', 'Prove myself', 'Get validation', 'Something else'] },
        { id: 'fixation', text: 'Is there a specific person or type of person I am fixating on?', options: ['Ex/partner', 'Authority figure', 'Someone I am attracted to', 'Family member', 'No one specific', 'A fantasy/ideal'] },
        { id: 'aftermath', text: 'If I acted on this urge, how would I feel immediately after?', options: ['Relieved temporarily', 'Ashamed', 'Empty', 'Powerful briefly', 'Regretful', 'Satisfied'] },
        { id: 'next_day', text: 'How would I feel the next day?', options: ['Regret', 'Same emptiness', 'Shame', 'Nothing changed', 'Briefly better', 'Worse than before'] },
        { id: 'avoiding', text: 'What would I be avoiding feeling if I gave in?', options: ['Emptiness', 'Powerlessness', 'Shame', 'Fear', 'Loneliness', 'I do not know'] },
        { id: 'greasy_food', text: 'What is the greasy food I am reaching for?', options: ['Attention/affection', 'Control/power', 'Validation', 'Escape', 'Temporary high', 'Sense of winning'] }
    ],

    vegetableQuestions: [
        { id: 'opposite', text: 'What would the opposite of this craving feel like?', options: ['Letting go', 'Being present', 'Accepting', 'Connecting genuinely', 'Resting', 'Being vulnerable'] },
        { id: 'true_need', text: 'What do I truly need right now?', options: ['Connection', 'Rest', 'Safety', 'Recognition', 'Purpose', 'Self-compassion', 'Truth'] },
        { id: 'genuine_connect', text: 'Is there someone I could connect with genuinely, without agenda?', options: ['Yes, a friend', 'Yes, family', 'A therapist/counselor', 'Not right now', 'I need to be alone first'] },
        { id: 'sit_with_it', text: 'What would it feel like to sit with this emotion for 5 minutes?', options: ['Scary but possible', 'Overwhelming', 'Like it would pass', 'I do not know', 'I have done it before'] },
        { id: 'proud_action', text: 'What is one small thing I could do to feel proud tomorrow?', options: ['Journal honestly', 'Reach out to someone', 'Complete a small task', 'Rest without guilt', 'Practice mindfulness', 'Set a boundary'] },
        { id: 'without_power', text: 'If I were not trying to feel powerful, what would I want?', options: ['Peace', 'Connection', 'Meaning', 'Rest', 'To be seen', 'To create something', 'Just to be'] },
        { id: 'which_self', text: 'Which version of me is running the show?', options: ['The powerful one (owning)', 'The weak one (hiding)', 'The clear one (connecting)', 'A mix of all three', 'I do not know'] },
        { id: 'add_vegetable', text: 'If I could add one vegetable to balance this, which would help most?', options: ['Calm', 'Connection', 'Rest', 'Meaning', 'Truth', 'Self-compassion', 'Presence'] }
    ],

    quotes: [
        'The old you just reacted. The you now is learning to choose.',
        'The pause between feeling and action is where freedom lives.',
        'Inner power is the capacity to tolerate emptiness without panic.',
        'If I were not trying to feel powerful at all, what would I want?'
    ],

    journalPrompts: [
        'What are you grateful for today?',
        'What is one thing that went well?',
        'What are you looking forward to?',
        'What is the spiciest emotion right now?',
        'What greasy thing are you reaching for?',
        'What vegetable do you actually need?'
    ],

    interventions: {
        grounding: { name: 'Values Grounding', duration: 60, instructions: 'Take a deep breath. Ask yourself: What truly matters to me beyond external validation?' },
        powerbreathing: { name: 'Power Breathing', duration: 120, instructions: 'Inhale for 4 counts, hold for 4, exhale for 6. Feel the energy settle.' },
        somatic: { name: 'Somatic Anchoring', duration: 180, instructions: 'Feel your feet on the ground. Notice 3 sensations in your body right now.' },
        reframe: { name: 'Cognitive Reframe', duration: 120, instructions: 'What is another way to view this situation? What would you tell a friend?' },
        urgesurfing: { name: 'Urge Surfing', duration: 300, instructions: 'Observe the craving like a wave. It will rise, peak, and fall. You do not need to act.' },
        patternbreak: { name: 'Pattern Interrupt', duration: 60, instructions: 'Stand up. Stretch. Splash cold water on your face. Change your physical state.' },
        sigh: { name: 'Physiological Sigh', duration: 60, instructions: 'Take two quick inhales through nose, then one long exhale through mouth. Repeat 3 times.' },
        '54321': { name: '5-4-3-2-1 Grounding', duration: 60, instructions: 'Name 5 things you see, 4 you can touch, 3 you hear, 2 you smell, 1 you taste.' },
        compassion: { name: 'Self-Compassion Break', duration: 60, instructions: 'Place hand on heart. Say: This is hard. I am not alone. May I be kind to myself.' }
    },

    init() {
        this.setupNavigation();
        this.updateGreeting();
        this.loadData();
        this.renderQuote();
        this.renderStreak();
        this.renderCycle();
        this.setupSaladCheck();
        this.renderProgress();
        this.initEmotionRibbon();
        
        // Check for tab query parameter or hash
        const urlParams = new URLSearchParams(window.location.search);
        const tabParam = urlParams.get('tab');
        const hash = window.location.hash.replace('#', '');
        
        if (tabParam) {
            this.navigate(tabParam);
        } else if (hash) {
            this.navigate(hash);
        }
    },

    // Initialize Emotion Ribbon
    initEmotionRibbon() {
        // Load Emotion Ribbon scripts dynamically
        this.loadScript('emotion-ribbon.js', () => {
            this.loadScript('emotion-ribbon-visualizer.js', () => {
                this.setupEmotionRibbonUI();
            });
        });
    },

    loadScript(src, callback) {
        const script = document.createElement('script');
        script.src = src;
        script.onload = callback;
        script.onerror = () => console.error(`Failed to load ${src}`);
        document.head.appendChild(script);
    },

    setupEmotionRibbonUI() {
        // Add ribbon container to assessment tab if not exists
        const assessmentTab = document.getElementById('assessment');
        if (!assessmentTab || document.getElementById('emotionRibbonContainer')) return;

        const ribbonSection = document.createElement('div');
        ribbonSection.className = 'emotion-ribbon-section';
        ribbonSection.innerHTML = `
            <div class="ribbon-header">
                <h3><i class="fas fa-palette"></i> Emotion Ribbon</h3>
                <span class="ribbon-status">Real-time emotion detection</span>
            </div>
            <div id="emotionRibbonContainer" class="ribbon-container"></div>
            <div id="emotionRibbonLegend" class="ribbon-legend"></div>
        `;

        // Insert after chat interface
        const chatInterface = assessmentTab.querySelector('.chat-interface');
        if (chatInterface) {
            chatInterface.parentNode.insertBefore(ribbonSection, chatInterface.nextSibling);
        }

        // Initialize visualizer
        this.initEmotionRibbon();

        // Add CSS
        this.addRibbonStyles();
    },

    initEmotionRibbon() {
        // Check if EmotionRibbon is available
        if (typeof EmotionRibbon !== 'undefined' && typeof EmotionRibbonVisualizer !== 'undefined') {
            this.emotionRibbon = EmotionRibbon;
            this.ribbonVisualizer = new EmotionRibbonVisualizer('emotionRibbonContainer', {
                width: 600,
                height: 100,
                maxSegments: 8
            });
            this.renderRibbonLegend();
            
            // Setup real-time input detection
            this.setupRealTimeDetection();
        } else {
            // Retry after a short delay
            setTimeout(() => this.initEmotionRibbon(), 100);
        }
    },

    setupRealTimeDetection() {
        const chatInput = document.getElementById('chatInput');
        if (!chatInput || !this.emotionRibbon) return;

        let debounceTimer;
        
        chatInput.addEventListener('input', (e) => {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => {
                const text = e.target.value.trim();
                if (text.length > 2) {
                    this.analyzeWithRibbon(text);
                }
            }, 300); // Debounce 300ms
        });
    },

    renderRibbonLegend() {
        const legend = document.getElementById('emotionRibbonLegend');
        if (!legend || !this.emotionRibbon) return;

        const categories = this.emotionRibbon.getAllCategories();
        legend.innerHTML = categories.map(cat => `
            <div class="ribbon-legend-item" title="${cat.description}">
                <span class="legend-dot" style="background: ${cat.color}"></span>
                <span class="legend-name">${cat.emoji} ${cat.name}</span>
            </div>
        `).join('');
    },

    addRibbonStyles() {
        if (document.getElementById('ribbon-styles')) return;
        
        const style = document.createElement('style');
        style.id = 'ribbon-styles';
        style.textContent = `
            .emotion-ribbon-section {
                background: white;
                border-radius: 1rem;
                padding: 1.5rem;
                margin: 1.5rem 0;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
                border: 1px solid #e2e8f0;
            }
            .ribbon-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 1rem;
            }
            .ribbon-header h3 {
                font-size: 1rem;
                margin: 0;
                color: #1e293b;
            }
            .ribbon-status {
                font-size: 0.75rem;
                color: #64748b;
                background: #f1f5f9;
                padding: 0.25rem 0.75rem;
                border-radius: 9999px;
            }
            .ribbon-container {
                min-height: 100px;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .ribbon-legend {
                display: flex;
                flex-wrap: wrap;
                gap: 0.75rem;
                margin-top: 1rem;
                padding-top: 1rem;
                border-top: 1px solid #e2e8f0;
            }
            .ribbon-legend-item {
                display: flex;
                align-items: center;
                gap: 0.5rem;
                font-size: 0.75rem;
                color: #64748b;
                cursor: help;
            }
            .legend-dot {
                width: 10px;
                height: 10px;
                border-radius: 50%;
            }
        `;
        document.head.appendChild(style);
    },

    // Analyze message with Emotion Ribbon
    analyzeWithRibbon(text) {
        if (!this.emotionRibbon) return null;
        
        const analysis = this.emotionRibbon.analyze(text);
        
        // Update visualizer
        if (this.ribbonVisualizer && analysis.detected) {
            this.ribbonVisualizer.updateFromAnalysis(analysis);
        }
        
        return analysis;
    },

    setupNavigation() {
        document.querySelectorAll('.nav-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const tab = btn.dataset.tab;
                this.navigate(tab);
            });
        });
    },

    navigate(tab) {
        this.currentTab = tab;

        document.querySelectorAll('.nav-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.tab === tab);
        });

        document.querySelectorAll('.tab').forEach(t => {
            t.classList.toggle('active', t.id === tab);
        });

        // Close mobile menu after navigation
        this.closeMobileMenu();

        if (tab === 'progress') {
            this.renderProgress();
        } else if (tab === 'cycle') {
            this.renderCycle();
        } else if (tab === 'assessment') {
            // Initialize ribbon if not already done
            setTimeout(() => this.setupEmotionRibbonUI(), 100);
        } else if (tab === 'balance') {
            // Add a small delay to ensure DOM is ready
            setTimeout(() => {
                this.renderBalance();
            }, 50);
        } else if (tab === 'compass') {
            // Add a small delay to ensure DOM is ready
            setTimeout(() => {
                this.renderCompass();
            }, 50);
        } else if (tab === 'explorer') {
            // Add a small delay to ensure DOM is ready
            setTimeout(() => {
                this.renderExplorer();
            }, 50);
        }
    },

    toggleMobileMenu() {
        const navLinks = document.getElementById('navLinks');
        if (navLinks) {
            navLinks.classList.toggle('mobile-open');
        }
    },

    closeMobileMenu() {
        const navLinks = document.getElementById('navLinks');
        if (navLinks) {
            navLinks.classList.remove('mobile-open');
        }
    },

    updateGreeting() {
        const hour = new Date().getHours();
        let greeting = 'Good morning';
        if (hour >= 12 && hour < 17) greeting = 'Good afternoon';
        else if (hour >= 17) greeting = 'Good evening';
        else if (hour < 5) greeting = 'Good night';
        
        const el = document.getElementById('greeting');
        if (el) el.textContent = greeting + ',';
    },

    renderQuote() {
        const quote = this.quotes[Math.floor(Math.random() * this.quotes.length)];
        const el = document.getElementById('quoteCard');
        if (el) el.innerHTML = `<p>${quote}</p>`;
    },

    renderStreak() {
        const streak = this.getStreak();
        const el = document.getElementById('streakValue');
        if (el) el.textContent = streak;
        
        const sessionEl = document.getElementById('sessionValue');
        const minuteEl = document.getElementById('minuteValue');
        
        if (sessionEl) {
            const sessions = JSON.parse(localStorage.getItem('sessions') || '[]');
            sessionEl.textContent = sessions.length;
        }
        
        if (minuteEl) {
            const sessions = JSON.parse(localStorage.getItem('sessions') || '[]');
            const minutes = sessions.reduce((sum, s) => sum + (s.duration || 0), 0);
            minuteEl.textContent = minutes;
        }
    },

    getStreak() {
        const checkins = JSON.parse(localStorage.getItem('checkins') || '[]');
        return Math.min(checkins.length, 7);
    },

    // Power-Possession Cycle Visualization
    renderCycle() {
        const container = document.getElementById('cycleVisualization');
        if (!container) return;

        const states = ['power', 'possession', 'loss', 'emptiness', 'craving', 'return'];
        const centerX = 200;
        const centerY = 200;
        const radius = 120;

        let svg = `<svg viewBox="0 0 400 400" class="cycle-svg">`;
        
        // Draw connecting lines
        for (let i = 0; i < states.length; i++) {
            const angle1 = (i * 60 - 90) * Math.PI / 180;
            const angle2 = ((i + 1) % states.length * 60 - 90) * Math.PI / 180;
            const x1 = centerX + radius * Math.cos(angle1);
            const y1 = centerY + radius * Math.sin(angle1);
            const x2 = centerX + radius * Math.cos(angle2);
            const y2 = centerY + radius * Math.sin(angle2);
            
            svg += `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="#e2e8f0" stroke-width="3" />`;
        }

        // Draw nodes
        states.forEach((stateKey, i) => {
            const state = this.cycleStates[stateKey];
            const angle = (i * 60 - 90) * Math.PI / 180;
            const x = centerX + radius * Math.cos(angle);
            const y = centerY + radius * Math.sin(angle);
            
            svg += `
                <g class="cycle-node" 
                   onclick="app.showStateDetail('${stateKey}')" 
                   onmouseenter="app.changeBackgroundColor('${state.color}', '${state.bgColor}')"
                   onmouseleave="app.resetBackgroundColor()"
                   style="cursor: pointer;">
                    <circle cx="${x}" cy="${y}" r="40" fill="${state.color}20" stroke="${state.color}" stroke-width="3"/>
                    <text x="${x}" y="${y - 5}" text-anchor="middle" font-size="13" font-weight="600" fill="${state.color}">${state.name}</text>
                    <text x="${x}" y="${y + 12}" text-anchor="middle" font-size="18">${['🔴', '🟠', '🔵', '⚫', '🔴', '🟢'][i]}</text>
                </g>
            `;
        });

        // Center label
        svg += `
            <circle cx="${centerX}" cy="${centerY}" r="50" fill="white" stroke="#e2e8f0" stroke-width="2"/>
            <text x="${centerX}" y="${centerY - 5}" text-anchor="middle" font-size="12" font-weight="600" fill="#1e293b">Power-Possession</text>
            <text x="${centerX}" y="${centerY + 10}" text-anchor="middle" font-size="12" font-weight="600" fill="#1e293b">Cycle</text>
        `;

        svg += '</svg>';
        container.innerHTML = svg;
    },

    showStateDetail(stateKey) {
        const state = this.cycleStates[stateKey];
        const container = document.getElementById('cycleInfo');
        if (!container) return;

        container.innerHTML = `
            <div class="state-detail">
                <h3 style="color: ${state.color}">${state.name}</h3>
                <p>${state.description}</p>
                <h4>Common Triggers:</h4>
                <ul>
                    ${state.triggers.map(t => `<li>${t}</li>`).join('')}
                </ul>
                <h4>Helpful Strategies:</h4>
                <ul>
                    ${state.strategies.map(s => `<li>${s}</li>`).join('')}
                </ul>
            </div>
        `;
    },

    renderExplorer() {
        const explorerContainer = document.getElementById('explorerContainer');
        if (!explorerContainer) {
            setTimeout(() => this.renderExplorer(), 100);
            return;
        }

        explorerContainer.innerHTML = `
            <div class="explorer-container" style="padding-top: 2rem;">
                <section class="ribbon-display-section">
                    <div class="ribbon-container-wrapper">
                        <div id="emotionRibbonDisplay">
                            <div id="rainbowSvgContainer" style="width: 100%; height: 100%; position: absolute; top: 0; left: 0;">
                                <svg id="emotionRainbowSvg" viewBox="0 0 1200 120" style="width: 100%; height: 100%;">
                                    <path id="rainbow-pair-1" d="M 0,120 A 600,35 0 0 1 1200,120 L 1200,95 A 600,35 0 0 0 0,95 Z" fill="transparent" stroke="none"></path>
                                    <path id="rainbow-pair-2" d="M 0,100 A 600,25 0 0 1 1200,100 L 1200,75 A 600,25 0 0 0 0,75 Z" fill="transparent" stroke="none"></path>
                                    <path id="rainbow-pair-3" d="M 0,80 A 600,15 0 0 1 1200,80 L 1200,55 A 600,15 0 0 0 0,55 Z" fill="transparent" stroke="none"></path>
                                </svg>
                            </div>
                        </div>
                    </div>
                </section>

                <section class="categories-tabs-section">
                    <div class="tabs-container">
                        <button class="category-tab active" data-category="POWER" onclick="app.switchExplorerTab('POWER')">
                            <span class="tab-emoji">💪</span>
                            <span class="tab-name">Power</span>
                            <span class="tab-color-indicator" style="background: #FF0000;"></span>
                        </button>
                        <button class="category-tab" data-category="POSSESSION" onclick="app.switchExplorerTab('POSSESSION')">
                            <span class="tab-emoji">🏠</span>
                            <span class="tab-name">Possession</span>
                            <span class="tab-color-indicator" style="background: #FF00FF;"></span>
                        </button>
                        <button class="category-tab" data-category="LOSS" onclick="app.switchExplorerTab('LOSS')">
                            <span class="tab-emoji">💔</span>
                            <span class="tab-name">Loss</span>
                            <span class="tab-color-indicator" style="background: #0000FF;"></span>
                        </button>
                        <button class="category-tab" data-category="EMPTINESS" onclick="app.switchExplorerTab('EMPTINESS')">
                            <span class="tab-emoji">⭕</span>
                            <span class="tab-name">Emptiness</span>
                            <span class="tab-color-indicator" style="background: #00FF00;"></span>
                        </button>
                        <button class="category-tab" data-category="CRAVE" onclick="app.switchExplorerTab('CRAVE')">
                            <span class="tab-emoji">🔥</span>
                            <span class="tab-name">Crave</span>
                            <span class="tab-color-indicator" style="background: #FFFF00;"></span>
                        </button>
                        <button class="category-tab" data-category="EMPATHY" onclick="app.switchExplorerTab('EMPATHY')">
                            <span class="tab-emoji">🤝</span>
                            <span class="tab-name">Empathy</span>
                            <span class="tab-color-indicator" style="background: #00FFFF;"></span>
                        </button>
                    </div>
                    
                    <div class="words-layout">
                        <div class="words-display-area" id="wordsDisplayArea">
                        </div>
                        
                        <div class="selected-words-panel">
                            <div class="selected-words-display">
                                <h4><i class="fas fa-check-circle"></i> Selected Words</h4>
                                <div id="selectedWordsList">
                                    <span style="color: #94a3b8; font-size: 0.875rem;">No words selected yet...</span>
                                </div>
                            </div>
                            
                            <div class="stats-bar">
                                <div class="stat-item">
                                    <div class="stat-value" id="totalSelected">0</div>
                                    <div class="stat-label">Words</div>
                                </div>
                                <div class="stat-item">
                                    <div class="stat-value" id="categoriesActive">0</div>
                                    <div class="stat-label">Categories</div>
                                </div>
                                <div class="stat-item">
                                    <div class="stat-value" id="dominantCategory">-</div>
                                    <div class="stat-label">Dominant</div>
                                </div>
                            </div>
                            
                            <button class="clear-all-btn" onclick="app.clearAllExplorerWords()">
                                <i class="fas fa-trash-alt"></i> Clear All
                            </button>
                        </div>
                    </div>
                </section>
            </div>
        `;
        this.initExplorer();
    },

    // Explorer helper functions
    initExplorer() {
        this.explorerSelectedWords = [];
        this.explorerCurrentTab = 'POWER';
        this.explorerCategories = {
            POWER: { name: 'Power', emoji: '💪', color: '#FF0000' },
            POSSESSION: { name: 'Possession', emoji: '🏠', color: '#FF00FF' },
            LOSS: { name: 'Loss', emoji: '💔', color: '#0000FF' },
            EMPTINESS: { name: 'Emptiness', emoji: '⭕', color: '#00FF00' },
            CRAVE: { name: 'Crave', emoji: '🔥', color: '#FFFF00' },
            EMPATHY: { name: 'Empathy', emoji: '🤝', color: '#00FFFF' }
        };
        this.explorerRainbowColors = {
            POWER: '#FF0000',
            EMPATHY: '#00FFFF',
            EMPTINESS: '#00FF00',
            POSSESSION: '#FF00FF',
            LOSS: '#0000FF',
            CRAVE: '#FFFF00'
        };
        this.explorerCategoryToBand = {
            POWER: 'pair-1',
            EMPATHY: 'pair-1',
            POSSESSION: 'pair-2',
            EMPTINESS: 'pair-2',
            CRAVE: 'pair-3',
            LOSS: 'pair-3'
        };
        this.explorerComplementaryPairs = {
            POWER: 'EMPATHY',
            EMPATHY: 'POWER',
            EMPTINESS: 'POSSESSION',
            POSSESSION: 'EMPTINESS',
            CRAVE: 'LOSS',
            LOSS: 'CRAVE'
        };

        // Load Emotion Ribbon scripts if not already loaded
        if (!window.EmotionRibbon) {
            this.loadScript('emotion-ribbon.js', () => {
                this.switchExplorerTab('POWER');
                this.updateExplorerUI();
            });
        } else {
            this.switchExplorerTab('POWER');
            this.updateExplorerUI();
        }
    },

    switchExplorerTab(category) {
        this.explorerCurrentTab = category;
        
        // Update tab buttons
        document.querySelectorAll('#explorer .category-tab').forEach(tab => {
            tab.classList.remove('active');
            if (tab.dataset.category === category) {
                tab.classList.add('active');
            }
        });
        
        // Display words for selected category
        this.displayExplorerWordsForCategory(category);
    },

    displayExplorerWordsForCategory(categoryKey) {
        const displayArea = document.querySelector('#explorer #wordsDisplayArea');
        const category = this.explorerCategories[categoryKey];
        
        if (!window.EmotionRibbon || !window.EmotionRibbon.lexicon) {
            displayArea.innerHTML = '<p style="text-align: center; color: #94a3b8; padding: 2rem;">Loading words...</p>';
            return;
        }
        
        const words = window.EmotionRibbon.lexicon[categoryKey] || [];
        
        if (words.length === 0) {
            displayArea.innerHTML = '<p style="text-align: center; color: #94a3b8; padding: 2rem;">No words found for this category.</p>';
            return;
        }
        
        displayArea.innerHTML = words.map(word => `
            <div class="word-bubble ${this.explorerSelectedWords.some(w => w.word === word) ? 'selected' : ''}"
                 style="border-color: ${category.color}; color: ${category.color};"
                 onclick="app.toggleExplorerWord('${word}', '${categoryKey}')">
                ${word}
            </div>
        `).join('');
    },

    toggleExplorerWord(word, category) {
        const existingIndex = this.explorerSelectedWords.findIndex(w => w.word === word);
        
        if (existingIndex >= 0) {
            // Remove word
            this.explorerSelectedWords.splice(existingIndex, 1);
        } else {
            // Add word
            this.explorerSelectedWords.push({ word, category, timestamp: Date.now() });
        }
        
        // Update UI
        this.updateExplorerUI();
        this.displayExplorerWordsForCategory(this.explorerCurrentTab);
    },

    updateExplorerUI() {
        this.updateExplorerSelectedWordsList();
        this.updateExplorerStats();
        this.updateExplorerRibbon();
    },

    updateExplorerSelectedWordsList() {
        const selectedWordsList = document.querySelector('#explorer #selectedWordsList');
        
        if (this.explorerSelectedWords.length === 0) {
            selectedWordsList.innerHTML = '<span style="color: #94a3b8; font-size: 0.875rem;">No words selected yet...</span>';
            return;
        }
        
        selectedWordsList.innerHTML = this.explorerSelectedWords.map(item => {
            const category = this.explorerCategories[item.category];
            return `<span class="selected-word" style="background: ${category.color}20; color: ${category.color}; border: 1px solid ${category.color};">
                ${category.emoji} ${item.word}
                <i class="fas fa-times" onclick="app.toggleExplorerWord('${item.word}', '${item.category}')" style="cursor: pointer; margin-left: 0.25rem;"></i>
            </span>`;
        }).join('');
    },

    updateExplorerStats() {
        const totalSelected = this.explorerSelectedWords.length;
        const categoriesActive = new Set(this.explorerSelectedWords.map(w => w.category)).size;
        
        // Find dominant category
        const categoryCounts = {};
        this.explorerSelectedWords.forEach(w => {
            categoryCounts[w.category] = (categoryCounts[w.category] || 0) + 1;
        });
        
        const dominantCategory = Object.keys(categoryCounts).reduce((a, b) => 
            categoryCounts[a] > categoryCounts[b] ? a : b, Object.keys(categoryCounts)[0] || '-'
        );
        
        document.querySelector('#explorer #totalSelected').textContent = totalSelected;
        document.querySelector('#explorer #categoriesActive').textContent = categoriesActive;
        document.querySelector('#explorer #dominantCategory').textContent = 
            dominantCategory !== '-' ? this.explorerCategories[dominantCategory].emoji : '-';
    },

    updateExplorerRibbon() {
        const rainbowSvg = document.querySelector('#explorer #emotionRainbowSvg');
        if (!rainbowSvg || this.explorerSelectedWords.length === 0) {
            // Reset all bands to transparent
            for (let i = 1; i <= 3; i++) {
                const band = document.querySelector(`#explorer #rainbow-pair-${i}`);
                if (band) band.style.fill = 'transparent';
            }
            return;
        }
        
        // Group words by their band
        const wordsByBand = {};
        this.explorerSelectedWords.forEach(word => {
            const band = this.explorerCategoryToBand[word.category];
            if (!wordsByBand[band]) wordsByBand[band] = [];
            wordsByBand[band].push(word);
        });
        
        // Update each band with blended color
        for (let i = 1; i <= 3; i++) {
            const band = document.querySelector(`#explorer #rainbow-pair-${i}`);
            const bandWords = wordsByBand[`pair-${i}`] || [];
            
            if (bandWords.length === 0) {
                band.style.fill = 'transparent';
            } else if (bandWords.length === 1) {
                const category = bandWords[0].category;
                band.style.fill = this.explorerRainbowColors[category];
                band.style.opacity = '0.7';
            } else {
                // Blend colors toward white (additive mixing)
                const colors = bandWords.map(w => this.explorerRainbowColors[w.category]);
                const blendedColor = this.blendExplorerColorsTowardWhite(colors);
                band.style.fill = blendedColor;
                band.style.opacity = '0.8';
            }
        }
    },

    blendExplorerColorsTowardWhite(colors) {
        if (colors.length === 0) return 'transparent';
        if (colors.length === 1) return colors[0];
        
        // Convert hex to RGB and average
        const rgbColors = colors.map(hex => {
            const r = parseInt(hex.slice(1, 3), 16);
            const g = parseInt(hex.slice(3, 5), 16);
            const b = parseInt(hex.slice(5, 7), 16);
            return { r, g, b };
        });
        
        const avg = {
            r: Math.round(rgbColors.reduce((sum, c) => sum + c.r, 0) / rgbColors.length),
            g: Math.round(rgbColors.reduce((sum, c) => sum + c.g, 0) / rgbColors.length),
            b: Math.round(rgbColors.reduce((sum, c) => sum + c.b, 0) / rgbColors.length)
        };
        
        // Blend toward white (add 50% white)
        const blended = {
            r: Math.round(avg.r * 0.5 + 255 * 0.5),
            g: Math.round(avg.g * 0.5 + 255 * 0.5),
            b: Math.round(avg.b * 0.5 + 255 * 0.5)
        };
        
        return `#${blended.r.toString(16).padStart(2, '0')}${blended.g.toString(16).padStart(2, '0')}${blended.b.toString(16).padStart(2, '0')}`;
    },

    clearAllExplorerWords() {
        this.explorerSelectedWords = [];
        this.updateExplorerUI();
        this.displayExplorerWordsForCategory(this.explorerCurrentTab);
    },

    // Background color change for cycle - only on cycle page
    changeBackgroundColor(color, bgColor) {
        // Only apply dark mode on cycle tab
        if (this.currentTab !== 'cycle') return;
        
        // Clear any pending reset
        if (this.hoverTimeout) {
            clearTimeout(this.hoverTimeout);
            this.hoverTimeout = null;
        }
        
        // Only change if it's a different state
        if (this.currentHoverState === color) return;
        this.currentHoverState = color;
        
        // Create or update overlay
        let overlay = document.getElementById('cycle-bg-overlay');
        if (!overlay) {
            overlay = document.createElement('div');
            overlay.id = 'cycle-bg-overlay';
            overlay.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: radial-gradient(ellipse at center, ${bgColor} 0%, ${color}40 50%, #0a0a0a 100%);
                opacity: 0;
                transition: opacity 3s ease-in-out;
                pointer-events: none;
                z-index: -1;
            `;
            document.body.appendChild(overlay);
            // Force reflow
            overlay.offsetHeight;
        } else {
            overlay.style.background = `radial-gradient(ellipse at center, ${bgColor} 0%, ${color}40 50%, #0a0a0a 100%)`;
        }
        
        // Fade in
        requestAnimationFrame(() => {
            overlay.style.opacity = '1';
        });
    },

    resetBackgroundColor() {
        // Debounce the reset
        this.hoverTimeout = setTimeout(() => {
            this.currentHoverState = null;
            const overlay = document.getElementById('cycle-bg-overlay');
            if (overlay) {
                overlay.style.opacity = '0';
                // Remove after fade out
                setTimeout(() => {
                    if (overlay.parentNode) {
                        overlay.parentNode.removeChild(overlay);
                    }
                }, 10000);
            }
        }, 100);
    },

    // Backend API Configuration
    apiConfig: {
        baseUrl: '', // Empty for same-origin, or set to 'http://localhost:3000' for local dev
        useBackend: true // Set to true to use backend proxy, false for local analysis only
    },

    // AI Chat with Emotion Ribbon Integration
    sendMessage() {
        const input = document.getElementById('chatInput');
        const sanitizedMessage = this.security.sanitize(input.value);
        const validation = this.security.validate(sanitizedMessage);

        if (!validation.isValid) {
            alert(`Validation Error: ${validation.message}`);
            return;
        }

        if (!sanitizedMessage) return;

        // Add user message
        this.addChatMessage(message, 'user');
        input.value = '';

        // Store message for session journey
        this.chatMessages.push({ text: message, sender: 'user', timestamp: Date.now() });

        // Analyze with Emotion Ribbon (real-time)
        const ribbonAnalysis = this.analyzeWithRibbon(message);
        if (ribbonAnalysis && ribbonAnalysis.dominant) {
            this.updateEmotionSidebar(ribbonAnalysis);
        }

        // Show typing indicator
        this.showTypingIndicator();

        // Use backend API if configured
        if (this.apiConfig.useBackend) {
            this.callBackendAPI(message, ribbonAnalysis);
        } else {
            // Simulate AI analysis with local fallback
            setTimeout(() => {
                this.hideTypingIndicator();
                this.analyzeEmotionLocal(message);
            }, 1000);
        }
    },

    updateEmotionSidebar(analysis) {
        const { dominant } = analysis;
        if (!dominant) return;

        const stateEl = document.getElementById('detectedState');
        const scoreEl = document.getElementById('confidenceScore');
        
        if (stateEl && this.emotionRibbon) {
            const cat = this.emotionRibbon.categories[dominant[0]];
            stateEl.innerHTML = `
                <h4>Detected Emotion</h4>
                <div style="padding: 1rem; background: ${cat.color}20; border-radius: 0.5rem; border-left: 4px solid ${cat.color}">
                    <strong style="color: ${cat.color}">${cat.emoji} ${cat.name}</strong>
                    <p style="margin-top: 0.5rem; font-size: 0.875rem; color: #64748b">${cat.description}</p>
                    <p style="margin-top: 0.5rem; font-size: 0.75rem; color: #94a3b8">Words: ${dominant[1].words.slice(0, 3).join(', ')}</p>
                </div>
            `;
        }

        if (scoreEl) {
            scoreEl.innerHTML = `
                <h4>Confidence</h4>
                <div class="score-bar">
                    <div class="score-fill" style="width: ${dominant[1].confidence}%; background: ${this.emotionRibbon?.categories[dominant[0]]?.color || '#14b8a6'}"></div>
                </div>
                <span class="score-value">${dominant[1].confidence}%</span>
            `;
        }
    },

    showTypingIndicator() {
        const container = document.getElementById('chatMessages');
        if (!container) return;

        const div = document.createElement('div');
        div.className = 'message ai-message typing-indicator';
        div.id = 'typingIndicator';
        div.innerHTML = '<p><span class="dot"></span><span class="dot"></span><span class="dot"></span></p>';
        container.appendChild(div);
        container.scrollTop = container.scrollHeight;
    },

    hideTypingIndicator() {
        const indicator = document.getElementById('typingIndicator');
        if (indicator) indicator.remove();
    },

    async callBackendAPI(userMessage, ribbonAnalysis) {
        const apiUrl = this.apiConfig.baseUrl || '';
        
        try {
            const response = await fetch(`${apiUrl}/api/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ 
                    message: userMessage,
                    emotionContext: ribbonAnalysis
                })
            });

            this.hideTypingIndicator();

            if (!response.ok) {
                // If backend fails, try fallback endpoint
                if (response.status === 503) {
                    console.log('AI not configured on backend, using fallback');
                    return this.callFallbackAPI(userMessage);
                }
                throw new Error(`API error: ${response.status}`);
            }

            const data = await response.json();

            // Add AI response to chat
            this.addChatMessage(data.response, 'ai');
            this.chatMessages.push({ text: data.response, sender: 'ai', timestamp: Date.now() });

            // Update sidebar with detected state
            if (data.state && this.cycleStates[data.state]) {
                this.updateDetectedState(this.cycleStates[data.state], data.confidence || 85);
            }

            // Update ribbon with server emotions if different
            if (data.emotionRibbon && data.emotionRibbon.dominant) {
                const dom = data.emotionRibbon.dominant;
                if (this.ribbonVisualizer) {
                    this.ribbonVisualizer.addSegment(dom.category, dom.intensity);
                }
            }

        } catch (error) {
            console.error('Backend API error:', error);
            this.hideTypingIndicator();
            
            // Fallback to local analysis on error
            this.addChatMessage(
                "I'm having trouble connecting to the AI service. Let me analyze this locally for you.",
                'ai'
            );
            this.analyzeEmotionLocal(userMessage);
        }
    },

    async callFallbackAPI(userMessage) {
        const apiUrl = this.apiConfig.baseUrl || '';
        
        try {
            const response = await fetch(`${apiUrl}/api/chat-fallback`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: userMessage })
            });

            this.hideTypingIndicator();

            if (!response.ok) {
                throw new Error(`Fallback API error: ${response.status}`);
            }

            const data = await response.json();

            // Add AI response to chat
            this.addChatMessage(data.response, 'ai');

            // Update sidebar with detected state
            if (data.state && this.cycleStates[data.state]) {
                this.updateDetectedState(this.cycleStates[data.state], data.confidence || 70);
            }

        } catch (error) {
            console.error('Fallback API error:', error);
            this.hideTypingIndicator();
            this.analyzeEmotionLocal(userMessage);
        }
    },

    addChatMessage(text, sender) {
        const container = document.getElementById('chatMessages');
        if (!container) return;

        const div = document.createElement('div');
        div.className = `message ${sender}-message`;
        div.innerHTML = `<p>${text}</p>`;
        container.appendChild(div);
        container.scrollTop = container.scrollHeight;
    },

    analyzeEmotionLocal(text) {
        // Simple keyword-based analysis (fallback when API is not available)
        const lowerText = text.toLowerCase();
        let detectedState = 'emptiness';
        let confidence = 70;

        if (lowerText.includes('angry') || lowerText.includes('power') || lowerText.includes('control')) {
            detectedState = 'power';
            confidence = 85;
        } else if (lowerText.includes('want') || lowerText.includes('need') || lowerText.includes('crave')) {
            detectedState = 'craving';
            confidence = 80;
        } else if (lowerText.includes('lost') || lowerText.includes('failed') || lowerText.includes('rejected')) {
            detectedState = 'loss';
            confidence = 82;
        } else if (lowerText.includes('empty') || lowerText.includes('nothing') || lowerText.includes('numb')) {
            detectedState = 'emptiness';
            confidence = 88;
        }

        const state = this.cycleStates[detectedState];

        // AI response
        this.addChatMessage(
            `I hear you. It sounds like you might be in the <strong>${state.name}</strong> state. ` +
            `This is when ${state.description.toLowerCase()}. ` +
            `Would you like to try a ${state.strategies[0].toLowerCase()} exercise?`,
            'ai'
        );

        // Update sidebar
        this.updateDetectedState(state, confidence);
    },

    updateDetectedState(state, confidence) {
        const stateEl = document.getElementById('detectedState');
        const scoreEl = document.getElementById('confidenceScore');
        const actionsEl = document.getElementById('suggestedActions');

        if (stateEl) {
            stateEl.innerHTML = `
                <h4>Detected State</h4>
                <div style="padding: 1rem; background: ${state.color}20; border-radius: 0.5rem; border-left: 4px solid ${state.color}">
                    <strong style="color: ${state.color}">${state.name}</strong>
                    <p style="margin-top: 0.5rem; font-size: 0.875rem; color: #64748b">${state.description}</p>
                </div>
            `;
        }

        if (scoreEl) {
            scoreEl.innerHTML = `
                <h4>Confidence</h4>
                <div class="score-bar">
                    <div class="score-fill" style="width: ${confidence}%"></div>
                </div>
                <span class="score-value">${confidence}%</span>
            `;
        }

        if (actionsEl) {
            actionsEl.innerHTML = `
                <h4>Suggested Actions</h4>
                <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                    ${state.strategies.map(s => `
                        <button class="option-btn" onclick="app.startInterventionFromState('${s}')" style="text-align: left;">
                            ${s}
                        </button>
                    `).join('')}
                </div>
            `;
        }
    },

    startInterventionFromState(strategy) {
        // Map strategy to intervention
        const mapping = {
            'Values grounding': 'grounding',
            'Somatic anchoring': 'somatic',
            'Urge surfing': 'urgesurfing',
            'Pattern interruption': 'patternbreak'
        };
        
        const intervention = mapping[strategy] || 'sigh';
        this.startIntervention(intervention);
    },

    toggleVoiceInput() {
        alert('Voice input would use Web Speech API in production');
    },

    toggleLearnSection(header) {
        header.classList.toggle('active');
        const content = header.nextElementSibling;
        if (content) {
            if (header.classList.contains('active')) {
                content.style.maxHeight = content.scrollHeight + 'px';
            } else {
                content.style.maxHeight = '0';
            }
        }
    },

    startStructuredAssessment() {
        this.navigate('salad');
    },

    // Salad Check
    setupSaladCheck() {
        this.currentStep = 0;
        this.answers = {};
        this.renderSaladQuestion();
    },

    renderSaladQuestion() {
        const container = document.getElementById('saladQuestions');
        const totalSteps = this.spicyQuestions.length + this.greasyQuestions.length + this.vegetableQuestions.length;
        
        const progressEl = document.getElementById('saladProgress');
        const textEl = document.getElementById('saladProgressText');
        
        if (progressEl) progressEl.style.width = `${(this.currentStep / totalSteps) * 100}%`;
        if (textEl) textEl.textContent = `Question ${this.currentStep + 1} of ${totalSteps}`;

        if (!container) return;

        let question, category, color;
        if (this.currentStep < this.spicyQuestions.length) {
            question = this.spicyQuestions[this.currentStep];
            category = 'spicy';
            color = '#dc2626';
        } else if (this.currentStep < this.spicyQuestions.length + this.greasyQuestions.length) {
            question = this.greasyQuestions[this.currentStep - this.spicyQuestions.length];
            category = 'greasy';
            color = '#f97316';
        } else {
            question = this.vegetableQuestions[this.currentStep - this.spicyQuestions.length - this.greasyQuestions.length];
            category = 'vegetable';
            color = '#22c55e';
        }

        container.innerHTML = `
            <div class="question-card">
                <div class="question-category ${category}">${category}</div>
                <div class="question-text">${question.text}</div>
                <div class="options">
                    ${question.options.map(opt => `
                        <button class="option-btn ${this.answers[question.id] === opt ? 'selected' : ''}" onclick="app.selectSaladOption('${question.id}', '${opt}')">
                            ${opt}
                            <span class="check">✓</span>
                        </button>
                    `).join('')}
                </div>
                <div class="nav-buttons">
                    ${this.currentStep > 0 ? `<button class="btn-secondary" onclick="app.prevSaladStep()">Previous</button>` : '<div></div>'}
                    <button class="btn-primary" onclick="app.nextSaladStep()">${this.currentStep < totalSteps - 1 ? 'Next' : 'See Results'}</button>
                </div>
            </div>
        `;
    },

    selectSaladOption(questionId, option) {
        this.answers[questionId] = option;
        this.renderSaladQuestion();
    },

    nextSaladStep() {
        const totalSteps = this.spicyQuestions.length + this.greasyQuestions.length + this.vegetableQuestions.length;
        
        if (this.currentStep < totalSteps - 1) {
            this.currentStep++;
            this.renderSaladQuestion();
        } else {
            this.showSaladResults();
        }
    },

    prevSaladStep() {
        if (this.currentStep > 0) {
            this.currentStep--;
            this.renderSaladQuestion();
        }
    },

    showSaladResults() {
        document.getElementById('saladQuestions').classList.add('hidden');
        document.getElementById('saladResults').classList.remove('hidden');
        
        const spice = this.answers['emotion_now'] || '';
        const grease = this.answers['greasy_food'] || '';
        const vegetable = this.answers['add_vegetable'] || '';
        
        // Save checkin
        const checkins = JSON.parse(localStorage.getItem('checkins') || '[]');
        checkins.push({
            date: new Date().toISOString(),
            spice,
            grease,
            vegetable,
            answers: this.answers
        });
        localStorage.setItem('checkins', JSON.stringify(checkins));
        
        // Render plate
        const plateEl = document.getElementById('plateContent');
        if (plateEl) {
            plateEl.innerHTML = `
                ${spice ? `
                    <div class="result-item spicy">
                        <div class="result-icon">🔥</div>
                        <div class="result-content">
                            <h4>Spicy</h4>
                            <p><strong>${spice}</strong></p>
                            <p>This is what is overwhelming you right now.</p>
                        </div>
                    </div>
                ` : ''}
                ${grease ? `
                    <div class="result-item greasy">
                        <div class="result-icon">🧈</div>
                        <div class="result-content">
                            <h4>Greasy</h4>
                            <p><strong>${grease}</strong></p>
                            <p>This is what you are reaching for to cope.</p>
                        </div>
                    </div>
                ` : ''}
                ${vegetable ? `
                    <div class="result-item vegetable">
                        <div class="result-icon">🥗</div>
                        <div class="result-content">
                            <h4>Vegetable</h4>
                            <p><strong>${vegetable}</strong></p>
                            <p>This is what would actually nourish you.</p>
                        </div>
                    </div>
                ` : ''}
            `;
        }
        
        // Render protocol
        const protocolEl = document.getElementById('protocolSteps');
        if (protocolEl) {
            protocolEl.innerHTML = [
                { title: 'Stop', desc: 'Physically pause. Do not act. Take one slow breath.' },
                { title: 'Name the Spiciness', desc: `What is too spicy? "${spice || 'Powerlessness'}"` },
                { title: 'Locate It', desc: 'Where do you feel this in your body? Just notice.' },
                { title: 'Identify the Craving', desc: `What are you reaching for? "${grease || 'External validation'}"` },
                { title: 'Choose a Vegetable', desc: `What would nourish you? "${vegetable || 'Rest'}"` },
                { title: 'Take Action', desc: 'Do it for just 2 minutes.' },
                { title: 'Notice', desc: 'How do you feel? Not perfect, just different.' }
            ].map((step, i) => `
                <div class="protocol-step">
                    <div class="step-number">${i + 1}</div>
                    <div class="step-content">
                        <h4>${step.title}</h4>
                        <p>${step.desc}</p>
                    </div>
                </div>
            `).join('');
        }
        
        this.renderStreak();
    },

    resetSalad() {
        this.currentStep = 0;
        this.answers = {};
        document.getElementById('saladQuestions').classList.remove('hidden');
        document.getElementById('saladResults').classList.add('hidden');
        this.renderSaladQuestion();
    },

    // Interventions
    startIntervention(type) {
        const intervention = this.interventions[type];
        if (!intervention) return;

        this.currentIntervention = type;
        document.getElementById('interventionModal').classList.remove('hidden');
        document.getElementById('interventionTitle').textContent = intervention.name;
        document.getElementById('interventionInstructions').textContent = intervention.instructions;
        
        this.timerSeconds = intervention.duration;
        this.timerTotal = intervention.duration;
        this.isRunning = false;
        this.updateInterventionTimer();
        
        // Update play button
        const btn = document.getElementById('playPauseBtn');
        if (btn) btn.innerHTML = '<i class="fas fa-play"></i>';
    },

    toggleIntervention() {
        this.isRunning = !this.isRunning;
        const btn = document.getElementById('playPauseBtn');
        
        if (this.isRunning) {
            if (btn) btn.innerHTML = '<i class="fas fa-pause"></i>';
            this.timerInterval = setInterval(() => {
                this.timerSeconds--;
                this.updateInterventionTimer();
                
                if (this.timerSeconds <= 0) {
                    this.completeIntervention();
                }
            }, 1000);
        } else {
            if (btn) btn.innerHTML = '<i class="fas fa-play"></i>';
            clearInterval(this.timerInterval);
        }
    },

    updateInterventionTimer() {
        const display = document.getElementById('interventionTimer');
        const circle = document.getElementById('interventionProgress');
        
        if (display) {
            const minutes = Math.floor(this.timerSeconds / 60);
            const seconds = this.timerSeconds % 60;
            display.textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
        }
        
        if (circle) {
            const progress = (this.timerTotal - this.timerSeconds) / this.timerTotal;
            const offset = 283 - (283 * progress);
            circle.style.strokeDashoffset = offset;
        }
    },

    stopIntervention() {
        clearInterval(this.timerInterval);
        this.isRunning = false;
        document.getElementById('interventionModal').classList.add('hidden');
    },

    completeIntervention() {
        clearInterval(this.timerInterval);
        this.isRunning = false;
        
        // Save session
        const sessions = JSON.parse(localStorage.getItem('sessions') || '[]');
        sessions.push({
            date: new Date().toISOString(),
            type: this.currentIntervention,
            duration: this.interventions[this.currentIntervention].duration
        });
        localStorage.setItem('sessions', JSON.stringify(sessions));
        
        alert('Exercise complete! 🎉 Great job taking care of yourself.');
        document.getElementById('interventionModal').classList.add('hidden');
        this.renderStreak();
    },

    // Journal
    logMood(mood) {
        localStorage.setItem('todayMood', mood);
        document.querySelectorAll('.mood-btn').forEach(btn => {
            btn.classList.toggle('selected', parseInt(btn.dataset.mood) === mood);
        });
    },

    newJournalPrompt() {
        const prompt = this.journalPrompts[Math.floor(Math.random() * this.journalPrompts.length)];
        const el = document.getElementById('journalPrompt');
        if (el) el.textContent = prompt;
    },

    saveJournalEntry() {
        const content = document.getElementById('journalText');
        const sanitizedContent = this.security.sanitize(content.value);
        const validation = this.security.validate(sanitizedContent, 10000); // Larger max length for journal

        if (!validation.isValid) {
            alert(`Validation Error: ${validation.message}`);
            return;
        }

        if (!sanitizedContent) return;
        
        const entries = JSON.parse(localStorage.getItem('journalEntries') || '[]');
        entries.unshift({
            date: new Date().toISOString(),
            title: 'Journal Entry',
            content: content.value,
            mood: localStorage.getItem('todayMood') || 3
        });
        localStorage.setItem('journalEntries', JSON.stringify(entries));
        
        content.value = '';
        this.renderJournalEntries();
    },

    renderJournalEntries() {
        const container = document.getElementById('journalEntries');
        if (!container) return;
        
        const entries = JSON.parse(localStorage.getItem('journalEntries') || '[]');
        const moods = ['', '😢', '😕', '😐', '🙂', '😊'];
        
        container.innerHTML = entries.slice(0, 5).map(entry => `
            <div class="journal-entry">
                <div class="mood">${moods[entry.mood] || '📝'}</div>
                <div class="journal-entry-content">
                    <h4>${entry.title}</h4>
                    <p>${entry.content.substring(0, 100)}${entry.content.length > 100 ? '...' : ''}</p>
                    <small>${new Date(entry.date).toLocaleDateString()}</small>
                </div>
            </div>
        `).join('');
    },

    // Progress
    renderProgress() {
        const sessions = JSON.parse(localStorage.getItem('sessions') || '[]');
        const checkins = JSON.parse(localStorage.getItem('checkins') || '[]');
        
        const totalSessions = sessions.length + checkins.length;
        const totalMinutes = sessions.reduce((sum, s) => sum + (s.duration || 0), 0) + (checkins.length * 5);
        
        const streakEl = document.getElementById('progressStreak');
        const sessionsEl = document.getElementById('progressSessions');
        const minutesEl = document.getElementById('progressMinutes');
        
        if (streakEl) streakEl.textContent = this.getStreak();
        if (sessionsEl) sessionsEl.textContent = totalSessions;
        if (minutesEl) minutesEl.textContent = totalMinutes;
        
        this.renderWeeklyChart();
        this.renderAchievements(totalSessions, totalMinutes);
        
        // Render Emotion Ribbon journey if available
        this.renderEmotionJourney();
    },

    renderEmotionJourney() {
        const container = document.getElementById('insightsList');
        if (!container) return;

        // Get chat history emotions
        if (!this.emotionRibbon || this.emotionRibbon.sessionHistory.length === 0) {
            container.innerHTML = '<p style="color: #64748b; font-size: 0.875rem;">Complete an AI chat session to see your emotional journey.</p>';
            return;
        }

        const journey = this.emotionRibbon.getSessionJourney();
        if (!journey) return;

        container.innerHTML = `
            <div class="emotion-journey">
                <h4>Session Emotional Journey</h4>
                <div class="journey-stats">
                    <div class="journey-stat">
                        <span class="stat-label">Messages analyzed:</span>
                        <span class="stat-value">${journey.totalMessages}</span>
                    </div>
                    <div class="journey-stat">
                        <span class="stat-label">Dominant emotion:</span>
                        <span class="stat-value" style="color: ${this.emotionRibbon.categories[journey.dominantEmotion]?.color || '#64748b'}">
                            ${this.emotionRibbon.categories[journey.dominantEmotion]?.emoji || ''} ${journey.dominantEmotion || 'None'}
                        </span>
                    </div>
                </div>
                <div class="journey-timeline">
                    ${journey.timeline.slice(-5).map(t => `
                        <div class="timeline-item">
                            <span class="time">${t.time}</span>
                            <span class="emotions">
                                ${t.emotions.map(e => `<span style="color: ${e.color}">${e.emoji}</span>`).join(' ')}
                            </span>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    },

    renderWeeklyChart() {
        const ctx = document.getElementById('weeklyChart');
        if (!ctx || typeof Chart === 'undefined') return;
        
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                datasets: [{
                    label: 'Minutes',
                    data: [15, 30, 10, 45, 20, 60, 25],
                    backgroundColor: '#14b8a6',
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: { beginAtZero: true }
                }
            }
        });
    },

    renderAchievements(sessions, minutes) {
        const container = document.getElementById('achievementsList');
        if (!container) return;
        
        const achievements = [
            { icon: '✨', name: 'First Step', unlocked: sessions >= 1 },
            { icon: '🥗', name: 'Salad Master', unlocked: sessions >= 5 },
            { icon: '🔥', name: 'On Fire', unlocked: this.getStreak() >= 7 },
            { icon: '⏱️', name: 'Time Master', unlocked: minutes >= 100 },
            { icon: '❤️', name: 'Self-Compassion', unlocked: sessions >= 3 },
            { icon: '🎨', name: 'Emotion Explorer', unlocked: this.emotionRibbon?.sessionHistory?.length >= 5 },
            { icon: '⏸️', name: 'The Pause', unlocked: sessions >= 10 }
        ];
        
        container.innerHTML = achievements.map(a => `
            <div class="achievement ${a.unlocked ? 'unlocked' : ''}">
                <div class="achievement-icon">${a.icon}</div>
                <div class="achievement-name">${a.name}</div>
            </div>
        `).join('');
    },

    loadData() {
        const mood = localStorage.getItem('todayMood');
        if (mood) this.logMood(parseInt(mood));
        this.renderJournalEntries();
    },

    // Balance Tool Functions
    renderBalance() {
        const balanceContainer = document.getElementById('balance');
        if (!balanceContainer) {
            setTimeout(() => this.renderBalance(), 100);
            return;
        }

        balanceContainer.innerHTML = `
            <h2>Balance</h2>
            <div class="emotion-balance-container">
                <div class="balance-card">
                    <div class="balance-header">
                        <h1>⚡ Emotion Balance Tool</h1>
                        <p class="subtitle">Check in. Get balanced. Move forward.</p>
                    </div>
                    
                    <div id="quiz-section">
                        <div class="slider-question">
                            <label>1. Energy Level</label>
                            <div class="slider-container">
                                <input type="range" id="energy" class="slider-track" min="1" max="10" value="5" oninput="app.updateBalanceValue('energy', this.value)">
                                <div class="slider-labels">
                                    <span>Drained</span>
                                    <span>Balanced</span>
                                    <span>Hyper</span>
                                </div>
                                <div class="slider-value" id="energy-val">5</div>
                            </div>
                        </div>
                        
                        <div class="slider-question">
                            <label>2. Mental Clarity</label>
                            <div class="slider-container">
                                <input type="range" id="clarity" class="slider-track" min="1" max="10" value="5" oninput="app.updateBalanceValue('clarity', this.value)">
                                <div class="slider-labels">
                                    <span>Foggy</span>
                                    <span>Clear</span>
                                    <span>Sharp</span>
                                </div>
                                <div class="slider-value" id="clarity-val">5</div>
                            </div>
                        </div>
                        
                        <div class="slider-question">
                            <label>3. Emotional Stability</label>
                            <div class="slider-container">
                                <input type="range" id="stability" class="slider-track" min="1" max="10" value="5" oninput="app.updateBalanceValue('stability', this.value)">
                                <div class="slider-labels">
                                    <span>Volatile</span>
                                    <span>Steady</span>
                                    <span>Centered</span>
                                </div>
                                <div class="slider-value" id="stability-val">5</div>
                            </div>
                        </div>
                        
                        <div class="slider-question">
                            <label>4. Stress Level</label>
                            <div class="slider-container">
                                <input type="range" id="stress" class="slider-track" min="1" max="10" value="5" oninput="app.updateBalanceValue('stress', this.value)">
                                <div class="slider-labels">
                                    <span>Calm</span>
                                    <span>Manageable</span>
                                    <span>Overwhelmed</span>
                                </div>
                                <div class="slider-value" id="stress-val">5</div>
                            </div>
                        </div>
                        
                        <button class="analyze-btn" onclick="app.calculateBalanceState()">
                            Analyze My State
                        </button>
                    </div>
                    
                    <div id="result-section" style="display: none;">
                        <div class="result-section">
                            <div class="score-display">
                                <div class="score-circle" id="score-circle">
                                    <span id="score-text">--</span>
                                </div>
                                <div class="state-info">
                                    <h3 class="state-title" id="state-title">Calculating...</h3>
                                    <p class="state-description" id="state-description"></p>
                                </div>
                            </div>
                            
                            <div class="advice-section">
                                <h4>Personalized Recommendations</h4>
                                <div class="advice-list" id="advice-list"></div>
                            </div>
                            
                            <div class="quick-actions-section">
                                <h4>Quick Actions</h4>
                                <div class="action-grid">
                                    <button class="action-btn grounding-btn" onclick="app.groundingExercise()">
                                        <i class="fas fa-feather"></i>
                                        Grounding
                                    </button>
                                    <button class="action-btn breathing-btn" onclick="app.showBreathing()">
                                        <i class="fas fa-wind"></i>
                                        Breathing
                                    </button>
                                    <button class="action-btn reset-btn" onclick="app.resetBalanceTool()">
                                        <i class="fas fa-redo"></i>
                                        Reset
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="breathing-exercise" id="breathing-exercise" style="display: none;">
                    <h3>Breathing Exercise</h3>
                    <div class="breathing-circle" id="breathing-circle"></div>
                    <p id="breathing-text">Breathe in...</p>
                    <button class="btn" onclick="app.hideBreathing()">Stop Exercise</button>
                </div>
            </div>`;
    },

    updateBalanceValue(id, value) {
        const valEl = document.getElementById(id + '-val');
        if (valEl) valEl.textContent = value;
    },

    calculateBalanceState() {
        const energy = parseInt(document.getElementById('energy').value);
        const clarity = parseInt(document.getElementById('clarity').value);
        const stability = parseInt(document.getElementById('stability').value);
        const stress = parseInt(document.getElementById('stress').value);
        
        // Calculate balance score (stress is inverted)
        const balanceScore = Math.round((energy + clarity + stability + (11 - stress)) / 4 * 10);
        
        // Determine state
        let state, color, desc, advice;
        
        if (balanceScore >= 80) {
            state = "⚡ Peak State";
            color = "#50c8b8";
            desc = "You're in a strong position. Channel this energy into meaningful work.";
            advice = [
                "Tackle your most important task now — you're sharp",
                "Document what's working so you can replicate it",
                "Help someone else — your clarity is contagious",
                "Set a boundary: protect this state from interruptions"
            ];
        } else if (balanceScore >= 60) {
            state = "🌊 Balanced Flow";
            color = "#4a90d9";
            desc = "Good equilibrium. Small adjustments will optimize your day.";
            advice = [
                "Take a 5-minute walk to maintain momentum",
                "Drink water — hydration affects clarity more than you think",
                "Do one thing that moves your main goal forward",
                "Check in with yourself again in 2 hours"
            ];
        } else if (balanceScore >= 40) {
            state = "🌫️ Drift Mode";
            color = "#f5a623";
            desc = "You're functional but not firing on all cylinders. Time to recalibrate.";
            advice = [
                "Close all tabs except the one you need right now",
                "Do a 2-minute body scan — where are you holding tension?",
                "Eat something with protein if you haven't recently",
                "Lower the bar: what's the smallest next step you can take?"
            ];
        } else {
            state = "⛈️ Storm Mode";
            color = "#e74c3c";
            desc = "Your system needs care before productivity. Recovery first.";
            advice = [
                "Step away from the screen for 10 minutes minimum",
                "Name three things you can see, hear, and feel (grounding)",
                "Text someone you trust: 'Having a rough moment'",
                "Ask: what's the kindest thing I could do for myself right now?",
                "Consider postponing non-urgent tasks until tomorrow"
            ];
        }
        
        // Display results
        const resultDiv = document.getElementById('result-section');
        const scoreCircle = document.getElementById('score-circle');
        const stateTitle = document.getElementById('state-title');
        
        if (scoreCircle) {
            scoreCircle.textContent = balanceScore;
            scoreCircle.style.setProperty('--score-color', color);
            scoreCircle.style.setProperty('--score-deg', (balanceScore * 3.6) + 'deg');
        }
        
        if (stateTitle) {
            stateTitle.textContent = state;
            stateTitle.style.setProperty('--score-color', color);
        }
        
        const stateDesc = document.getElementById('state-desc');
        if (stateDesc) stateDesc.textContent = desc;
        
        const adviceList = document.getElementById('advice-list');
        if (adviceList) adviceList.innerHTML = advice.map(a => `<li>${a}</li>`).join('');
        
        const quizSection = document.getElementById('quiz-section');
        if (quizSection) quizSection.style.display = 'none';
        
        if (resultDiv) resultDiv.classList.add('show');
        
        // Scroll to results
        if (resultDiv) {
            resultDiv.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    },

    showBreathing() {
        const breathingSection = document.getElementById('breathing-section');
        if (breathingSection) breathingSection.classList.add('show');
    },

    hideBreathing() {
        const breathingSection = document.getElementById('breathing-section');
        if (breathingSection) breathingSection.classList.remove('show');
    },

    groundingExercise() {
        alert(`5-4-3-2-1 Grounding Exercise:

👁️ 5 things you can SEE
👂 4 things you can HEAR
✋ 3 things you can TOUCH
👃 2 things you can SMELL
👅 1 thing you can TASTE

Take your time. Come back to now.`);
    },

    resetBalanceTool() {
        const energy = document.getElementById('energy');
        const clarity = document.getElementById('clarity');
        const stability = document.getElementById('stability');
        const stress = document.getElementById('stress');
        
        if (energy) energy.value = 5;
        if (clarity) clarity.value = 5;
        if (stability) stability.value = 5;
        if (stress) stress.value = 5;
        
        ['energy', 'clarity', 'stability', 'stress'].forEach(id => {
            const valEl = document.getElementById(id + '-val');
            if (valEl) valEl.textContent = '5';
        });
    },

    renderCompass() {
        const compassContainer = document.getElementById('compassContainer');
        if (!compassContainer) {
            setTimeout(() => this.renderCompass(), 100);
            return;
        }

        compassContainer.innerHTML = `
            <div class="compass-container">
                <div class="compass-card">
                    <div class="compass-header">
                        <h1>🧭 Salad Plate Compass</h1>
                        <p class="subtitle">Your personal emotional navigation tool</p>
                    </div>
                    
                    <div class="compass-instructions">
                        <h3>How to Use This Compass</h3>
                        <ol>
                            <li><strong>Identify your state:</strong> Look at the table below and find where you are right now.</li>
                            <li><strong>Find the missing vegetable:</strong> Each state has a "missing vegetable" that brings balance.</li>
                            <li><strong>Take one action:</strong> Do the suggested action to add that vegetable to your plate.</li>
                        </ol>
                    </div>
                    
                    <!-- The Compass Table -->
                    <table class="compass-table">
                        <thead>
                            <tr>
                                <th>Your State</th>
                                <th>How It Feels</th>
                                <th>Quick Self-Check</th>
                                <th>The Missing Vegetable</th>
                                <th>One Action to Balance</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>
                                    <span class="state-badge state-power">
                                        <i class="fas fa-bolt"></i> Power
                                    </span>
                                </td>
                                <td>Excited, happy, optimistic</td>
                                <td class="self-check">"Am I riding high?"</td>
                                <td class="missing-veg">Connection</td>
                                <td class="action-cell">Share your excitement with someone you trust—without needing anything back.</td>
                            </tr>
                            <tr>
                                <td>
                                    <span class="state-badge state-possession">
                                        <i class="fas fa-hand-holding"></i> Possession
                                    </span>
                                </td>
                                <td>Satisfied, full, occupied</td>
                                <td class="self-check">"Am I holding onto something too tightly?"</td>
                                <td class="missing-veg">Release</td>
                                <td class="action-cell">Let go of one small thing—a plan, an opinion, a need to control. Notice how it feels.</td>
                            </tr>
                            <tr>
                                <td>
                                    <span class="state-badge state-loss">
                                        <i class="fas fa-heart-broken"></i> Loss
                                    </span>
                                </td>
                                <td>Disappointed, frustrated, powerless</td>
                                <td class="self-check">"Did something slip away?"</td>
                                <td class="missing-veg">Grieve</td>
                                <td class="action-cell">Sit for 3 minutes and just name what you lost. No fixing. Just naming.</td>
                            </tr>
                            <tr>
                                <td>
                                    <span class="state-badge state-emptiness">
                                        <i class="fas fa-circle"></i> Emptiness
                                    </span>
                                </td>
                                <td>Unrestful, slightly panicked, mindless</td>
                                <td class="self-check">"Is there a hollow feeling?"</td>
                                <td class="missing-veg">Ground</td>
                                <td class="action-cell"><strong>5-4-3-2-1 grounding:</strong> 5 things you see, 4 you touch, 3 you hear, 2 you smell, 1 you taste.</td>
                            </tr>
                            <tr>
                                <td>
                                    <span class="state-badge state-crave">
                                        <i class="fas fa-fire"></i> Crave
                                    </span>
                                </td>
                                <td>Like eating something—urgent, hungry</td>
                                <td class="self-check">"What am I hungry for right now?"</td>
                                <td class="missing-veg">Pause</td>
                                <td class="action-cell">Wait 10 minutes before acting. Notice the urge in your body. Don't feed it—just watch it.</td>
                            </tr>
                        </tbody>
                    </table>
                    
                    <!-- Color Key -->
                    <div class="color-key">
                        <h3><i class="fas fa-palette"></i> Color Quick Reference</h3>
                        <p style="color: #888; margin-bottom: 20px;">Assign colors to make recognition even faster. When you feel "a lot of red"—you know you need the pause.</p>
                        
                        <div class="color-grid">
                            <div class="color-item">
                                <div class="color-dot color-power"></div>
                                <div>
                                    <strong style="color: #ffd700;">Power</strong>
                                    <div style="font-size: 0.85rem; color: #888;">Gold / Yellow</div>
                                </div>
                            </div>
                            <div class="color-item">
                                <div class="color-dot color-possession"></div>
                                <div>
                                    <strong style="color: #ff6b35;">Possession</strong>
                                    <div style="font-size: 0.85rem; color: #888;">Deep Orange</div>
                                </div>
                            </div>
                            <div class="color-item">
                                <div class="color-dot color-loss"></div>
                                <div>
                                    <strong style="color: #a0a0a0;">Loss</strong>
                                    <div style="font-size: 0.85rem; color: #888;">Dark Gray</div>
                                </div>
                            </div>
                            <div class="color-item">
                                <div class="color-dot color-emptiness"></div>
                                <div>
                                    <strong style="color: #c0c0c0;">Emptiness</strong>
                                    <div style="font-size: 0.85rem; color: #888;">Light Gray / Pale Blue</div>
                                </div>
                            </div>
                            <div class="color-item">
                                <div class="color-dot color-crave"></div>
                                <div>
                                    <strong style="color: #dc143c;">Crave</strong>
                                    <div style="font-size: 0.85rem; color: #888;">Deep Red</div>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Why This Works -->
                    <div class="why-works">
                        <h3><i class="fas fa-lightbulb"></i> Why This Works</h3>
                        <ul>
                            <li>It uses <strong>your words</strong>, not clinical terms.</li>
                            <li>It's <strong>fast</strong>—one glance, one action.</li>
                            <li>It's built on <strong>your own salad plate metaphor</strong> (spicy emotions, missing vegetables, balancing actions).</li>
                            <li>It gives you <strong>agency</strong>—you're not just reacting; you're choosing a different vegetable.</li>
                        </ul>
                    </div>
                    
                    <!-- Quick Access Buttons -->
                    <div class="quick-access">
                        <a href="#" onclick="app.navigate('salad')" class="quick-access-btn">
                            <i class="fas fa-clipboard-check"></i> Take the Full Salad Check
                        </a>
                    </div>
                </div>
            </div>
        `;
    },

    resetBalanceAll() {
        const resultSection = document.getElementById('result-section');
        const quizSection = document.getElementById('quiz-section');
        
        if (resultSection) resultSection.classList.remove('show');
        if (quizSection) quizSection.style.display = 'block';
        
        this.hideBreathing();
        this.resetBalanceTool();
        
        // Scroll back to top
        const balanceCard = document.querySelector('.balance-card');
        if (balanceCard) {
            balanceCard.scrollIntoView({ behavior: 'smooth' });
        }
    },

    // Copyright protection - show privacy policy
    showPrivacyPolicy() {
        alert('Privacy Policy:\n\n' +
            '© 2026 Mindfulness Therapy. All rights reserved.\n\n' +
            'Your data is stored locally on your device.\n' +
            'We do not collect or share personal information.\n' +
            'All journal entries and progress data remain private.');
    },

    // Copyright protection - show terms
    showTerms() {
        alert('Terms of Use:\n\n' +
            '© 2026 Mindfulness Therapy. All rights reserved.\n\n' +
            'This application is for personal use only.\n' +
            'Unauthorized copying, distribution, or modification is prohibited.\n' +
            'The content and design are protected by copyright law.');
    }
};

// Copyright Protection - Disable right-click and certain keyboard shortcuts
document.addEventListener('contextmenu', (e) => {
    e.preventDefault();
    return false;
});

document.addEventListener('keydown', (e) => {
    // Disable F12, Ctrl+Shift+I, Ctrl+U
    if (e.key === 'F12' || 
        (e.ctrlKey && e.shiftKey && e.key === 'I') ||
        (e.ctrlKey && e.key === 'u')) {
        e.preventDefault();
        return false;
    }
});

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    app.init();
});

// Learn section toggle function
function toggleLearnSection(header) {
    header.classList.toggle('active');
}
