from fastapi import APIRouter, Depends
from app.auth import verify_token
from app.utils.image import base64_to_image
from app.ai.detector import detect_faces
from app.ai.recognizer import get_embedding
from app.ai.quality import is_face_clear
from app.database import supabase
import numpy as np

router = APIRouter(prefix="/api")

@router.post("/face-training")
def single_training(payload: dict, user=Depends(verify_token)):
    student_id = payload["student_id"]
    images = payload["images"]

    embeddings = []

    for img64 in images:
        img = base64_to_image(img64)
        faces = detect_faces(img)

        if len(faces) != 1:
            return {"success": False, "error": "multiple_faces"}

        # YOLO is used ONLY as a gatekeeper
        if len(faces) != 1:
            return {"success": False, "error": "multiple_faces"}

        # Quality check can stay on crop
        face_crop, _ = faces[0]
        if not is_face_clear(face_crop):
            return {"success": False, "error": "low_quality"}

        # 🔥 PASS FULL IMAGE TO INSIGHTFACE
        emb = get_embedding(img)
        if emb is None:
            return {"success": False, "error": "face_not_detected"}

        embeddings.append(emb)

    avg_emb = np.mean(embeddings, axis=0).tolist()
    emb_id = f"emb_{student_id}"

    supabase.table("face_embeddings").insert({
        "id": emb_id,
        "embedding": avg_emb
    }).execute()

    supabase.table("students").update({
        "face_registered": True,
        "face_embedding_id": emb_id
    }).eq("id", student_id).execute()

    return {
        "success": True,
        "student_id": student_id,
        "face_embedding_id": emb_id,
        "message": "Face model trained successfully",
        "confidence_score": 0.95
    }

@router.post("/face-training/bulk")
def bulk_training(payload: dict, user=Depends(verify_token)):
    results = []
    trained = failed = 0

    for s in payload["students"]:
        img64 = payload["images"].get(str(s["serial_no"]))
        if not img64:
            failed += 1
            continue

        img = base64_to_image(img64)
        faces = detect_faces(img)

        if len(faces) != 1:
            failed += 1
            results.append({"serial_no": s["serial_no"], "status": "failed"})
            continue

        face_crop, _ = faces[0]
        emb = get_embedding(img)
        if emb is None:
            failed += 1
            continue

        emb_id = f"emb_{s['roll_number']}"
        supabase.table("face_embeddings").insert({
            "id": emb_id,
            "embedding": emb.tolist()
        }).execute()

        trained += 1
        results.append({
            "serial_no": s["serial_no"],
            "roll_number": s["roll_number"],
            "status": "success",
            "face_embedding_id": emb_id
        })

    return {
        "success": True,
        "total": len(payload["students"]),
        "trained": trained,
        "failed": failed,
        "results": results
    }
