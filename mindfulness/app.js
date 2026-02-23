// Mindfulness Therapy - Enhanced JavaScript
// Features: Power-Possession Cycle, AI Assessment, Micro-Interventions, Emotion Ribbon
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

    // Power-Possession Cycle Data
    cycleStates: {
        power: {
            name: 'Power',
            color: '#991b1b',
            bgColor: '#450a0a',
            description: 'External validation, feeling in control',
            triggers: ['Achievement', 'Recognition', 'Status gain'],
            strategies: ['Values grounding', 'Internal validation', 'Preventive balance']
        },
        possession: {
            name: 'Possession',
            color: '#6b21a8',
            bgColor: '#3b0764',
            description: 'Owning phase, attachment to external power',
            triggers: ['Control behaviors', 'Territoriality', 'Acquisition'],
            strategies: ['Letting go practice', 'Non-attachment', 'Impermanence awareness']
        },
        loss: {
            name: 'Loss',
            color: '#1e40af',
            bgColor: '#172554',
            description: 'Inevitable decline, external power fading',
            triggers: ['Status loss', 'Rejection', 'Failure'],
            strategies: ['Acceptance', 'Grief processing', 'Reality orientation']
        },
        emptiness: {
            name: 'Emptiness',
            color: '#374151',
            bgColor: '#111827',
            description: 'Collapse, void when external validation gone',
            triggers: ['Isolation', 'Meaninglessness', 'Disconnection'],
            strategies: ['Somatic anchoring', 'Presence', 'Self-compassion']
        },
        craving: {
            name: 'Craving',
            color: '#b45309',
            bgColor: '#451a03',
            description: 'Compulsive urge for substitute satisfaction',
            triggers: ['Emptiness', 'Boredom', 'Restlessness'],
            strategies: ['Urge surfing', 'Pattern interruption', 'Alternative satisfaction']
        },
        return: {
            name: 'Return',
            color: '#15803d',
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
    },

    // Initialize Emotion Ribbon
    initEmotionRibbon() {
        // Create ribbon container if on assessment page
        const chatInterface = document.querySelector('.chat-interface');
        if (chatInterface && typeof EmotionRibbon !== 'undefined') {
            // Insert ribbon before chat interface
            const ribbonContainer = document.createElement('div');
            ribbonContainer.id = 'emotionRibbonContainer';
            ribbonContainer.className = 'emotion-ribbon-container';
            ribbonContainer.innerHTML = `
                <div class="ribbon-header">
                    <span class="ribbon-title">🎨 Emotion Ribbon</span>
                    <span class="ribbon-subtitle">Real-time emotional awareness</span>
                </div>
                <div id="ribbonVisualization"></div>
            `;
            chatInterface.parentNode.insertBefore(ribbonContainer, chatInterface);
            
            // Initialize visualizer
            if (typeof EmotionRibbonVisualizer !== 'undefined') {
                this.emotionRibbonVisualizer = new EmotionRibbonVisualizer('ribbonVisualization', {
                    width: 600,
                    height: 100,
                    maxSegments: 8
                });
            }
        }
        
        // Add styles
        const style = document.createElement('style');
        style.textContent = `
            .emotion-ribbon-container {
                background: white;
                border-radius: 1rem;
                padding: 1rem 1.5rem;
                margin-bottom: 1.5rem;
                box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
                border: 1px solid #e2e8f0;
            }
            .ribbon-header {
                display: flex;
                align-items: center;
                gap: 0.75rem;
                margin-bottom: 0.75rem;
            }
            .ribbon-title {
                font-weight: 600;
                color: #1e293b;
            }
            .ribbon-subtitle {
                font-size: 0.75rem;
                color: #64748b;
            }
            #ribbonVisualization {
                min-height: 80px;
            }
            .emotion-journey-btn {
                margin-top: 1rem;
                padding: 0.5rem 1rem;
                background: linear-gradient(135deg, #14b8a6, #0d9488);
                color: white;
                border: none;
                border-radius: 9999px;
                font-size: 0.875rem;
                cursor: pointer;
                transition: all 0.2s;
            }
            .emotion-journey-btn:hover {
                transform: translateY(-1px);
                box-shadow: 0 4px 12px rgba(20, 184, 166, 0.3);
            }
        `;
        document.head.appendChild(style);
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
                    <text x="${x}" y="${y + 12}" text-anchor="middle" font-size="18">${['🔥', '💜', '💙', '⚪', '🟠', '🟢'][i]}</text>
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

    // Emotion Ribbon Visualizer
    emotionRibbonVisualizer: null,
    sessionEmotions: [],

    // Backend API Configuration
    apiConfig: {
        baseUrl: '', // Empty for same-origin, or set to 'http://localhost:3000' for local dev
        useBackend: true // Set to true to use backend proxy, false for local analysis only
    },

    // AI Chat
    sendMessage() {
        const input = document.getElementById('chatInput');
        const message = input.value.trim();
        if (!message) return;

        // Add user message
        this.addChatMessage(message, 'user');
        input.value = '';

        // Analyze emotions locally first for real-time ribbon
        if (typeof EmotionRibbon !== 'undefined') {
            const analysis = EmotionRibbon.analyze(message);
            if (analysis.detected && Object.keys(analysis.detected).length > 0) {
                // Update ribbon
                if (this.emotionRibbonVisualizer) {
                    this.emotionRibbonVisualizer.updateFromAnalysis(analysis);
                }
                // Store for session
                this.sessionEmotions.push({
                    timestamp: Date.now(),
                    message: message.substring(0, 100),
                    emotions: analysis.detected
                });
            }
        }

        // Show typing indicator
        this.showTypingIndicator();

        // Use backend API if configured, otherwise fallback to local analysis
        if (this.apiConfig.useBackend) {
            this.callBackendAPI(message);
        } else {
            // Simulate AI analysis with local fallback
            setTimeout(() => {
                this.hideTypingIndicator();
                this.analyzeEmotionLocal(message);
            }, 1000);
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

    async callBackendAPI(userMessage) {
        const apiUrl = this.apiConfig.baseUrl || '';
        
        try {
            const response = await fetch(`${apiUrl}/api/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: userMessage, includeEmotions: true })
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

            // Update ribbon with server-side emotion analysis if available
            if (data.emotionRibbon) {
                this.updateEmotionRibbonFromServer(data.emotionRibbon);
            }

            // Update sidebar with detected state
            if (data.state && this.cycleStates[data.state]) {
                this.updateDetectedState(this.cycleStates[data.state], data.confidence || 85);
            }

            // Store emotion data
            if (data.emotions) {
                this.sessionEmotions.push({
                    timestamp: Date.now(),
                    message: userMessage.substring(0, 100),
                    emotions: data.emotions,
                    aiDetected: data.state
                });
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

    // Update ribbon from server analysis
    updateEmotionRibbonFromServer(emotionRibbon) {
        if (!this.emotionRibbonVisualizer || !emotionRibbon) return;
        
        // Add all detected emotions from server
        if (emotionRibbon.all) {
            emotionRibbon.all.forEach(emo => {
                this.emotionRibbonVisualizer.addSegment(emo.category, emo.intensity);
            });
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

            // Update ribbon with emotion data
            if (data.emotionRibbon) {
                this.updateEmotionRibbonFromServer(data.emotionRibbon);
            }

            // Update sidebar with detected state
            if (data.state && this.cycleStates[data.state]) {
                this.updateDetectedState(this.cycleStates[data.state], data.confidence || 70);
            }

            // Store emotion data
            if (data.emotions) {
                this.sessionEmotions.push({
                    timestamp: Date.now(),
                    message: userMessage.substring(0, 100),
                    emotions: data.emotions,
                    aiDetected: data.state
                });
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
        if (!content || !content.value.trim()) return;
        
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

    // Show Emotion Journey Dashboard
    showEmotionJourney() {
        if (this.sessionEmotions.length === 0) {
            alert('No emotions detected yet. Start a conversation to see your emotional journey!');
            return;
        }

        // Calculate statistics
        const emotionCounts = {};
        const timeline = [];
        
        this.sessionEmotions.forEach((entry, index) => {
            const emotions = Object.keys(entry.emotions);
            emotions.forEach(emo => {
                emotionCounts[emo] = (emotionCounts[emo] || 0) + entry.emotions[emo].count;
            });
            
            timeline.push({
                index: index + 1,
                time: new Date(entry.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
                emotions: emotions,
                dominant: emotions[0]
            });
        });

        const dominantEmotion = Object.entries(emotionCounts)
            .sort((a, b) => b[1] - a[1])[0];

        // Create modal content
        const modalContent = `
            <div class="emotion-journey-modal">
                <h2>🎨 Your Emotional Journey</h2>
                <div class="journey-stats">
                    <div class="stat">
                        <span class="stat-value">${this.sessionEmotions.length}</span>
                        <span class="stat-label">Messages Analyzed</span>
                    </div>
                    <div class="stat">
                        <span class="stat-value">${Object.keys(emotionCounts).length}</span>
                        <span class="stat-label">Emotions Detected</span>
                    </div>
                    <div class="stat">
                        <span class="stat-value">${dominantEmotion ? dominantEmotion[0] : 'None'}</span>
                        <span class="stat-label">Dominant Emotion</span>
                    </div>
                </div>
                
                <div class="emotion-distribution">
                    <h3>Emotion Distribution</h3>
                    <div class="emotion-bars">
                        ${Object.entries(emotionCounts).map(([emotion, count]) => {
                            const cat = EmotionRibbon.categories[emotion];
                            const percentage = (count / Object.values(emotionCounts).reduce((a, b) => a + b, 0) * 100).toFixed(1);
                            return `
                                <div class="emotion-bar">
                                    <span class="bar-label">${cat.emoji} ${cat.name}</span>
                                    <div class="bar-track">
                                        <div class="bar-fill" style="width: ${percentage}%; background: ${cat.color};"></div>
                                    </div>
                                    <span class="bar-value">${percentage}%</span>
                                </div>
                            `;
                        }).join('')}
                    </div>
                </div>

                <div class="emotion-timeline">
                    <h3>Session Timeline</h3>
                    <div class="timeline">
                        ${timeline.map((t, i) => `
                            <div class="timeline-item">
                                <span class="timeline-index">${t.index}</span>
                                <span class="timeline-time">${t.time}</span>
                                <div class="timeline-emotions">
                                    ${t.emotions.map(e => {
                                        const cat = EmotionRibbon.categories[e];
                                        return `<span class="timeline-badge" style="background: ${cat.color}20; color: ${cat.color};">${cat.emoji} ${cat.name}</span>`;
                                    }).join('')}
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>

                <div class="journey-insights">
                    <h3>💡 Insights</h3>
                    <ul>
                        ${this.generateInsights(emotionCounts, timeline)}
                    </ul>
                </div>

                <button class="btn-primary" onclick="app.closeEmotionJourney()">Close</button>
            </div>
        `;

        // Show modal
        const modal = document.createElement('div');
        modal.className = 'modal emotion-journey-overlay';
        modal.innerHTML = `<div class="modal-content journey-content">${modalContent}</div>`;
        document.body.appendChild(modal);

        // Add styles
        const style = document.createElement('style');
        style.textContent = `
            .emotion-journey-overlay {
                z-index: 300;
            }
            .journey-content {
                max-width: 700px;
                max-height: 90vh;
                overflow-y: auto;
            }
            .emotion-journey-modal h2 {
                margin-bottom: 1.5rem;
                text-align: center;
            }
            .journey-stats {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 1rem;
                margin-bottom: 2rem;
            }
            .journey-stats .stat {
                text-align: center;
                padding: 1rem;
                background: #f8fafc;
                border-radius: 0.75rem;
            }
            .journey-stats .stat-value {
                display: block;
                font-size: 1.5rem;
                font-weight: 700;
                color: #14b8a6;
            }
            .journey-stats .stat-label {
                font-size: 0.75rem;
                color: #64748b;
            }
            .emotion-distribution, .emotion-timeline, .journey-insights {
                margin-bottom: 2rem;
            }
            .emotion-distribution h3, .emotion-timeline h3, .journey-insights h3 {
                margin-bottom: 1rem;
                font-size: 1.125rem;
            }
            .emotion-bar {
                display: flex;
                align-items: center;
                gap: 0.75rem;
                margin-bottom: 0.5rem;
            }
            .bar-label {
                width: 120px;
                font-size: 0.875rem;
                font-weight: 500;
            }
            .bar-track {
                flex: 1;
                height: 24px;
                background: #e2e8f0;
                border-radius: 12px;
                overflow: hidden;
            }
            .bar-fill {
                height: 100%;
                border-radius: 12px;
                transition: width 0.5s ease;
            }
            .bar-value {
                width: 50px;
                text-align: right;
                font-size: 0.875rem;
                color: #64748b;
            }
            .timeline {
                display: flex;
                flex-direction: column;
                gap: 0.5rem;
            }
            .timeline-item {
                display: flex;
                align-items: center;
                gap: 0.75rem;
                padding: 0.75rem;
                background: #f8fafc;
                border-radius: 0.5rem;
            }
            .timeline-index {
                width: 24px;
                height: 24px;
                background: #14b8a6;
                color: white;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 0.75rem;
                font-weight: 600;
            }
            .timeline-time {
                width: 60px;
                font-size: 0.75rem;
                color: #64748b;
            }
            .timeline-emotions {
                display: flex;
                gap: 0.5rem;
                flex-wrap: wrap;
            }
            .timeline-badge {
                padding: 0.25rem 0.5rem;
                border-radius: 9999px;
                font-size: 0.75rem;
                font-weight: 500;
            }
            .journey-insights ul {
                list-style: none;
                padding: 0;
            }
            .journey-insights li {
                padding: 0.5rem 0;
                padding-left: 1.5rem;
                position: relative;
            }
            .journey-insights li::before {
                content: '💡';
                position: absolute;
                left: 0;
            }
        `;
        document.head.appendChild(style);
    },

    generateInsights(emotionCounts, timeline) {
        const insights = [];
        const emotions = Object.keys(emotionCounts);
        
        if (emotions.includes('POWER') && emotions.includes('LOSS')) {
            insights.push('You cycled between feeling powerful and experiencing loss — this is a common pattern.');
        }
        if (emotions.includes('CRAVE') && emotions.includes('EMPTINESS')) {
            insights.push('Craving often follows emptiness. Notice when you reach for something to fill a void.');
        }
        if (emotions.includes('EMPATHY')) {
            insights.push('You showed self-awareness and compassion — a sign of emotional growth.');
        }
        if (timeline.length > 5) {
            insights.push('You engaged deeply with your emotions. Regular reflection builds resilience.');
        }
        if (insights.length === 0) {
            insights.push('Every emotional experience is valid. Continue exploring your inner world.');
        }
        
        return insights.map(i => `<li>${i}</li>`).join('');
    },

    closeEmotionJourney() {
        const modal = document.querySelector('.emotion-journey-overlay');
        if (modal) modal.remove();
    },
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
