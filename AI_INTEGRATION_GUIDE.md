# 🤖 AI Pharmacy Assistant - Integration Guide

## What You Have Now

✅ **AI-powered chatbot** using Google Gemini
✅ **Beautiful chat widget** that floats at bottom-right
✅ **FastAPI backend** with error handling
✅ **Easy integration** - just copy/paste code!

---

## 📁 Files You Need

```
Pharmacy_app/
├── ai_assistant_app.py         ← Backend (improved version)
├── medicines.json               ← Medicine database (or use medicines_updated.json)
└── chat_widget.html             ← Chat widget code
```

---

## 🚀 Quick Setup (3 Steps)

### Step 1: Setup Backend

1. **Save the improved backend:**
```bash
cd Pharmacy_app
# Save ai_assistant_app.py to your folder
```

2. **Install dependencies:**
```bash
pip install fastapi uvicorn google-generativeai
```

3. **Run the AI backend:**
```bash
python ai_assistant_app.py
```

You should see:
```
✅ Google Gemini AI initialized
✅ Medicines loaded: 12
Server running on http://localhost:8001
```

### Step 2: Add Widget to Your Website

Open any HTML page where you want the chatbot and add this **before the closing `</body>` tag:**

```html
<!-- AI Assistant Chat Widget -->
<div id="pharma-ai-widget">
  <!-- Chat Button -->
  <button id="chat-toggle-btn" class="chat-toggle-btn">
    <svg id="chat-icon" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor">
      <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
    </svg>
    <svg id="close-icon" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" style="display: none;">
      <line x1="18" y1="6" x2="6" y2="18"></line>
      <line x1="6" y1="6" x2="18" y2="18"></line>
    </svg>
  </button>
  
  <!-- Copy the rest from chat_widget.html -->
</div>

<style>
  /* Copy all styles from chat_widget.html */
</style>

<script>
  // Copy all JavaScript from chat_widget.html
  const API_BASE_URL = 'http://localhost:8001';  // Your backend URL
</script>
```

**OR** simply include it as an external file:

```html
<!-- At the bottom of your HTML page -->
<iframe src="chat_widget.html" 
        style="position: fixed; bottom: 20px; right: 20px; 
               border: none; z-index: 9999; width: 400px; height: 600px;">
</iframe>
```

### Step 3: Test It!

1. Open your website in browser
2. Click the purple chat button at bottom-right
3. Try asking: "I have a headache"
4. You should get an AI response! 🎉

---

## 🎨 How It Looks

**Chat Button (Closed):**
```
                                    [🤖]  ← Purple floating button
```

**Chat Window (Open):**
```
┌─────────────────────────┐
│ 🤖 AI Pharmacy Assistant│
│ Online                   │
├─────────────────────────┤
│                          │
│ [Bot] Hi! I can help...  │
│                          │
│          [You] Headache  │
│                          │
│ [Bot] Try Paracetamol... │
│                          │
├─────────────────────────┤
│ [🤕 Headache] [🤧 Cold]  │
├─────────────────────────┤
│ Type message...      [→] │
└─────────────────────────┘
```

---

## ⚙️ Configuration

### Change Backend URL (for deployment):

In `chat_widget.html`, find this line:
```javascript
const API_BASE_URL = 'http://localhost:8001';
```

Change to your deployed URL:
```javascript
const API_BASE_URL = 'https://your-api.herokuapp.com';
// or
const API_BASE_URL = 'https://api.yoursite.com';
```

### Change Colors:

Find this in the CSS:
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

Replace with your brand colors:
```css
background: linear-gradient(135deg, #2e7d32 0%, #1b5e20 100%); /* Green */
```

### Change Position:

The widget is at bottom-right by default. To move it:

```css
#pharma-ai-widget {
  position: fixed;
  bottom: 20px;
  right: 20px;  /* Change to 'left: 20px' for bottom-left */
}
```

---

## 🔒 Security (IMPORTANT!)

### 1. Protect Your API Key

**Never commit API keys to GitHub!**

Instead, use environment variables:

```bash
# Create .env file
echo "GOOGLE_API_KEY=AIzaSyBPjAkGBSzNLddP9Kp-EoMvOIbkQT6cx3M" > .env

# Add to .gitignore
echo ".env" >> .gitignore
```

Then in `ai_assistant_app.py`:
```python
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
```

### 2. Update CORS for Production

In `ai_assistant_app.py`, change:
```python
allow_origins=["*"]  # Development only!
```

To:
```python
allow_origins=["https://yourwebsite.com"]  # Production
```

