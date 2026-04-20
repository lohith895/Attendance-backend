from fastapi import APIRouter, Depends
from app.auth import verify_token
from app.utils.image import base64_to_image
from app.ai.detector import detect_faces
from app.ai.recognizer import get_embedding
from app.database import supabase
from app.config import SIMILARITY_THRESHOLD
from sklearn.metrics.pairwise import cosine_similarity

router = APIRouter(prefix="/api")

@router.post("/face-recognition")
def recognize(payload: dict, user=Depends(verify_token)):
    img = base64_to_image(payload["image"])
    faces = detect_faces(img)

    students = supabase.table("students").select(
        "id,roll_number,full_name,face_embedding_id"
    ).eq("section_id", payload["section_id"]).execute().data

    # Pre-load all embeddings in one pass, skip unregistered students
    student_embeddings = []
    for s in students:
        if not s["face_embedding_id"]:  # 👈 skip students with no face registered
            continue

        stored = supabase.table("face_embeddings").select(
            "embedding"
        ).eq("id", s["face_embedding_id"]).execute().data

        if not stored:  # 👈 skip if embedding record missing
            continue

        student_embeddings.append({
            "student": s,
            "embedding": stored[0]["embedding"]
        })

    recognized, unrecognized = [], []

    if not student_embeddings:
        return {
            "success": False,
            "faces_detected": len(faces),
            "recognized": [],
            "unrecognized": [],
            "error": "No trained students found in this section"
        }

    for _, box in faces:
        emb = get_embedding(img)
        if emb is None:
            unrecognized.append({"bounding_box": box})
            continue

        best, score = None, 0

        for se in student_embeddings:
            sim = cosine_similarity([emb], [se["embedding"]])[0][0]
            if sim > score:
                score, best = sim, se["student"]

        if score >= SIMILARITY_THRESHOLD:
            recognized.append({
                "student_id": best["id"],
                "roll_number": best["roll_number"],
                "student_name": best["full_name"],
                "confidence": float(score),
                "bounding_box": box
            })
        else:
            unrecognized.append({"bounding_box": box})

    return {
        "success": True,
        "faces_detected": len(faces),
        "recognized": recognized,
        "unrecognized": unrecognized
    }