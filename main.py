import os
import logging
from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from pydantic import BaseModel, HttpUrl
from typing import Optional, Dict, Any
import uvicorn
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

import sys
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Fix for Playwright on Windows with Uvicorn
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

app = FastAPI()

class QuizRequest(BaseModel):
    email: str
    secret: str
    url: HttpUrl
    # Allow extra fields
    class Config:
        extra = "allow"

# Placeholder for the solver function
from solver import QuizSolver

async def process_quiz(email: str, secret: str, url: str):
    logger.info(f"Processing quiz for {email} at {url}")
    solver = QuizSolver()
    await solver.solve(email, secret, url)

@app.post("/run")
async def run_quiz(request: QuizRequest, background_tasks: BackgroundTasks):
    # Verify secret (simple check against env var or hardcoded for now as per user request to just "fill out form")
    # In a real scenario, we might validate against a stored secret.
    # The prompt says: "Verify the secret matches what you provided in the Google Form."
    # We will assume the user sets a local env var for their own secret to verify incoming requests match it?
    # Or simply accept it if it matches our expected secret.
    
    expected_secret = os.getenv("QUIZ_SECRET", "default_secret")
    
    if request.secret != expected_secret:
        raise HTTPException(status_code=403, detail="Invalid secret")

    # Start background task to solve the quiz
    background_tasks.add_task(process_quiz, request.email, request.secret, str(request.url))

    return {"message": "Quiz processing started", "status": "success"}

@app.get("/")
def read_root():
    return {"message": "Quiz Solver Bot is running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
