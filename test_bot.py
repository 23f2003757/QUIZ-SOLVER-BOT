import requests
import os
from dotenv import load_dotenv

load_dotenv()

def test_local_bot():
    url = "http://localhost:8000/run"
    email = os.getenv("STUDENT_EMAIL", "test@example.com")
    secret = os.getenv("QUIZ_SECRET", "default_secret")

    quiz_url = "https://tds-llm-analysis.s-anand.net/demo"
    
    payload = {
        "email": email,
        "secret": secret,
        "url": quiz_url
    }
    
    print(f"Sending request to {url} with payload: {payload}")
    
    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure the server is running: uvicorn main:app --reload")

if __name__ == "__main__":
    test_local_bot()