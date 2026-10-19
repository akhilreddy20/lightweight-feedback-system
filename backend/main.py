import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from auth import auth_router
from config import CORS_ORIGINS
from feedback import router as feedback_router

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")

app = FastAPI(title="Lightweight Feedback System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(feedback_router)


@app.get("/")
def root():
    return {"status": "ok", "service": "lightweight-feedback-system"}


@app.get("/health")
def health():
    return {"status": "ok"}
