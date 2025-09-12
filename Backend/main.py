from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
import re
import mimetypes
try:
    from src.photo_verifier import verify_photos
    from src.sign_verifier import SignatureVerifier
    from src.certificate_parser import CertificateParser
except ImportError:
    from src.mock_services import mock_verify_photos as verify_photos
    from src.mock_services import MockSignatureVerifier as SignatureVerifier
    from src.mock_services import MockCertificateParser as CertificateParser
    print("Using mock services - AI models not available")

from src.certificate_verification_service import CertificateVerificationService
from pathlib import Path
import tempfile
import shutil
import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

app = FastAPI(title="Certificate Verification API with Blockchain")

# Security configuration
security = HTTPBearer()

# File validation constants
ALLOWED_FILE_TYPES = {'.pdf', '.jpg', '.jpeg', '.png'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # Restrict to needed methods
    allow_headers=["*"],
)

def validate_file(file: UploadFile) -> bool:
    """Validate uploaded file type and size"""
    if not file.filename:
        return False
    
    # Check file extension
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ALLOWED_FILE_TYPES:
        return False
    
    # Check MIME type
    mime_type, _ = mimetypes.guess_type(file.filename)
    if mime_type and not mime_type.startswith(('image/', 'application/pdf')):
        return False
    
    return True

def sanitize_filename(filename: str) -> str:
    """Sanitize filename to prevent path traversal"""
    # Remove path separators and dangerous characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    filename = os.path.basename(filename)
    return filename[:255]  # Limit length

# Initialize services
cert_verification_service = CertificateVerificationService()

# Legacy model initialization for backward compatibility
BASE_DIR = Path(__file__).resolve().parents[1]
SIGNATURE_OUTPUT_FOLDER = BASE_DIR / "cropped_signature"
<<<<<<< HEAD
PHOTO_OUTPUT_FOLDER = BASE_DIR / "cropped_photo"

SIGNATURE_OUTPUT_FOLDER = SIGNATURE_OUTPUT_FOLDER.as_posix()
SIGN_PARSER_MODEL_PATH = BASE_DIR / "/Backend/models/sign_parser.pt"
SIGN_VERIFIER_MODEL_PATH = BASE_DIR / "Backend/models/sign_verifier.keras"

verifier = SignatureVerifier(model_path=SIGN_VERIFIER_MODEL_PATH)
parser = CertificateParser(str(SIGNATURE_OUTPUT_FOLDER), str(PHOTO_OUTPUT_FOLDER))
=======
SIGN_PARSER_MODEL_PATH = os.getenv('SIGN_PARSER_MODEL_PATH', str(BASE_DIR / "models" / "sign_parser.pt"))
SIGN_VERIFIER_MODEL_PATH = os.getenv('SIGN_VERIFIER_MODEL_PATH', str(BASE_DIR / "models" / "sign_verifier.keras"))

try:
    verifier = SignatureVerifier(model_path=SIGN_VERIFIER_MODEL_PATH)
    parser = CertificateParser(SIGN_PARSER_MODEL_PATH, str(SIGNATURE_OUTPUT_FOLDER))
except Exception as e:
    print(f"Warning: Legacy models not loaded: {e}")
    verifier = None
    parser = None
>>>>>>> 755948e (Normalize line endings)


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
    # Use the certificate parser from the service (includes mock fallback)
    if not cert_verification_service.certificate_parser:
        raise HTTPException(status_code=503, detail="Certificate parser not available")
    
    # Validate file
    if not validate_file(file):
        raise HTTPException(status_code=400, detail="Invalid file type or size")
    
    try:
        tmp_dir = tempfile.mkdtemp()
        safe_filename = sanitize_filename(file.filename)
        file_path = os.path.join(tmp_dir, safe_filename)

        # Check file size
        file_content = await file.read()
        if len(file_content) > MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail="File too large")
        
        with open(file_path, "wb") as f:
            f.write(file_content)

        result = cert_verification_service.certificate_parser.parse_certificate(file_path)
        return JSONResponse(content=result, status_code=200)

    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(content={"error": "Processing failed"}, status_code=500)
    finally:
        # Cleanup
        if 'tmp_dir' in locals():
            shutil.rmtree(tmp_dir, ignore_errors=True)


