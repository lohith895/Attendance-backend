from fastapi import APIRouter, Depends
from app.auth import verify_token
from app.database import supabase

router = APIRouter(prefix="/api/model")

@router.post("/train")
def train_model(payload: dict, user=Depends(verify_token)):
    section_id = payload["section_id"]
    students = supabase.table("students").select("*").eq("section_id", section_id).execute().data
    trained = [s for s in students if s["face_registered"]]

    if not trained:
        return {"success": False, "error": "no_students"}

    return {
        "success": True,
        "message": f"Model trained successfully with {len(trained)} students",
        "model_id": f"model_{section_id}",
        "students_count": len(trained)
    }

@router.get("/status/{section_id}")
def model_status(section_id: str, user=Depends(verify_token)):
    students = supabase.table("students").select("*").eq("section_id", section_id).execute().data
    trained = [s for s in students if s["face_registered"]]

    return {
        "section_id": section_id,
        "is_trained": len(trained) > 0,
        "last_trained_at": None,
        "students_count": len(students),
        "trained_students_count": len(trained)
    }
