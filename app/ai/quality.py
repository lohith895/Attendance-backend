import cv2

def is_face_clear(face):
    gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
    return cv2.Laplacian(gray, cv2.CV_64F).var() > 40
