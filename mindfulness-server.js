// server.js - Backend proxy for DeepSeek API with Emotion Ribbon integration
// This keeps your API key server-side and enriches prompts with emotion context

const express = require('express');
const cors = require('cors');
const fetch = require('node-fetch');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Get API key from environment variable
const DEEPSEEK_API_KEY = process.env.DEEPSEEK_API_KEY;
const DEEPSEEK_API_URL = 'https://api.deepseek.com/v1/chat/completions';

// Emotion Ribbon Lexicon (subset for server-side analysis)
const emotionLexicon = {
    POWER: ['powerful','mighty','strength','dominant','authority','control','master','leader','confident','capable','triumph','victory','success','courage','brave','energy','vigor','accomplish','achievement','agency','ambition','excellence','hero','champion','conquer','prevail','supreme','almighty','potent','robust'],
    POSSESSION: ['possess','own','acquire','obtain','gain','seize','claim','desire','want','covet','greed','hoard','wealth','treasure','have','hold','keep','mine','property','belongings','assets','collection','accumulation','retention','custody'],
    LOSS: ['loss','lose','grief','mourn','sorrow','anguish','pain','separation','abandonment','deprived','bereft','missing','forfeit','surrender','death','divorce','disaster','devastation','distress','lament','weep','cry','heartbreak','mourning','widow'],
    EMPTINESS: ['empty','void','hollow','numb','dead','lifeless','meaningless','pointless','isolated','lonely','despair','disconnected','alienated','vacant','blank','drained','exhausted','depleted','barren','desolate','abandoned','forsaken'],
    CRAVE: ['crave','long','yearn','desire','hunger','thirst','urge','obsession','passion','lust','desperate','urgent','burning','addicted','impatient','aching','pining','starving','ravenous','insatiable','voracious'],
    EMPATHY: ['empathy','compassion','sympathy','understand','care','kind','gentle','tender','love','connect','bond','support','comfort','nurture','share','listen','concern','affection','warmth','solace','mercy','kindness','tenderness']
};

// Emotion category metadata
const emotionCategories = {
    POWER: { name: 'Power', color: '#8B0000', description: 'Agency, Control, Mastery', emoji: '🔴' },
    POSSESSION: { name: 'Possession', color: '#FF6B35', description: 'Desire to Own, Acquire', emoji: '🟠' },
    LOSS: { name: 'Loss', color: '#191970', description: 'Grief, Deprivation', emoji: '🔵' },
    EMPTINESS: { name: 'Emptiness', color: '#36454F', description: 'Void, Numbness', emoji: '⚫' },
    CRAVE: { name: 'Crave', color: '#DC143C', description: 'Urgent Desire', emoji: '🔴' },
    EMPATHY: { name: 'Empathy', color: '#2E8B57', description: 'Connection, Compassion', emoji: '🟢' }
};

// Middleware
app.use(cors());
app.use(express.json());

// Serve static files (the mindfulness app)
app.use(express.static(path.join(__dirname, 'mindfulness')));

// Health check
app.get('/api/health', (req, res) => {
    res.json({ 
        status: 'ok', 
        ai_available: !!DEEPSEEK_API_KEY,
        emotion_ribbon: 'enabled'
    });
});

// Analyze emotions in text
function analyzeEmotions(text) {
    const words = text.toLowerCase().match(/\b[a-z]+\b/g) || [];
    const detected = {};
    
    for (const [category, wordList] of Object.entries(emotionLexicon)) {
        const matches = words.filter(word => wordList.includes(word));
        if (matches.length > 0) {
            detected[category] = {
                count: matches.length,
                words: matches,
                intensity: Math.min(matches.length / 3, 1),
                confidence: Math.min(70 + matches.length * 10, 95)
            };
        }
    }
    
    // Get dominant emotion
    const entries = Object.entries(detected);
    const dominant = entries.length > 0 
        ? entries.sort((a, b) => b[1].count - a[1].count)[0]
        : null;
    
    return { detected, dominant };
}

