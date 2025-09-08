from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from Backend.src.photo_verifier import verify_photos
from Backend.src.sign_verifier import SignatureVerifier
from Backend.src.certificate_parser import CertificateParser
from pathlib import Path
import tempfile
import shutil
import os
from dotenv import load_dotenv

load_dotenv()
HF_API = os.getenv("HF_API_TOKEN")


app = FastAPI(title="Photo Verification API")


BASE_DIR = Path(__file__).resolve().parents[1]
SIGNATURE_OUTPUT_FOLDER = BASE_DIR / "cropped_signature"
SIGNATURE_OUTPUT_FOLDER = SIGNATURE_OUTPUT_FOLDER.as_posix()
SIGN_PARSER_MODEL_PATH = "/Backend/models/sign_parser.pt"
SIGN_VERIFIER_MODEL_PATH = "/Backend/models/sign_verifier.keras"

verifier = SignatureVerifier(model_path=SIGN_VERIFIER_MODEL_PATH)
parser = CertificateParser(SIGN_PARSER_MODEL_PATH, str(SIGNATURE_OUTPUT_FOLDER))


@app.post("/verify-faces")
async def verify_faces(
    file1_path: str,
    file2_path: str,
    threshold: float = 0.9
):
    try:
        result = verify_photos(file1_path, file2_path, threshold=threshold)
        if result:
            return JSONResponse(content=result, status_code=200)
        return JSONResponse(content={"error": "Verification failed"}, status_code=400)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/verify-signatures")
async def verify_signatures(
    file1_path: str,
    file2_path: str,
    threshold: float = 0.5
):
    try:
        result = verifier.verify_signatures(file1_path, file2_path, threshold=threshold)
        if result:
            return JSONResponse(content=result, status_code=200)
        return JSONResponse(content={"error": "Verification failed"}, status_code=400)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    

@app.post("/parse-certificate/")
async def parse_certificate(file: UploadFile = File(...)):
    try:
        tmp_dir = tempfile.mkdtemp()
        file_path = os.path.join(tmp_dir, file.filename)

        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        result = parser.parse_certificate(file_path)

        return JSONResponse(content=result, status_code=200)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)






# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=5000)