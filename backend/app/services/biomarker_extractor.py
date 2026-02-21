import re
from PyPDF2 import PdfReader
from io import BytesIO


def extract_biomarkers_from_pdf(file_bytes):

    reader = PdfReader(BytesIO(file_bytes))
    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    def find(pattern):
        match = re.search(pattern, text, re.IGNORECASE)
        return float(match.group(1)) if match else None

    return {
        "fasting_glucose": find(r"glucose.*?(\d+\.?\d*)"),
        "triglycerides": find(r"triglycerides.*?(\d+\.?\d*)"),
        "hdl": find(r"hdl.*?(\d+\.?\d*)"),
        "ldl": find(r"ldl.*?(\d+\.?\d*)"),
        "hba1c": find(r"hba1c.*?(\d+\.?\d*)"),
        "hs_crp": find(r"crp.*?(\d+\.?\d*)"),
        "ast": find(r"ast.*?(\d+\.?\d*)"),
        "alt": find(r"alt.*?(\d+\.?\d*)"),
        "vitamin_d": find(r"vitamin.*?d.*?(\d+\.?\d*)"),
    }
