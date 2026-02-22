# Mindfulness Therapy App - Backend Proxy Setup

## Overview

This app now uses a **backend proxy server** to securely handle DeepSeek API calls. Your API key stays on the server, never exposed to the frontend or GitHub.

## Architecture

```
User Browser <--> Your Backend Server <--> DeepSeek API
                    (API key stored here)
```

## Quick Start

### 1. Install Dependencies

```bash
cd /root/.openclaw/workspace/travel-website
npm install
```

### 2. Set Environment Variable

Add to your `.bashrc` or `.zshrc`:
```bash
export DEEPSEEK_API_KEY="sk-your-actual-api-key-here"
```

Then reload:
```bash
source ~/.bashrc
```

### 3. Start the Server

```bash
npm start
```

Or with the key inline:
```bash
DEEPSEEK_API_KEY=sk-your-key npm start
```

The server will start on `http://localhost:3000`

### 4. Open the App

Visit: `http://localhost:3000`

The AI chat will now use DeepSeek through your secure backend proxy.

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Serves the mindfulness app |
| `/api/health` | GET | Check server and AI status |
| `/api/chat` | POST | Send message to DeepSeek AI |
| `/api/chat-fallback` | POST | Local analysis (no API key needed) |

## Frontend Configuration

In `mindfulness/app.js`, the config is:
```javascript
apiConfig: {
    baseUrl: '',        // Empty for same-origin
    useBackend: true    // Use backend proxy
}
```

For local development with server on different port:
```javascript
apiConfig: {
    baseUrl: 'http://localhost:3000',
    useBackend: true
}
```

## Deployment Options

### Option 1: Self-Hosted Server
- Run the Node.js server on your own VPS/cloud instance
- Set `DEEPSEEK_API_KEY` as environment variable
- Users connect directly to your server

### Option 2: Railway/Render/Fly.io
- Deploy `mindfulness-server.js` to a platform like Railway
- Add `DEEPSEEK_API_KEY` in platform's environment settings
- Update frontend `baseUrl` to your deployed URL

### Option 3: Vercel/Netlify Functions
- Convert `mindfulness-server.js` to serverless functions
- Deploy frontend to Vercel/Netlify
- API key stays in serverless environment variables

## Security Notes

✅ **Safe:**
- API key in server environment variables
- Backend makes all DeepSeek calls
- Frontend never sees the key

❌ **Never do:**
- Commit API key to GitHub
- Send API key to browser
- Hardcode key in frontend JavaScript

## Troubleshooting

**"AI service not configured"**
- Server started without `DEEPSEEK_API_KEY`
- Set the environment variable and restart

**"Failed to get response from AI service"**
- DeepSeek API might be down
- Check your API key is valid
- Check internet connection

**CORS errors**
- Frontend and backend on different ports?
- Set `baseUrl` in frontend config
- Or ensure CORS is properly configured

## Files

- `mindfulness-server.js` - Express backend server
- `mindfulness-package.json` - Dependencies (rename to `package.json`)
- `mindfulness/app.js` - Frontend (calls backend API)
- `mindfulness/` - Static app files
