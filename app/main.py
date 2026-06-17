import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import health, training, recognition, model

app = FastAPI(title="AI Face Attendance Backend")

# ✅ CORS FIX
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(training.router)
app.include_router(recognition.router)
app.include_router(model.router)
