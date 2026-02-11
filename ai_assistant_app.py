"""
AI-Powered Pharmacy Assistant - Improved Backend
To be embedded as chatbot widget in main website
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os
from typing import List, Optional
import google.generativeai as genai
from datetime import datetime



app = FastAPI(
    title="Pharma AI Assistant",
    description="AI-powered medicine recommendation chatbot",
    version="2.0.0"
)

# CORS - Allow your main website to access this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your actual domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Google AI Configuration
# SECURITY: Move API key to environment variable in production!
API_KEY = os.getenv("GOOGLE_API_KEY", "AIzaSyBPjAkGBSzNLddP9Kp-EoMvOIbkQT6cx3M")

try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    print("✅ Google Gemini AI initialized")
except Exception as e:
    print(f"❌ Error initializing AI: {e}")
    model = None

# =============================================================================
# DATA MODELS
# =============================================================================

class ChatMessage(BaseModel):
    text: str
    user_id: Optional[str] = "anonymous"

class ChatResponse(BaseModel):
    answer: str
    suggested_medicines: List[dict]
    should_see_doctor: bool
    timestamp: str

# =============================================================================
# LOAD MEDICINES DATA
# =============================================================================

medicines = []

def load_medicines():
    """Load medicines database"""
    global medicines
    try:
        with open("medicines.json") as f:
            medicines = json.load(f)
        print(f"✅ Loaded {len(medicines)} medicines")
    except FileNotFoundError:
        print("⚠️  medicines.json not found, using default data")
        medicines = [
            {
                "medicine": "Paracetamol",
                "use": "fever headache pain body ache",
                "dose": "500mg every 6 hours",
                "warning": "Max 4 per day. Avoid alcohol."
            },
            {
                "medicine": "Cetirizine",
                "use": "allergy cold sneezing runny nose",
                "dose": "10mg once daily",
                "warning": "May cause drowsiness"
            },
            {
                "medicine": "ORS",
                "use": "dehydration diarrhea vomiting",
                "dose": "1 sachet in water",
                "warning": "Drink slowly"
            }
        ]
    except Exception as e:
        print(f"❌ Error loading medicines: {e}")
        medicines = []

# Load medicines on startup
load_medicines()

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def search_medicine(symptom: str) -> List[dict]:
    """Search for relevant medicines based on symptoms"""
    results = []
    symptom_words = set(symptom.lower().split())
    
    for med in medicines:
        use_words = set(med["use"].lower().split())
        # Check if any symptom word matches the medicine use
        if symptom_words & use_words:  # Set intersection
            results.append(med)
    
    return results

def assess_severity(text: str) -> str:
    """Assess severity of symptoms"""
    serious_keywords = [
        'chest pain', 'difficulty breathing', 'severe pain', 'bleeding',
        'unconscious', 'seizure', 'stroke', 'heart attack', 'suicide',
        'emergency', 'cant breathe', 'blood', 'broken bone'
    ]
    
    text_lower = text.lower()
    for keyword in serious_keywords:
        if keyword in text_lower:
            return "severe"
    
    return "mild"

# =============================================================================
# API ENDPOINTS
# =============================================================================

@app.get("/")
def root():
    """Health check"""
    return {
        "status": "healthy",
        "service": "Pharma AI Assistant",
        "version": "2.0.0",
        "medicines_loaded": len(medicines)
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """
    Main chat endpoint for AI assistant
    """
    if not model:
        raise HTTPException(status_code=503, detail="AI service unavailable")
    
    if not message.text or message.text.strip() == "":
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    try:
        # Search for relevant medicines
        relevant_meds = search_medicine(message.text)
        
        # Assess severity
        severity = assess_severity(message.text)
        should_see_doctor = severity == "severe"
        
        # Build AI prompt
        prompt = f"""You are a helpful pharmacy AI assistant. Be friendly and concise.

User says: "{message.text}"

Available OTC medicines in our database:
{json.dumps(relevant_meds, indent=2) if relevant_meds else "No specific matches found"}

Instructions:
1. If symptoms are serious (chest pain, difficulty breathing, severe injuries, etc.) → Tell user to seek immediate medical help
2. For mild symptoms → Suggest appropriate OTC medicine from the list
3. Always include dosage and warnings
4. Keep response SHORT (2-3 sentences max)
5. Be empathetic and helpful

Response format:
[Your suggestion here]

Medicine: [Name if applicable]
Dose: [Dosage if applicable]
⚠️ Warning: [Warning if applicable]
"""

        # Get AI response
        response = model.generate_content(prompt)
        answer_text = response.text.strip()
        
        # Return formatted response
        return ChatResponse(
            answer=answer_text,
            suggested_medicines=relevant_meds[:3],  # Top 3 matches
            should_see_doctor=should_see_doctor,
            timestamp=datetime.utcnow().isoformat()
        )
        
    except Exception as e:
        print(f"❌ Error in chat endpoint: {e}")
        raise HTTPException(
            status_code=500,
            detail="Sorry, I'm having trouble processing your request. Please try again."
        )

@app.post("/ask")
def ask_legacy(q: ChatMessage):
    """
    Legacy endpoint for backward compatibility
    """
    try:
        response = chat(q)
        return {"answer": response.answer}
    except Exception as e:
        return {"answer": f"Sorry, I encountered an error: {str(e)}"}

@app.get("/medicines")
def get_all_medicines():
    """Get all medicines in database"""
    return {
        "total": len(medicines),
        "medicines": medicines
    }

@app.get("/medicines/search/{symptom}")
def search_medicines_endpoint(symptom: str):
    """Search medicines by symptom"""
    results = search_medicine(symptom)
    return {
        "query": symptom,
        "count": len(results),
        "medicines": results
    }

# =============================================================================
# STARTUP EVENT
# =============================================================================

@app.on_event("startup")
async def startup_event():
    print("\n" + "="*60)
    print("🤖 Pharma AI Assistant Starting...")
    print("="*60)
    print(f"✅ Medicines loaded: {len(medicines)}")
    print(f"✅ AI Model: {'Initialized' if model else 'Not available'}")
    print("="*60 + "\n")

# =============================================================================
# RUN SERVER
# =============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")
