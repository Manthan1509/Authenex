import cv2
import pytesseract
import re
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv

load_dotenv()

# Path to Tesseract OCR exe (Windows only)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_image(image_path, threshold_value=150):
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"⚠️ Could not read the image at: {image_path}")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)

    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(thresh, config=custom_config)

    return text.strip()

def clean_ocr_text(text):
    return re.sub(r"[^a-zA-Z0-9.,;:!?()@%&\-\s]", "", text)

# -----------------------------
# LLM Setup
# -----------------------------
llm = HuggingFaceEndpoint(
    model="google/gemma-2-2b-it",
    task="text-generation",
    temperature=0
)
model = ChatHuggingFace(llm=llm)
parser = JsonOutputParser()

prompt = PromptTemplate(
    template="""
You are an AI assistant specialized in extracting information from student certificates.
Extract the following fields from the certificate text. If a field is missing, set its value to null:

- Student Name
- Institute Name
- Degree
- Major/Specialization
- Date of Issue
- Certificate ID / Registration Number

Return the output in **strict JSON format**, like:

{{
  "student_name": "...",
  "institute_name": "...",
  "degree": "...",
  "major": "...",
  "date_of_issue": "...",
  "certificate_id": "..."
}}

Certificate Text:
{certificate_text}

output format:
{format_instructions}
""",
    input_variables=["certificate_text"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

chain = prompt | model | parser

def extract_certificate_info(image_path):
    extracted_text = extract_text_from_image(image_path)
    cleaned_text = clean_ocr_text(extracted_text)
    result = chain.invoke({'certificate_text': cleaned_text})
    return result

print(extract_certificate_info(r'C:\Users\pc\Desktop\test_images\Kanushi.jpg'))
