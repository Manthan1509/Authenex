from fastapi import FastAPI, UploadFile, File
from Backend.src.photo_verifier import verify_photos
from Backend.src.sign_verifier import SignatureVerifier
import tempfile
import shutil
import os

app = FastAPI(title="Photo Verification API")

verifier = SignatureVerifier(model_path="Backend/models/signature_verification_model.keras")

@app.post("/verify-faces")
async def verify_faces(
    file1: UploadFile = File(...),
    file2: UploadFile = File(...),
    threshold: float = 0.9
):
    try:
        tmp_dir = tempfile.mkdtemp()
        file1_path = os.path.join(tmp_dir, file1.filename)
        file2_path = os.path.join(tmp_dir, file2.filename)

        with open(file1_path, "wb") as f:
            shutil.copyfileobj(file1.file, f)
        with open(file2_path, "wb") as f:
            shutil.copyfileobj(file2.file, f)

        result = verify_photos(file1_path, file2_path, threshold=threshold)

        return result if result else {"error": "Verification failed"}


    except Exception as e:
        return {"error": str(e)}


@app.post("/verify-signatures")
async def verify_signatures(
    file1: UploadFile = File(...),
    file2: UploadFile = File(...),
    threshold: float = 0.5
):
    try:
        tmp_dir = tempfile.mkdtemp()
        file1_path = os.path.join(tmp_dir, file1.filename)
        file2_path = os.path.join(tmp_dir, file2.filename)

        with open(file1_path, "wb") as f:
            shutil.copyfileobj(file1.file, f)
        with open(file2_path, "wb") as f:
            shutil.copyfileobj(file2.file, f)

        result = verifier.verify_signatures(file1_path, file2_path, threshold=threshold)

        return result if result else {"error": "Verification failed"}

    except Exception as e:
        return {"error": str(e)}