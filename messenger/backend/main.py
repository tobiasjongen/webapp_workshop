from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from datetime import datetime

app = FastAPI(title="Simple Messenger API")

# Add CORS middleware to allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

messages = []

# Pydantic models for request/response
class MessageCreate(BaseModel):
    username: str
    content: str

class Message(BaseModel):
    id: int
    username: str
    content: str
    timestamp: str

class LoginRequest(BaseModel):
    username: str

@app.get("/")
def read_root():
    return {"message": "Simple Messenger API"}

@app.post("/login")
def login(request: LoginRequest):
    """Simple login endpoint - just validates username exists"""
    if not request.username or request.username.strip() == "":
        raise HTTPException(status_code=400, detail="Username cannot be empty")
    
    return {"message": f"Welcome {request.username}!", "username": request.username}

@app.get("/messages", response_model=List[Message])
def get_messages():
    """Get all messages in chronological order"""
    return messages

@app.post("/messages", response_model=Message)
def send_message(message: MessageCreate):
    """Send a new message"""
    if not message.username or message.username.strip() == "":
        raise HTTPException(status_code=400, detail="Username cannot be empty")
    
    if not message.content or message.content.strip() == "":
        raise HTTPException(status_code=400, detail="Message content cannot be empty")
    
    # Create new message
    new_message = {
        "id": len(messages) + 1,
        "username": message.username.strip(),
        "content": message.content.strip(),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    messages.append(new_message)
    return new_message

@app.delete("/messages")
def clear_messages():
    """Clear all messages (for testing purposes)"""
    global messages
    messages = []
    return {"message": "All messages cleared"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)