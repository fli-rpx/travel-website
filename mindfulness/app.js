// Mindfulness Therapy Web App - JavaScript

const app = {
    currentTab: 'home',
    currentStep: 0,
    answers: {},
    timerInterval: null,
    timerSeconds: 0,
    timerTotal: 0,
    isRunning: false,

    // Data
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
        'If I were not trying to feel powerful at all, what would I want?',
        'The pause between feeling and action is where freedom lives.',
        'Inner power is the capacity to tolerate emptiness without panic.'
    ],

    journalPrompts: [
        'What are you grateful for today?',
        'What is one thing that went well?',
        'What are you looking forward to?',
        'What is the spiciest emotion right now?',
        'What greasy thing are you reaching for?',
        'What vegetable do you actually need?'
    ],

    init() {
        this.setupNavigation();
        this.updateGreeting();
        this.loadData();
        this.renderQuote();
        this.renderStreak();
        this.setupSaladCheck();
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

        if (tab === 'progress') {
            this.renderProgress();
        }
    },

    updateGreeting() {
        const hour = new Date().getHours();
        let greeting = 'Good morning';
        if (hour >= 12 && hour < 17) greeting = 'Good afternoon';
        else if (hour >= 17) greeting = 'Good evening';
        else if (hour < 5) greeting = 'Good night';
        
        document.getElementById('greeting').textContent = greeting + ',';
    },

    renderQuote() {
        const quote = this.quotes[Math.floor(Math.random() * this.quotes.length)];
        document.getElementById('quoteCard').innerHTML = `<p>${quote}</p>`;
    },

    renderStreak() {
        const streak = this.getStreak();
        document.getElementById('streakCount').textContent = `${streak} Day Streak`;
        
        const dotsContainer = document.getElementById('streakDots');
        dotsContainer.innerHTML = '';
        for (let i = 0; i < 7; i++) {
            const dot = document.createElement('div');
            dot.className = 'streak-dot' + (i < streak % 7 ? ' active' : '');
            dotsContainer.appendChild(dot);
        }
    },

    getStreak() {
        const checkins = JSON.parse(localStorage.getItem('checkins') || '[]');
        if (checkins.length === 0) return 0;
        
        // Simple streak calculation
        return Math.min(checkins.length, 7);
    },

    // Salad Check
    setupSaladCheck() {
        this.currentStep = 0;
        this.answers = {};
        this.renderQuestion();
    },

    renderQuestion() {
        const container = document.getElementById('questionContainer');
        const totalSteps = this.spicyQuestions.length + this.greasyQuestions.length + this.vegetableQuestions.length;
        
        document.getElementById('progressFill').style.width = `${(this.currentStep / totalSteps) * 100}%`;
        document.getElementById('progressText').textContent = `Question ${this.currentStep + 1} of ${totalSteps}`;

        let question, category, color;
        if (this.currentStep < this.spicyQuestions.length) {
            question = this.spicyQuestions[this.currentStep];
            category = 'spicy';
            color = '#ef4444';
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
                <div class="question-category ${category}" style="color: ${color}">${category.toUpperCase()}</div>
                <div class="question-text">${question.text}</div>
                <div class="options">
                    ${question.options.map(opt => `
                        <button class="option-btn ${this.answers[question.id] === opt ? 'selected' : ''}" onclick="app.selectOption('${question.id}', '${opt}')">
                            ${opt}
                            <span class="check">✓</span>
                        </button>
                    `).join('')}
                </div>
                <div class="nav-buttons">
                    ${this.currentStep > 0 ? '<button class="btn-secondary" onclick="app.prevStep()">Previous</button>' : '<div></div>'}
                    <button class="btn-primary" onclick="app.nextStep()">${this.currentStep < totalSteps - 1 ? 'Next' : 'See Results'}</button>
                </div>
            </div>
        `;
    },

    selectOption(questionId, option) {
        this.answers[questionId] = option;
        this.renderQuestion();
    },

    nextStep() {
        const totalSteps = this.spicyQuestions.length + this.greasyQuestions.length + this.vegetableQuestions.length;
        
        if (this.currentStep < totalSteps - 1) {
            this.currentStep++;
            this.renderQuestion();
        } else {
            this.showResults();
        }
    },

    prevStep() {
        if (this.currentStep > 0) {
            this.currentStep--;
            this.renderQuestion();
        }
    },

    showResults() {
        document.getElementById('questionContainer').classList.add('hidden');
        document.getElementById('resultsContainer').classList.remove('hidden');
        
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
        
        document.getElementById('resultsContent').innerHTML = `
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
            
            <div class="protocol">
                <h3>Your 7-Step Balancing Protocol</h3>
                <div class="protocol-step">
                    <div class="step-number">1</div>
                    <div class="step-content">
                        <h4>Stop</h4>
                        <p>Physically pause. Do not act. Take one slow breath.</p>
                    </div>
                </div>
                <div class="protocol-step">
                    <div class="step-number">2</div>
                    <div class="step-content">
                        <h4>Name the Spiciness</h4>
                        <p>What is too spicy? "${spice || 'Powerlessness'}"</p>
                    </div>
                </div>
                <div class="protocol-step">
                    <div class="step-number">3</div>
                    <div class="step-content">
                        <h4>Locate It</h4>
                        <p>Where do you feel this in your body? Just notice.</p>
                    </div>
                </div>
                <div class="protocol-step">
                    <div class="step-number">4</div>
                    <div class="step-content">
                        <h4>Identify the Craving</h4>
                        <p>What are you reaching for? "${grease || 'External validation'}"</p>
                    </div>
                </div>
                <div class="protocol-step">
                    <div class="step-number">5</div>
                    <div class="step-content">
                        <h4>Choose a Vegetable</h4>
                        <p>What would nourish you? "${vegetable || 'Rest'}"</p>
                    </div>
                </div>
                <div class="protocol-step">
                    <div class="step-number">6</div>
                    <div class="step-content">
                        <h4>Take Action</h4>
                        <p>Do it for just 2 minutes.</p>
                    </div>
                </div>
                <div class="protocol-step">
                    <div class="step-number">7</div>
                    <div class="step-content">
                        <h4>Notice</h4>
                        <p>How do you feel? Not perfect, just different.</p>
                    </div>
                </div>
            </div>
        `;
        
        this.renderStreak();
    },

    resetSalad() {
        this.currentStep = 0;
        this.answers = {};
        document.getElementById('questionContainer').classList.remove('hidden');
        document.getElementById('resultsContainer').classList.add('hidden');
        this.renderQuestion();
    },

    // Exercises
    startExercise(type) {
        const exercises = {
            breathing: { name: 'Breathing', duration: 5 },
            bodyscan: { name: 'Body Scan', duration: 15 },
            lovingkindness: { name: 'Loving Kindness', duration: 10 },
            sleep: { name: 'Sleep Relaxation', duration: 20 },
            anxiety: { name: 'Anxiety Relief', duration: 10 },
            gratitude: { name: 'Gratitude', duration: 5 },
            walking: { name: 'Mindful Walking', duration: 10 }
        };
        
        const exercise = exercises[type];
        if (!exercise) return;
        
        document.getElementById('exerciseTitle').textContent = exercise.name;
        document.getElementById('exerciseModal').classList.remove('hidden');
        
        this.timerSeconds = exercise.duration * 60;
        this.timerTotal = exercise.duration * 60;
        this.isRunning = false;
        this.updateTimerDisplay();
    },

    toggleTimer() {
        this.isRunning = !this.isRunning;
        document.getElementById('playPauseBtn').textContent = this.isRunning ? '⏸️' : '▶️';
        
        if (this.isRunning) {
            this.timerInterval = setInterval(() => {
                this.timerSeconds--;
                this.updateTimerDisplay();
                
                if (this.timerSeconds <= 0) {
                    this.stopExercise();
                    alert('Exercise complete! 🎉');
                }
            }, 1000);
        } else {
            clearInterval(this.timerInterval);
        }
    },

    updateTimerDisplay() {
        const minutes = Math.floor(this.timerSeconds / 60);
        const seconds = this.timerSeconds % 60;
        document.getElementById('timerText').textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
        
        const progress = (this.timerTotal - this.timerSeconds) / this.timerTotal;
        const offset = 283 - (283 * progress);
        document.getElementById('timerProgress').style.strokeDashoffset = offset;
    },

    stopExercise() {
        clearInterval(this.timerInterval);
        this.isRunning = false;
        document.getElementById('exerciseModal').classList.add('hidden');
        
        // Save session
        const sessions = JSON.parse(localStorage.getItem('sessions') || '[]');
        sessions.push({
            date: new Date().toISOString(),
            duration: Math.floor((this.timerTotal - this.timerSeconds) / 60)
        });
        localStorage.setItem('sessions', JSON.stringify(sessions));
    },

    // Journal
    logMood(mood) {
        localStorage.setItem('todayMood', mood);
        document.querySelectorAll('.mood-btn').forEach(btn => {
            btn.classList.toggle('selected', parseInt(btn.dataset.mood) === mood);
        });
    },

    newPrompt() {
        const prompt = this.journalPrompts[Math.floor(Math.random() * this.journalPrompts.length)];
        document.getElementById('journalPrompt').textContent = prompt;
    },

    saveJournal() {
        const content = document.getElementById('journalEntry').value;
        if (!content.trim()) return;
        
        const entries = JSON.parse(localStorage.getItem('journalEntries') || '[]');
        entries.unshift({
            date: new Date().toISOString(),
            title: 'Journal Entry',
            content,
            mood: localStorage.getItem('todayMood') || 3
        });
        localStorage.setItem('journalEntries', JSON.stringify(entries));
        
        document.getElementById('journalEntry').value = '';
        this.renderJournalEntries();
    },

    renderJournalEntries() {
        const entries = JSON.parse(localStorage.getItem('journalEntries') || '[]');
        const container = document.getElementById('journalEntries');
        
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
        
        document.getElementById('totalSessions').textContent = totalSessions;
        document.getElementById('totalMinutes').textContent = totalMinutes;
        document.getElementById('streakDays').textContent = this.getStreak();
        
        this.renderWeeklyChart();
        this.renderAchievements(totalSessions, totalMinutes);
        this.renderInsights();
    },

    renderWeeklyChart() {
        const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
        const container = document.getElementById('weeklyChart');
        
        container.innerHTML = days.map(day => `
            <div class="chart-bar">
                <div class="chart-bar-fill" style="height: ${Math.random() * 60 + 20}px"></div>
                <div class="chart-bar-label">${day}</div>
            </div>
        `).join('');
    },

    renderAchievements(sessions, minutes) {
        const achievements = [
            { icon: '✨', name: 'First Step', unlocked: sessions >= 1 },
            { icon: '🥗', name: 'Salad Master', unlocked: sessions >= 5 },
            { icon: '🔥', name: 'On Fire', unlocked: this.getStreak() >= 7 },
            { icon: '⏱️', name: 'Time Master', unlocked: minutes >= 100 },
            { icon: '❤️', name: 'Self-Compassion', unlocked: sessions >= 3 },
            { icon: '⏸️', name: 'The Pause', unlocked: sessions >= 10 }
        ];
        
        document.getElementById('achievements').innerHTML = achievements.map(a => `
            <div class="achievement ${a.unlocked ? 'unlocked' : ''}">
                <div class="achievement-icon">${a.icon}</div>
                <div class="achievement-name">${a.name}</div>
            </div>
        `).join('');
    },

    renderInsights() {
        const streak = this.getStreak();
        let insight = 'Start your mindfulness journey today!';
        if (streak >= 7) insight = `Amazing! You have practiced for ${streak} days in a row.`;
        else if (streak > 0) insight = `Great job! You are on a ${streak}-day streak.`;
        
        document.getElementById('insights').innerHTML = `
            <div class="insight">
                <div class="insight-icon">📈</div>
                <div class="insight-text">${insight}</div>
            </div>
            <div class="insight">
                <div class="insight-icon">🥗</div>
                <div class="insight-text">The old you just reacted. The you now is learning to choose.</div>
            </div>
        `;
    },

    loadData() {
        const mood = localStorage.getItem('todayMood');
        if (mood) {
            this.logMood(parseInt(mood));
        }
        this.renderJournalEntries();
    }
};

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    app.init();
});
