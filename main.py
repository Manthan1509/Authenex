import cv2
import pytesseract
import re
from dateutil.parser import parse as parse_date

# Update path below if Tesseract is installed elsewhere
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_image(image_path: str) -> str:
    """Extract text from certificate image using Tesseract OCR."""
    img = cv2.imread(image_path)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    text = pytesseract.image_to_string(thresh)
    return text


def parse_certificate_to_key_value(ocr_text: str) -> dict:
    """Parse OCR text into structured key-value pairs with robust rules."""

    lines = [line.strip() for line in ocr_text.splitlines() if line.strip()]
    normalized_lines = [re.sub(r'\s+', ' ', line) for line in lines]
    lower_lines = [line.lower() for line in normalized_lines]

    data = {
        'university_name': None,
        'student_name': None,
        'degree_name': None,
        'major': None,
        'date_of_issue': None,
        'registration_no': None
    }

    for line in normalized_lines[:5]:  
        if re.search(r'university|institute|college', line, re.IGNORECASE):
            data['university_name'] = line
            break

    name_keywords = ("certifies that", "awarded to", "student name", "conferred upon", "presented to")
    for i, l in enumerate(lower_lines):
        if any(k in l for k in name_keywords):
            candidates = []
            if i < len(normalized_lines):
                candidates.append(normalized_lines[i])
            if i + 1 < len(normalized_lines):
                candidates.append(normalized_lines[i + 1])

            for cand in candidates:
                if re.match(r'^[A-Z\s\.]+$', cand) or re.match(r'^([A-Z][a-z]+(?:\s[A-Z][a-z\.]+)+)$', cand):
                    data['student_name'] = cand.title()
                    break
            if data['student_name']:
                break

    degree_match = re.search(r'(Bachelor|Master|Doctor)\s+of\s+[A-Za-z\s]+', ocr_text, re.IGNORECASE)
    if degree_match:
        data['degree_name'] = degree_match.group(0).title()

    major_match = re.search(r'(in|major in|specialization in|field of)\s+([A-Za-z\s,]+)', ocr_text, re.IGNORECASE)
    if major_match:
        data['major'] = major_match.group(2).title()

    reg_match = re.search(r'(Reg(istration)?\.?\s*No\.?|Roll\s*No\.?|Student\s*ID|Enroll(ment)?\.?\s*No\.?)\s*[:\-]?\s*([A-Z0-9\-\/]+)',
                          ocr_text, re.IGNORECASE)
    if reg_match:
        data['registration_no'] = reg_match.group(5).strip()

    date_patterns = [
        r'(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})',          # 12/09/2022 or 12-09-22
        r'(\d{1,2}\s+[A-Za-z]+\s+\d{2,4})',              # 12 September 2022
        r'([A-Za-z]+\s+\d{1,2},\s*\d{4})'                # September 12, 2022
    ]
    for pattern in date_patterns:
        match = re.search(pattern, ocr_text)
        if match:
            try:
                parsed_date = parse_date(match.group(1), fuzzy=True, dayfirst=True)
                data['date_of_issue'] = parsed_date.strftime('%d %B %Y')
                break
            except Exception:
                continue

    return data


from fastapi import FastAPI, File, UploadFile
import uvicorn

app = FastAPI()

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    content = await file.read()
    # Process with model here
    return {"status": "verified", "confidence": 0.93}

if __name__ == "_main_":
    uvicorn.run(app, host="0.0.0.0", port=5000)
    
# if __name__ == "__main__":
#     image_path = "image copy.png"  
#     ocr_text = extract_text_from_image(image_path)
#     print("\n--- OCR Extracted Text ---\n")
#     print(ocr_text)

#     parsed_data = parse_certificate_to_key_value(ocr_text)
#     print("\n--- Extracted Key-Value Pairs ---\n")
#     for k, v in parsed_data.items():
#         print(f"{k}: {v}")


