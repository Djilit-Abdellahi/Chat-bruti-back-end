from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from core import ChatBrutiGPT
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Enable CORS for Frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserMessage(BaseModel):
    message: str

# Initialize the bot
# Ensure you have your .env file with OPENAI_API_KEY defined
bot = ChatBrutiGPT(data_path_prefix='.')

@app.post("/chat")
def chat_endpoint(user_msg: UserMessage):
    if not user_msg.message:
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    result = bot.get_response(user_msg.message)
    return result