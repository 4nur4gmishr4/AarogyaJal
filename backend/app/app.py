from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
import os
from datetime import datetime
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from models import SmartMoneyModel, User, UserRole, get_smart_money_instance

# Load environment variables
load_dotenv()

# Configure API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set")
genai.configure(api_key=api_key)

# Create FastAPI app
app = FastAPI(title="AarogyaJal Gemini API Service")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Water quality context for Gemini
WATER_QUALITY_CONTEXT = """
Context: Water Quality Analysis System
Focus Areas:
- Water quality parameters and their significance
- Waterborne diseases and their prevention
- Water treatment methods and recommendations
- Public health implications of water quality
- Safety measures and preventive actions
"""

# Model configuration
MODEL = "gemini-2.5-flash"

# Initialize SmartMoney model with anuraga as admin
smart_money = get_smart_money_instance()

# Request models
class ChatRequest(BaseModel):
    query: str

class AnalysisRequest(BaseModel):
    parameters: dict
    location: str = None
    notes: str = None

@app.get("/")
async def root():
    return {"message": "AarogyaJal Gemini API Service"}

# SmartMoney Model Endpoints
@app.get("/smartmoney")
async def get_smart_money_info():
    """Get SmartMoney model information including admins"""
    return {
        "name": smart_money.name,
        "description": smart_money.description,
        "admins": smart_money.admins,
        "total_users": len(smart_money.users),
        "created_at": smart_money.created_at.isoformat(),
        "updated_at": smart_money.updated_at.isoformat()
    }

@app.get("/smartmoney/admins")
async def get_admins():
    """Get list of admins in SmartMoney model"""
    return {"admins": smart_money.admins}

@app.get("/smartmoney/users")
async def get_users():
    """Get all users in SmartMoney model"""
    return {
        "users": [
            {
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "is_active": user.is_active,
                "created_at": user.created_at.isoformat() if user.created_at else None
            }
            for user in smart_money.users
        ]
    }

@app.get("/smartmoney/users/{username}")
async def get_user(username: str):
    """Get specific user information"""
    user = smart_money.get_user(username)
    if not user:
        raise HTTPException(status_code=404, detail=f"User '{username}' not found")
    
    return {
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "is_admin": smart_money.is_admin(user.username),
        "is_active": user.is_active,
        "created_at": user.created_at.isoformat() if user.created_at else None
    }

@app.post("/smartmoney/users")
async def add_user(user: User):
    """Add a new user to SmartMoney model"""
    if smart_money.add_user(user):
        return {
            "message": "User added successfully",
            "user": {
                "username": user.username,
                "role": user.role,
                "is_admin": smart_money.is_admin(user.username)
            }
        }
    raise HTTPException(status_code=400, detail="User already exists")

@app.post("/smartmoney/admins/{username}")
async def add_admin(username: str):
    """Add a user as admin in SmartMoney model"""
    if smart_money.add_admin(username):
        # Update user role if user exists
        user = smart_money.get_user(username)
        if user:
            user.role = UserRole.ADMIN
        return {
            "message": f"'{username}' added as admin successfully",
            "admins": smart_money.admins
        }
    raise HTTPException(status_code=400, detail=f"'{username}' is already an admin")

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        model = genai.GenerativeModel(MODEL)
        response = model.generate_content(
            f"{WATER_QUALITY_CONTEXT}\n\nUser Query: {request.query}\n\n"
            f"Provide a helpful response focused on water quality and health."
        )
        
        return {"response": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze")
async def analyze_water_quality(request: AnalysisRequest):
    try:
        # Format the parameters for analysis
        params_text = "\n".join([f"{k}: {v}" for k, v in request.parameters.items()])
        location_info = f"Location: {request.location}" if request.location else ""
        notes_info = f"Notes: {request.notes}" if request.notes else ""
        
        prompt = f"{WATER_QUALITY_CONTEXT}\n\nWater Quality Parameters:\n{params_text}\n{location_info}\n{notes_info}\n\n"
        prompt += "Analyze these water quality parameters and provide:\n"
        prompt += "1. Overall water quality assessment\n"
        prompt += "2. Health implications\n"
        prompt += "3. Recommendations for treatment or improvement\n"
        prompt += "4. Potential risks if any parameters are concerning"
        
        model = genai.GenerativeModel(MODEL)
        response = model.generate_content(prompt)
        
        return {
            "analysis": response.text,
            "timestamp": str(datetime.now().isoformat())
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)