import base64, cv2, numpy as np

def base64_to_image(data_url: str):
    encoded = data_url.split(",")[1]
    img_bytes = base64.b64decode(encoded)
    return cv2.imdecode(np.frombuffer(img_bytes, np.uint8), 1)
