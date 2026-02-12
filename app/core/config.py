from dotenv import load_dotenv
import os

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPEN_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
DATABASE_URL = os.getenv("DATABASE_URL", "")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL não configurado no .env")

if not TELEGRAM_BOT_TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN não configurado no .env")