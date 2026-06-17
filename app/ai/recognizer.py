import insightface
import numpy as np
import cv2

app = insightface.app.FaceAnalysis(name="buffalo_l")
app.prepare(ctx_id=0)

def get_embedding(image):
    # Convert BGR → RGB (VERY IMPORTANT)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    faces = app.get(rgb)
    if not faces:
        return None

    # Take the largest face (safety)
    face = max(faces, key=lambda f: (f.bbox[2] - f.bbox[0]) * (f.bbox[3] - f.bbox[1]))

    emb = face.embedding
    if emb is None:
        return None
    return emb / np.linalg.norm(emb)

def get_all_embeddings(image):
    """
    Runs InsightFace on the full frame and returns all detected faces
    with their normalized embeddings and bounding boxes.
    Used by recognition to match the full-image context of training embeddings.
    """
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    faces = app.get(rgb)
    result = []
    for face in faces:
        emb = face.embedding
        if emb is None:
            continue
        norm = np.linalg.norm(emb)
        if norm == 0:
            continue
        x1, y1, x2, y2 = map(int, face.bbox)
        result.append({
            "embedding": emb / norm,
            "bbox": {
                "x": max(0, x1),
                "y": max(0, y1),
                "width": max(0, x2 - x1),
                "height": max(0, y2 - y1),
            },
        })
    return result