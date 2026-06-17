from fastapi import APIRouter, Depends
from app.auth import verify_token
from app.utils.image import base64_to_image
from app.ai.recognizer import get_embedding, get_all_embeddings
from app.ai.quality import verify_liveness
from app.utils.sms import send_whatsapp_alert
from app.database import supabase
from app.config import SIMILARITY_THRESHOLD
from sklearn.metrics.pairwise import cosine_similarity

router = APIRouter(prefix="/api")

def _load_student_embeddings(section_id: str):
    """Fetch all students in the section that have a registered face embedding."""
    students = supabase.table("students").select(
        "id,roll_number,full_name,face_embedding_id"
    ).eq("section_id", section_id).execute().data

    result = []
    for s in students:
        if not s["face_embedding_id"]:
            continue
        stored = supabase.table("face_embeddings").select(
            "embedding"
        ).eq("id", s["face_embedding_id"]).execute().data
        if not stored:
            continue
        result.append({"student": s, "embedding": stored[0]["embedding"]})
    return result

def _match_face(emb, student_embeddings):
    """Return (best_student, score) for the closest stored embedding."""
    best, score = None, 0.0
    for se in student_embeddings:
        sim = float(cosine_similarity([emb], [se["embedding"]])[0][0])
        if sim > score:
            score, best = sim, se["student"]
    return best, score

@router.post("/face-recognition")
def recognize(payload: dict, user=Depends(verify_token)):
    img = base64_to_image(payload["image"])

    # Use InsightFace on the FULL frame — same context as training embeddings.
    # This is critical: training also calls get_embedding(full_image), so embeddings
    # are only comparable when extracted at the same scale/context.
    all_faces = get_all_embeddings(img)

    student_embeddings = _load_student_embeddings(payload["section_id"])

    recognized, unrecognized = [], []

    if not student_embeddings:
        return {
            "success": True,
            "faces_detected": len(all_faces),
            "recognized": [],
            "unrecognized": [{"bounding_box": f["bbox"]} for f in all_faces],
            "error": "No trained students found in this section"
        }

    h, w, _ = img.shape
    for face_data in all_faces:
        box = face_data["bbox"]
        emb = face_data["embedding"]

        # Crop for liveness check only (embedding already computed above)
        x1 = max(0, box["x"])
        y1 = max(0, box["y"])
        x2 = min(w, box["x"] + box["width"])
        y2 = min(h, box["y"] + box["height"])
        face_crop = img[y1:y2, x1:x2]

        if not verify_liveness(face_crop):
            unrecognized.append({
                "bounding_box": box,
                "spoof": True,
                "message": "Spoof detected"
            })
            continue

        best, score = _match_face(emb, student_embeddings)

        if best and score >= SIMILARITY_THRESHOLD:
            recognized.append({
                "student_id": best["id"],
                "roll_number": best["roll_number"],
                "student_name": best["full_name"],
                "confidence": score,
                "bounding_box": box
            })
        else:
            unrecognized.append({"bounding_box": box})

    return {
        "success": True,
        "faces_detected": len(all_faces),
        "recognized": recognized,
        "unrecognized": unrecognized
    }

@router.post("/face-recognition/crops")
def recognize_crops(payload: dict, user=Depends(verify_token)):
    section_id = payload["section_id"]
    crops = payload.get("crops", [])

    student_embeddings = _load_student_embeddings(section_id)

    recognized, unrecognized = [], []

    if not student_embeddings:
        return {
            "success": True,
            "faces_detected": len(crops),
            "recognized": [],
            "unrecognized": [{"bounding_box": crop["bounding_box"]} for crop in crops],
            "error": "No trained students found in this section"
        }

    for crop_data in crops:
        crop_img = base64_to_image(crop_data["image"])
        box = crop_data["bounding_box"]

        if not verify_liveness(crop_img):
            unrecognized.append({
                "bounding_box": box,
                "spoof": True,
                "message": "Spoof detected"
            })
            continue

        emb = get_embedding(crop_img)
        if emb is None:
            unrecognized.append({"bounding_box": box})
            continue

        best, score = _match_face(emb, student_embeddings)

        if best and score >= SIMILARITY_THRESHOLD:
            recognized.append({
                "student_id": best["id"],
                "roll_number": best["roll_number"],
                "student_name": best["full_name"],
                "confidence": score,
                "bounding_box": box
            })
        else:
            unrecognized.append({"bounding_box": box})

    return {
        "success": True,
        "faces_detected": len(crops),
        "recognized": recognized,
        "unrecognized": unrecognized
    }

@router.post("/alerts/whatsapp")
def trigger_whatsapp_alert(payload: dict, user=Depends(verify_token)):
    teacher_phone = payload.get("teacher_phone", "+91 99999 99999")
    parent_phone = payload.get("parent_phone")
    student_name = payload.get("student_name")
    subject_name = payload.get("subject_name")
    subject_code = payload.get("subject_code")
    
    if not parent_phone or not student_name:
        return {"success": False, "error": "Missing parameters"}
        
    result = send_whatsapp_alert(
        teacher_phone=teacher_phone,
        parent_phone=parent_phone,
        student_name=student_name,
        subject_name=subject_name,
        subject_code=subject_code
    )
    return result