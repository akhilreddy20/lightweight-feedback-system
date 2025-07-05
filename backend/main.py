from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth import auth_router

app = FastAPI()

# ✅ Allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("🚀 FastAPI app is starting...")

app.include_router(auth_router)
