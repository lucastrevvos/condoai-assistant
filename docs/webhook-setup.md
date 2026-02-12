# Telegram Webhook Setup

- Local development uses ngrok to expose FastAPI
- Telegram webhook points to /webhook/telegram
- This allows real-time message handling without polling

# Commands Python

- .\.venv\Scripts\Activate.ps1
- python -m uvicorn app.main:app --reload --port 8000