// Build emotion-aware system prompt
function buildSystemPrompt(emotionContext) {
    const basePrompt = `You are an empathetic AI therapist specializing in emotional awareness and the "Power-Possession Cycle".

The six emotional states are:
🔴 POWER - Agency, Control, Mastery (Dark Red #8B0000)
🟠 POSSESSION - Desire to Own, Acquire (Burnt Orange #FF6B35)  
🔵 LOSS - Grief, Deprivation (Midnight Blue #191970)
⚫ EMPTINESS - Void, Numbness (Charcoal #36454F)
🔴 CRAVE - Urgent Desire, Compulsion (Crimson #DC143C)
🟢 EMPATHY - Connection, Compassion (Sea Green #2E8B57)

The emotion cycle flows: CRAVE → POSSESSION → POWER → LOSS → EMPTINESS → CRAVE

Guidelines:
- Respond with warmth and empathy (3-4 sentences max)
- Acknowledge their emotional state specifically
- Suggest one concrete intervention they can try now
- Available interventions: Values grounding, Somatic anchoring, Urge surfing, Pattern interrupt, Physiological sigh, 5-4-3-2-1 grounding, Self-compassion break`;

    if (emotionContext && emotionContext.dominant) {
        const [category, data] = emotionContext.dominant;
        const cat = emotionCategories[category];
        
        return basePrompt + `\n\n[EMOTION ANALYSIS]\nThe user's message indicates ${cat.name.toLowerCase()} emotions (${data.confidence}% confidence). ` +
               `Detected words: ${data.words.slice(0, 5).join(', ')}. ` +
               `This relates to: ${cat.description.toLowerCase()}. ` +
               `Respond with particular sensitivity to ${cat.name.toLowerCase()}-related feelings.`;
    }
    
    return basePrompt;
}

