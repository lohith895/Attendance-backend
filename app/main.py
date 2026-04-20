from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import health, training, recognition, model

app = FastAPI(title="AI Face Attendance Backend")

# ✅ CORS FIX (VERY IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for development
    allow_credentials=True,
    allow_methods=["*"],  # allows OPTIONS
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(training.router)
app.include_router(recognition.router)
app.include_router(model.router)
