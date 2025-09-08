import cv2
import pytesseract
import re
import os
from ultralytics import YOLO
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv

load_dotenv()
HF_API = os.getenv("HF_API_TOKEN")

pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"


class CertificateParser:
    def __init__(self, yolo_model_path, signature_output_folder):
        self.yolo_model_path = yolo_model_path
        self.signature_output_folder = signature_output_folder

        # Setup LLM
        llm = HuggingFaceEndpoint(
            model="meta-llama/Llama-3.3-70B-Instruct",  # or "google/gemma-2-2b-it"
            huggingfacehub_api_token=HF_API,
            task="text-generation",
            temperature=0
        )
        self.model = ChatHuggingFace(llm=llm)
        self.parser = JsonOutputParser()

        self.prompt = PromptTemplate(
            template="""
You are an AI assistant specialized in extracting information from student certificates.
Extract the following fields from the certificate text.
If a field is missing, set its value to null (the JSON null literal, not the string "null").

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
            partial_variables={"format_instructions": self.parser.get_format_instructions()}
        )

        self.chain = self.prompt | self.model | self.parser

    # ---------------- OCR ---------------- #
    def extract_text_from_image(self, image_path, threshold_value=150):
        img = cv2.imread(image_path)
        if img is None:
            raise FileNotFoundError(f"Could not read the image at: {image_path}")

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)

        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(thresh, config=custom_config)

        return text.strip()

    def clean_ocr_text(self, text):
        return re.sub(r"[^a-zA-Z0-9.,;:!?()@%&\-\s]", "", text)

    def extract_certificate_info(self, image_path):
        extracted_text = self.extract_text_from_image(image_path)
        cleaned_text = self.clean_ocr_text(extracted_text)
        result = self.chain.invoke({'certificate_text': cleaned_text})
        return result

    # ---------------- Signature Extraction ---------------- #
    def crop_signatures(self, image_path, student_name):
        os.makedirs(self.signature_output_folder, exist_ok=True)
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"Could not read the image at: {image_path}")

        model = YOLO(self.yolo_model_path)
        results = model(image)
        cropped_paths = []

        student_name = student_name if student_name else "unknown"
        student_name = student_name.replace(" ", "_").strip().lower()

        for result in results:
            boxes = result.boxes.xyxy.cpu().numpy()
            class_ids = result.boxes.cls.cpu().numpy()

            for idx, (bbox, cls_id) in enumerate(zip(boxes, class_ids)):
                if int(cls_id) == 0:  # signature class
                    x1, y1, x2, y2 = map(int, bbox)
                    cropped = image[y1:y2, x1:x2]
                    cropped_name = f"{student_name}_signature_{idx}.png"
                    cropped_path = os.path.join(self.signature_output_folder, cropped_name)
                    cv2.imwrite(cropped_path, cropped)
                    cropped_paths.append(cropped_path)

        return [p.replace("\\", "/") for p in cropped_paths] if cropped_paths else []

    # ---------------- Combined ---------------- #
    def parse_certificate(self, image_path):
        ocr_result = self.extract_certificate_info(image_path)
        sig_paths = self.crop_signatures(image_path, ocr_result["student_name"])

        return {
            "certificate_info": ocr_result,
            "signature_folder": self.signature_output_folder if sig_paths else None,
            "signature_paths": sig_paths
        }
