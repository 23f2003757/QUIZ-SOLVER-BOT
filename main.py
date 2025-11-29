import os
import logging
from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from pydantic import BaseModel, HttpUrl
from typing import Optional, Dict, Any
import uvicorn
from dotenv import load_dotenv

load_dotenv()

import sys
import asyncio
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

app = FastAPI()

class QuizRequest(BaseModel):
    email: str
    secret: str
    url: HttpUrl
    class Config:
        extra = "allow"

from solver import QuizSolver

async def process_quiz(email: str, secret: str, url: str):
    logger.info(f"Processing quiz for {email} at {url}")
    solver = QuizSolver()
    await solver.solve(email, secret, url)

@app.post("/run")
async def run_quiz(request: QuizRequest, background_tasks: BackgroundTasks):
    
    expected_secret = os.getenv("QUIZ_SECRET", "default_secret")
    
    if request.secret != expected_secret:
        raise HTTPException(status_code=403, detail="Invalid secret")

    background_tasks.add_task(process_quiz, request.email, request.secret, str(request.url))

    return {"message": "Quiz processing started", "status": "success"}

@app.get("/")
def read_root():
    return {"message": "Quiz Solver Bot is running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
