import logging
import os
import secrets

from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger("feedback")

ALGORITHM = "HS256"
TOKEN_TTL_MINUTES = int(os.getenv("TOKEN_TTL_MINUTES", "60"))

SECRET_KEY = os.getenv("JWT_SECRET")
if not SECRET_KEY:
    # Fail safe instead of crashing: a random per-process key is secure, but
    # every restart signs users out. Set JWT_SECRET in production.
    SECRET_KEY = secrets.token_urlsafe(32)
    logger.warning("JWT_SECRET is not set; using a random key (tokens reset on restart)")

CORS_ORIGINS = [
    o.strip()
    for o in os.getenv(
        "CORS_ORIGINS",
        "http://localhost:3000,https://lightweight-feedback-system-5clk.onrender.com",
    ).split(",")
    if o.strip()
]
