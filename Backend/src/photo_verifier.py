import cv2
from keras_facenet import FaceNet
from numpy.linalg import norm


embedder = FaceNet()

def get_embedding(img_path):
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    detections = embedder.extract(img, threshold=0.95)

    if len(detections) == 0:
        raise ValueError(f"No face detected in {img_path}")

    embedding = detections[0]["embedding"]
    return embedding


def verify_photos(img1_path, img2_path, threshold=0.9):
    emb1 = get_embedding(img1_path)
    emb2 = get_embedding(img2_path)

    emb1 = emb1 / norm(emb1)
    emb2 = emb2 / norm(emb2)

    distance = norm(emb1 - emb2)
    prediction = distance < threshold

    confidence = abs(distance - threshold) / threshold
    confidence = min(1.0, confidence)

    return {
            "distance": round(float(distance), 2),
            "prediction": bool(prediction),
            'confidence': round(float(confidence), 2),
            "threshold": threshold
        }
