# Quiz Solver Bot

## Setup

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    playwright install chromium
    ```

2.  **Environment Variables**:
    - Copy `.env.example` to `.env`.
    - Set your `OPENAI_API_KEY`.
    - Set a `QUIZ_SECRET` (this is the secret you provide in the Google Form).

## Running the Bot

Start the server:
```bash
uvicorn main:app --reload
```

## Usage

The bot listens on `POST /run`.
Payload:
```json
{
  "email": "your_email@example.com",
  "secret": "your_secret",
  "url": "https://example.com/quiz-start"
}
```

## Contest Prompts

See `contest_prompts.md` for the System and User prompts required for the form.