---

## 📱 Mobile Responsive

The chat widget is already mobile-friendly! It automatically adjusts on smaller screens.

---

## 🎯 Customization Ideas

### Add More Quick Actions:

```html
<button class="quick-action-btn" onclick="sendQuickMessage('Medicine for fever')">
  🌡️ Fever
</button>
<button class="quick-action-btn" onclick="sendQuickMessage('Allergy medicine')">
  🤧 Allergies
</button>
```

### Add Medicine Images:

Update `medicines.json`:
```json
{
  "medicine": "Paracetamol",
  "use": "fever headache",
  "dose": "500mg",
  "warning": "Max 4 per day",
  "image": "https://example.com/paracetamol.jpg"
}
```

### Track Conversations:

Add to JavaScript:
```javascript
function sendMessage() {
  // ... existing code ...
  
  // Track conversation
  fetch('/api/analytics', {
    method: 'POST',
    body: JSON.stringify({
      query: message,
      timestamp: new Date().toISOString()
    })
  });
}
```

---

## 🚀 Deploy to Production

### Option 1: Deploy Backend to Heroku

```bash
# Create Procfile
echo "web: uvicorn ai_assistant_app:app --host 0.0.0.0 --port \$PORT" > Procfile

# Deploy
git init
git add .
git commit -m "AI assistant"
heroku create your-ai-assistant
git push heroku main

# Set API key
heroku config:set GOOGLE_API_KEY=AIzaSyBPjAkGBSzNLddP9Kp-EoMvOIbkQT6cx3M
```

Your API will be at: `https://your-ai-assistant.herokuapp.com`

### Option 2: Deploy Backend to Google Cloud Run

```bash
# Create Dockerfile
cat > Dockerfile << EOF
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD uvicorn ai_assistant_app:app --host 0.0.0.0 --port 8080
EOF

# Deploy
gcloud builds submit --tag gcr.io/PROJECT_ID/ai-assistant
gcloud run deploy --image gcr.io/PROJECT_ID/ai-assistant --platform managed
```

### Deploy Frontend

Your chat widget is just HTML/CSS/JS - it works on any hosting:
- GitHub Pages
- Netlify
- Vercel
- Your existing website

Just update the `API_BASE_URL` to your deployed backend!

---

## 🧪 Testing

### Test Backend API:

```bash
# Health check
curl http://localhost:8001/

# Test chat
curl -X POST http://localhost:8001/chat \
  -H "Content-Type: application/json" \
  -d '{"text": "I have a headache"}'
```

### Test Frontend:

1. Open browser console (F12)
2. You should see: `✅ AI Assistant API connected`
3. Send a test message
4. Check Network tab for API calls

---

## 🐛 Troubleshooting

### Chat button not appearing:
- Check if JavaScript loaded (view page source)
- Check browser console for errors
- Make sure z-index is high enough

### API not responding:
- Check backend is running: `curl http://localhost:8001/`
- Check CORS settings
- Check API_BASE_URL in JavaScript

### AI gives weird responses:
- Check medicine database has good data
- Improve the prompt in `ai_assistant_app.py`
- Increase medicine descriptions

### "API key not valid" error:
- Check your Google API key is active
- Enable Gemini API in Google Cloud Console
- Check API key has no extra spaces

---

## 📊 Analytics (Optional)

Track how users interact with your chatbot:

```javascript
// Add to sendMessage() function
gtag('event', 'chat_message', {
  'query': message,
  'timestamp': new Date().toISOString()
});
```

---

## 🎓 Next Steps

1. ✅ Add more medicines to `medicines.json`
2. ✅ Improve AI prompts for better responses
3. ✅ Add user authentication (connect to your main API)
4. ✅ Track conversation history
5. ✅ Add prescription upload feature
6. ✅ Integrate with your medicine inventory
7. ✅ Add payment for medicine purchases
8. ✅ Deploy to production!

---

## 💡 Pro Tips

1. **Keep responses short** - Mobile users prefer quick answers
2. **Add disclaimers** - Always remind users you're not a doctor
3. **Test with real users** - Get feedback on the AI responses
4. **Monitor API usage** - Google Gemini has usage limits
5. **Cache common questions** - Reduce API calls for FAQs

---

## 📞 Need Help?

If something's not working:
1. Check the console for errors (F12)
2. Verify backend is running
3. Test API endpoints with curl
4. Check CORS settings
5. Verify API key is valid

---

**You're all set! 🎉 Your AI pharmacy assistant is ready to help users!**
