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
    face = max(faces, key=lambda f: f.bbox[2] * f.bbox[3])

    emb = face.embedding
    return emb / np.linalg.norm(emb)