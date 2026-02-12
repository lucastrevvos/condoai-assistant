# Telegram Webhook Setup

- Local development uses ngrok to expose FastAPI
- Telegram webhook points to /webhook/telegram
- This allows real-time message handling without polling

# Commands Python

- .\.venv\Scripts\Activate.ps1
- python -m uvicorn app.main:app --reload --port 8000

https://api.telegram.org/bot8524273423:AAFUgidWOOeBljBawKlWkGoiu5G_IY6R8W4/getWebhookInfo

{
"ok": true,
"result": {
"url": "https://noelia-curlier-rochelle.ngrok-free.dev/webhook/telegram",
"has_custom_certificate": false,
"pending_update_count": 0,
"last_error_date": 1770899568,
"last_error_message": "Wrong response from the webhook: 404 Not Found",
"max_connections": 40,
"ip_address": "3.125.209.94"
}
}

https://api.telegram.org/bot8524273423:AAFUgidWOOeBljBawKlWkGoiu5G_IY6R8W4/setWebhook?url=https://noelia-curlier-rochelle.ngrok-free.dev/webhook/telegram

https://api.telegram.org/bot8524273423:AAFUgidWOOeBljBawKlWkGoiu5G_IY6R8W4/getMe