// server.js - Backend proxy for DeepSeek API
// This keeps your API key server-side, never exposed to frontend

const express = require('express');
const cors = require('cors');
const fetch = require('node-fetch');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Get API key from environment variable
const DEEPSEEK_API_KEY = process.env.DEEPSEEK_API_KEY;
const DEEPSEEK_API_URL = 'https://api.deepseek.com/v1/chat/completions';

// Middleware
app.use(cors());
app.use(express.json());

// Serve static files (the mindfulness app)
app.use(express.static(path.join(__dirname, 'mindfulness')));

// Health check
app.get('/api/health', (req, res) => {
    res.json({ 
        status: 'ok', 
        ai_available: !!DEEPSEEK_API_KEY 
    });
});

// Proxy endpoint for DeepSeek chat
app.post('/api/chat', async (req, res) => {
    if (!DEEPSEEK_API_KEY) {
        return res.status(503).json({ 
            error: 'AI service not configured',
            message: 'DEEPSEEK_API_KEY not set on server'
        });
    }

    try {
        const { message } = req.body;
        
        if (!message) {
            return res.status(400).json({ error: 'Message is required' });
        }

        const systemPrompt = `You are an empathetic AI therapist specializing in the "Power-Possession Cycle" - a psychological pattern where people seek external validation (power), possess it, inevitably lose it, collapse into emptiness, crave substitutes, and return to power-seeking.

The six states are:
1. Power - External validation, feeling in control
2. Possession - Owning phase, attachment to external power  
3. Loss - Inevitable decline, external power fading
4. Emptiness - Collapse, void when external validation gone
5. Craving - Compulsive urge for substitute satisfaction
6. Return - Power-seeking behavior restarting cycle

Analyze the user's emotional state and respond with:
1. A brief empathetic acknowledgment (1-2 sentences)
2. Identify which state(s) they seem to be in
3. Suggest one specific intervention from: Values grounding, Somatic anchoring, Urge surfing, Pattern interrupt, Physiological sigh, 5-4-3-2-1 grounding, or Self-compassion break

Keep your response concise (3-4 sentences max) and warm.`;

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
                max_tokens: 200
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
        
        // Extract state from response for sidebar update
        const aiResponse = data.choices[0].message.content;
        const detectedState = inferStateFromResponse(aiResponse);
        
        res.json({
            response: aiResponse,
            state: detectedState,
            confidence: 85
        });

    } catch (error) {
        console.error('Proxy error:', error);
        res.status(500).json({ 
            error: 'Internal server error',
            message: 'Something went wrong processing your request'
        });
    }
});

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
    
    // Simple keyword-based fallback
    const lowerText = message.toLowerCase();
    let detectedState = 'emptiness';
    let confidence = 70;
    
    const states = {
        power: {
            name: 'Power',
            description: 'External validation, feeling in control',
            strategies: ['Values grounding', 'Internal validation', 'Preventive balance'],
            keywords: ['angry', 'power', 'control', 'strong', 'confident']
        },
        possession: {
            name: 'Possession', 
            description: 'Owning phase, attachment to external power',
            strategies: ['Letting go practice', 'Non-attachment', 'Impermanence awareness'],
            keywords: ['have', 'own', 'mine', 'keep', 'hold']
        },
        loss: {
            name: 'Loss',
            description: 'Inevitable decline, external power fading',
            strategies: ['Acceptance', 'Grief processing', 'Reality orientation'],
            keywords: ['lost', 'failed', 'rejected', 'gone', 'ended']
        },
        emptiness: {
            name: 'Emptiness',
            description: 'Collapse, void when external validation gone',
            strategies: ['Somatic anchoring', 'Presence', 'Self-compassion'],
            keywords: ['empty', 'nothing', 'numb', 'void', 'hollow']
        },
        craving: {
            name: 'Craving',
            description: 'Compulsive urge for substitute satisfaction',
            strategies: ['Urge surfing', 'Pattern interruption', 'Alternative satisfaction'],
            keywords: ['want', 'need', 'crave', 'urge', 'desperate']
        },
        return: {
            name: 'Return',
            description: 'Power-seeking behavior restarting cycle',
            strategies: ['Cycle awareness', 'Conscious choice', 'Break pattern'],
            keywords: ['again', 'restart', 'new', 'chance', 'try']
        }
    };
    
    for (const [stateKey, stateData] of Object.entries(states)) {
        if (stateData.keywords.some(kw => lowerText.includes(kw))) {
            detectedState = stateKey;
            confidence = 80 + Math.floor(Math.random() * 15);
            break;
        }
    }
    
    const state = states[detectedState];
    
    res.json({
        response: `I hear you. It sounds like you might be in the **${state.name}** state. This is when ${state.description.toLowerCase()}. Would you like to try a ${state.strategies[0].toLowerCase()} exercise?`,
        state: detectedState,
        confidence: confidence,
        fallback: true
    });
});

app.listen(PORT, () => {
    console.log(`🧘 Mindfulness Therapy Server running on http://localhost:${PORT}`);
    console.log(`AI Status: ${DEEPSEEK_API_KEY ? '✅ Configured' : '⚠️  Not configured (set DEEPSEEK_API_KEY env var)'}`);
});