# Blockchain Certificate Endpoints
@app.post("/certificate/store-blockchain")
async def store_certificate_blockchain(
    file: UploadFile = File(...),
    account_address: str = Form(...)
):
    """Parse certificate and store on blockchain"""
    # Validate file
    if not validate_file(file):
        raise HTTPException(status_code=400, detail="Invalid file type or size")
    
    # Validate account address format (basic Ethereum address validation)
    if account_address and not re.match(r'^0x[a-fA-F0-9]{40}$', account_address):
        # For mock mode, use a default address if invalid
        account_address = '0x1234567890123456789012345678901234567890'
    
    try:
        tmp_dir = tempfile.mkdtemp()
        safe_filename = sanitize_filename(file.filename)
        file_path = os.path.join(tmp_dir, safe_filename)

        # Check file size
        file_content = await file.read()
        if len(file_content) > MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail="File too large")
        
        with open(file_path, "wb") as f:
            f.write(file_content)

        result = cert_verification_service.parse_and_store_certificate(
            file_path, account_address
        )
        
        return JSONResponse(content=result, status_code=200)

    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(content={"error": "Processing failed"}, status_code=500)
    finally:
        if 'tmp_dir' in locals():
            shutil.rmtree(tmp_dir, ignore_errors=True)


@app.get("/certificate/blockchain/{certificate_hash}")
async def get_certificate_blockchain(certificate_hash: str):
    """Get certificate info from blockchain"""
    # Validate hash format (basic hex validation)
    if not re.match(r'^[a-fA-F0-9]{64}$', certificate_hash):
        raise HTTPException(status_code=400, detail="Invalid certificate hash format")
    
    try:
        result = cert_verification_service.blockchain.get_certificate_info(certificate_hash)
        return JSONResponse(content=result, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": "Certificate not found"}, status_code=404)


@app.post("/certificate/verify-comprehensive")
async def verify_certificate_comprehensive(
    certificate_hash: str = Form(...),
    account_address: Optional[str] = Form(None),
    photo1: Optional[UploadFile] = File(None),
    photo2: Optional[UploadFile] = File(None),
    signature1: Optional[UploadFile] = File(None),
    signature2: Optional[UploadFile] = File(None)
):
    """Comprehensive certificate verification using blockchain + AI"""
    tmp_files = []
    
    try:
        tmp_dir = tempfile.mkdtemp()
        
        # Save uploaded files
        photo1_path = photo2_path = signature1_path = signature2_path = None
        
        if photo1:
            photo1_path = os.path.join(tmp_dir, f"photo1_{photo1.filename}")
            with open(photo1_path, "wb") as f:
                shutil.copyfileobj(photo1.file, f)
            tmp_files.append(photo1_path)
        
        if photo2:
            photo2_path = os.path.join(tmp_dir, f"photo2_{photo2.filename}")
            with open(photo2_path, "wb") as f:
                shutil.copyfileobj(photo2.file, f)
            tmp_files.append(photo2_path)
        
        if signature1:
            signature1_path = os.path.join(tmp_dir, f"sig1_{signature1.filename}")
            with open(signature1_path, "wb") as f:
                shutil.copyfileobj(signature1.file, f)
            tmp_files.append(signature1_path)
        
        if signature2:
            signature2_path = os.path.join(tmp_dir, f"sig2_{signature2.filename}")
            with open(signature2_path, "wb") as f:
                shutil.copyfileobj(signature2.file, f)
            tmp_files.append(signature2_path)
        
        # Perform comprehensive verification
        result = cert_verification_service.verify_certificate_comprehensive(
            certificate_hash=certificate_hash,
            photo1_path=photo1_path,
            photo2_path=photo2_path,
            signature1_path=signature1_path,
            signature2_path=signature2_path,
            account_address=account_address
        )
        
        return JSONResponse(content=result, status_code=200)
        
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    finally:
        # Cleanup temporary files
        if 'tmp_dir' in locals():
            shutil.rmtree(tmp_dir, ignore_errors=True)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    # Show as connected if either real blockchain or mock mode
    blockchain_status = (cert_verification_service.blockchain.contract is not None or 
                        getattr(cert_verification_service.blockchain, 'mock_mode', False))
    
    return {
        "status": "healthy",
        "blockchain_connected": blockchain_status,
        "ai_models_loaded": {
            "certificate_parser": cert_verification_service.certificate_parser is not None,
            "signature_verifier": cert_verification_service.signature_verifier is not None
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)