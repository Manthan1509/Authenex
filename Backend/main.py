from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from Backend.src.photo_verifier import verify_photos
from Backend.src.sign_verifier import SignatureVerifier
from Backend.src.signature_extractor import crop_signatures
from Backend.src.ocr import extract_certificate_info
import tempfile
import shutil
import os

app = FastAPI(title="Photo Verification API")

verifier = SignatureVerifier(model_path="Backend/models/signature_verification_model.keras")
YOLO_MODEL_PATH = "/Backend/models/best.pt"
SIGNATURE_OUTPUT_FOLDER = "./Authenex/cropped_signatures"

@app.post("/verify-faces")
async def verify_faces(
    file1_path: str,
    file2_path: str,
    threshold: float = 0.9
):
    try:
        result = verify_photos(file1_path, file2_path, threshold=threshold)
        return result if result else {"error": "Verification failed"}
    except Exception as e:
        return {"error": str(e)}


@app.post("/verify-signatures")
async def verify_signatures(
    file1_path: str,
    file2_path: str,
    threshold: float = 0.5
):
    try:
        result = verifier.verify_signatures(file1_path, file2_path, threshold=threshold)
        return result if result else {"error": "Verification failed"}
    except Exception as e:
        return {"error": str(e)}
    

@app.post("/process-certificate/")
async def process_certificate(file: UploadFile = File(...)):
    try:
        # Create temp directory for uploaded file
        tmp_dir = tempfile.mkdtemp()
        file_path = os.path.join(tmp_dir, file.filename)

        # Save uploaded file
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        # Run OCR
        ocr_result = extract_certificate_info(file_path)

        # Extract signatures
        sig_paths = crop_signatures(file_path, YOLO_MODEL_PATH, SIGNATURE_OUTPUT_FOLDER)

        response = {
            "certificate_info": ocr_result,
            "signature_folder": SIGNATURE_OUTPUT_FOLDER,
            "signature_paths": sig_paths
        }

        return JSONResponse(content=response)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)






# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=5000)