// Proxy endpoint for DeepSeek chat with emotion enrichment
app.post('/api/chat', async (req, res) => {
    if (!DEEPSEEK_API_KEY) {
        return res.status(503).json({ 
            error: 'AI service not configured',
            message: 'DEEPSEEK_API_KEY not set on server'
        });
    }

    try {
        const { message, includeEmotions = true } = req.body;
        
        if (!message) {
            return res.status(400).json({ error: 'Message is required' });
        }

        // Analyze emotions if requested
        let emotionContext = null;
        if (includeEmotions) {
            emotionContext = analyzeEmotions(message);
        }

        // Build emotion-aware prompt
        const systemPrompt = buildSystemPrompt(emotionContext);

        const response = await fetch(DEEPSEEK_API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${DEEPSEEK_API_KEY}`
            },
            body: JSON.stringify({
                model: 'deepseek-chat',
                messages: [
                    { role: 'system', content: systemPrompt },
                    { role: 'user', content: message }
                ],
                temperature: 0.7,
                max_tokens: 250
            })
        });

        if (!response.ok) {
            const errorData = await response.text();
            console.error('DeepSeek API error:', errorData);
            return res.status(502).json({ 
                error: 'AI service error',
                message: 'Failed to get response from AI service'
            });
        }

        const data = await response.json();
        const aiResponse = data.choices[0].message.content;
        
        // Determine state from emotion analysis or AI response
        let detectedState = 'emptiness';
        let confidence = 70;
        
        if (emotionContext && emotionContext.dominant) {
            detectedState = emotionContext.dominant[0].toLowerCase();
            confidence = emotionContext.dominant[1].confidence;
        } else {
            detectedState = inferStateFromResponse(aiResponse);
            confidence = 75;
        }

        res.json({
            response: aiResponse,
            state: detectedState,
            confidence: confidence,
            emotions: emotionContext ? emotionContext.detected : {},
            emotionRibbon: emotionContext ? {
                dominant: emotionContext.dominant ? {
                    category: emotionContext.dominant[0],
                    ...emotionCategories[emotionContext.dominant[0]],
                    ...emotionContext.dominant[1]
                } : null,
                all: Object.entries(emotionContext?.detected || {}).map(([cat, data]) => ({
                    category: cat,
                    ...emotionCategories[cat],
                    ...data
                }))
            } : null
        });

    } catch (error) {
        console.error('Proxy error:', error);
        res.status(500).json({ 
            error: 'Internal server error',
            message: 'Something went wrong processing your request'
        });
    }
});

// Dedicated emotion analysis endpoint
app.post('/api/analyze-emotions', (req, res) => {
    const { text } = req.body;
    
    if (!text) {
        return res.status(400).json({ error: 'Text is required' });
    }
    
    const analysis = analyzeEmotions(text);
    
    res.json({
        detected: analysis.detected,
        dominant: analysis.dominant ? {
            category: analysis.dominant[0],
            ...emotionCategories[analysis.dominant[0]],
            ...analysis.dominant[1]
        } : null,
        summary: analysis.dominant 
            ? `Primarily ${emotionCategories[analysis.dominant[0]].name} (${analysis.dominant[1].confidence}% confidence)`
            : 'No strong emotions detected'
    });
});

// Get session journey (would integrate with session storage in production)
app.post('/api/session-journey', (req, res) => {
    const { messages } = req.body;
    
    if (!Array.isArray(messages)) {
        return res.status(400).json({ error: 'Messages array required' });
    }
    
    // Analyze all messages
    const journey = messages.map((msg, index) => {
        const analysis = analyzeEmotions(msg.text || msg);
        return {
            index,
            timestamp: msg.timestamp || Date.now(),
            emotions: analysis.detected,
            dominant: analysis.dominant ? {
                category: analysis.dominant[0],
                ...emotionCategories[analysis.dominant[0]],
                ...analysis.dominant[1]
            } : null
        };
    });
    
    // Calculate aggregate stats
    const emotionCounts = {};
    journey.forEach(entry => {
        Object.keys(entry.emotions).forEach(emo => {
            emotionCounts[emo] = (emotionCounts[emo] || 0) + entry.emotions[emo].count;
        });
    });
    
    res.json({
        journey,
        totalMessages: messages.length,
        emotionCounts,
        dominantEmotion: Object.entries(emotionCounts)
            .sort((a, b) => b[1] - a[1])[0]?.[0] || null
    });
});

// Emotion Ribbon Lexicon for server-side analysis
const emotionRibbonLexicon = {
    POWER: ['powerful','mighty','strength','dominant','authority','control','master','leader','confident','capable','triumph','victory','success','courage','brave','energy','vigor','accomplish','achievement','agency','ambition','excellence','hero','champion','conquer','prevail','supreme','almighty','potent','robust','excel','authority','competent','expert','accomplished','skilled','superior','bold','determined','resolute','backbone','command','dominance','empower','force','influence','mastery','powerful','strength','strong','superior','triumph','victory','win','winning'],
    POSSESSION: ['possess','own','acquire','obtain','gain','seize','claim','desire','want','covet','greed','hoard','wealth','treasure','have','hold','keep','mine','property','belongings','assets','collection','accumulation','retention','custody','capture','grasp','attain','accumulate','amass','property','belongings','mine','cling','fortune','treasure','gain','wealth','acquire','obtain'],
    LOSS: ['loss','lose','grief','mourn','sorrow','anguish','pain','separation','abandonment','deprived','bereft','missing','forfeit','surrender','death','divorce','disaster','devastation','distress','lament','weep','cry','heartbreak','mourning','widow','lost','grief','mourn','ache','parting','departure','bereavement','denied','hurt','sorrow','pain','forsaken','orphan','surrender'],
    EMPTINESS: ['empty','void','hollow','numb','dead','lifeless','meaningless','pointless','isolated','lonely','despair','disconnected','alienated','vacant','blank','drained','exhausted','depleted','barren','desolate','abandoned','forsaken','lonely','despair','worthless','isolated','absence','hollow','barren','apathetic','meaningless','pointless','futile','disconnected','alienated','depression','detached','useless','lack','deficiency'],
    CRAVE: ['crave','long','yearn','desire','hunger','thirst','urge','obsession','passion','lust','desperate','urgent','burning','addicted','impatient','aching','pining','starving','ravenous','insatiable','voracious','appetency','covetous','intense','eager','frantic','thirst','passion','fierce','ardent','anxious','compulsion','dependent','pine','impatient','obsession','fixation','desperate','burning','hooked','withdrawal','itch'],
    EMPATHY: ['empathy','compassion','sympathy','understand','care','kind','gentle','tender','love','connect','bond','support','comfort','nurture','share','listen','concern','affection','warmth','solace','mercy','kindness','tenderness','nurture','comfort','share','intimate','kind','tender','affection','heal','compassion','sympathy','love','console','empathy','care','concern','kindness','connect','bond','attach','relate','identify','feel','listen','hear','soothe','unite','join','link','close','sensitive']
};

// Analyze text with Emotion Ribbon Lexicon
function analyzeEmotionRibbon(text) {
    const words = text.toLowerCase().match(/\b[a-z]+\b/g) || [];
    const detected = {};
    
    for (const [category, wordList] of Object.entries(emotionRibbonLexicon)) {
        const matches = words.filter(word => wordList.includes(word));
        if (matches.length > 0) {
            detected[category] = {
                count: matches.length,
                words: matches,
                intensity: Math.min(matches.length / 3, 1),
                confidence: Math.min(70 + matches.length * 10, 95)
            };
        }
    }
    
    // Get dominant emotion
    const dominant = Object.entries(detected).sort((a, b) => b[1].count - a[1].count)[0];
    
    return {
        detected,
        dominant: dominant ? { category: dominant[0], ...dominant[1] } : null,
        categories: Object.keys(detected)
    };
}

// Helper to infer state from AI response
function inferStateFromResponse(response) {
    const lowerResponse = response.toLowerCase();
    
    if (lowerResponse.includes('power') && !lowerResponse.includes('power-seeking')) {
        return 'power';
    } else if (lowerResponse.includes('possession') || lowerResponse.includes('attachment')) {
        return 'possession';
    } else if (lowerResponse.includes('loss') || lowerResponse.includes('lost')) {
        return 'loss';
    } else if (lowerResponse.includes('emptiness') || lowerResponse.includes('empty')) {
        return 'emptiness';
    } else if (lowerResponse.includes('craving') || lowerResponse.includes('crave')) {
        return 'craving';
    } else if (lowerResponse.includes('return') || lowerResponse.includes('seeking')) {
        return 'return';
    }
    
    return 'emptiness';
}

// Fallback endpoint when AI is not available
app.post('/api/chat-fallback', (req, res) => {
    const { message } = req.body;
    
    // Analyze emotions
    const emotionContext = analyzeEmotions(message);
    
    // Simple keyword-based fallback
    const lowerText = message.toLowerCase();
    let detectedState = emotionContext.dominant ? emotionContext.dominant[0].toLowerCase() : 'emptiness';
    let confidence = emotionContext.dominant ? emotionContext.dominant[1].confidence : 70;
    
    const states = {
        power: {
            name: 'Power',
            description: 'External validation, feeling in control',
            strategies: ['Values grounding', 'Internal validation', 'Preventive balance']
        },
        possession: {
            name: 'Possession', 
            description: 'Owning phase, attachment to external power',
            strategies: ['Letting go practice', 'Non-attachment', 'Impermanence awareness']
        },
        loss: {
            name: 'Loss',
            description: 'Inevitable decline, external power fading',
            strategies: ['Acceptance', 'Grief processing', 'Reality orientation']
        },
        emptiness: {
            name: 'Emptiness',
            description: 'Collapse, void when external validation gone',
            strategies: ['Somatic anchoring', 'Presence', 'Self-compassion']
        },
        crave: {
            name: 'Craving',
            description: 'Compulsive urge for substitute satisfaction',
            strategies: ['Urge surfing', 'Pattern interruption', 'Alternative satisfaction']
        },
        empathy: {
            name: 'Empathy',
            description: 'Connection, compassion, understanding',
            strategies: ['Active listening', 'Validation', 'Shared presence']
        }
    };
    
    const state = states[detectedState] || states.emptiness;
    
    res.json({
        response: `I hear you. It sounds like you might be experiencing **${state.name}** emotions. This relates to: ${state.description.toLowerCase()}. Would you like to try a ${state.strategies[0].toLowerCase()} exercise?`,
        state: detectedState,
        confidence: confidence,
        emotions: emotionContext.detected,
        emotionRibbon: emotionContext.dominant ? {
            dominant: {
                category: emotionContext.dominant[0],
                ...emotionCategories[emotionContext.dominant[0]],
                ...emotionContext.dominant[1]
            },
            all: Object.entries(emotionContext.detected).map(([cat, data]) => ({
                category: cat,
                ...emotionCategories[cat],
                ...data
            }))
        } : null,
        fallback: true
    });
});

app.listen(PORT, () => {
    console.log(`🧘 Mindfulness Therapy Server running on http://localhost:${PORT}`);
    console.log(`AI Status: ${DEEPSEEK_API_KEY ? '✅ Configured' : '⚠️  Not configured (set DEEPSEEK_API_KEY env var)'}`);
    console.log(`🎨 Emotion Ribbon: ✅ Enabled with ${Object.values(emotionLexicon).flat().length} words`);
});
