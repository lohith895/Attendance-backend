import cv2

def is_face_clear(face):
    gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
    return cv2.Laplacian(gray, cv2.CV_64F).var() > 40

def verify_liveness(face):
    h, w, _ = face.shape
    if h < 20 or w < 20:
        return True
    
    gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
    
    # 1. Laplacian variance check (detects flat/blurry prints or high-frequency screen grids)
    variance = cv2.Laplacian(gray, cv2.CV_64F).var()
    
    # 2. Glare checking (highly reflective screens or glossy photo paper)
    _, thresh = cv2.threshold(gray, 245, 255, cv2.THRESH_BINARY)
    glare_pct = (cv2.countNonZero(thresh) / (h * w)) * 100
    
    # Flag low variance (blur prints), extreme variance (moiré/grid from screens), or high glare
    # Upper bound raised to 5000: real webcam faces under good light can exceed 1000 (sharp edges,
    # textured clothing in background), but screen moiré patterns typically exceed 5000.
    if variance < 20.0 or variance > 5000.0 or glare_pct > 20.0:
        return False
        
    return True
