import re


def extract_biomarkers_from_pdf(file_bytes):

    text = file_bytes.decode(errors="ignore")

    def find(pattern):
        match = re.search(pattern, text, re.IGNORECASE)
        return float(match.group(1)) if match else None

    return {
        "fasting_glucose": find(r"glucose\s*[:\-]?\s*(\d+\.?\d*)"),
        "triglycerides": find(r"triglycerides\s*[:\-]?\s*(\d+\.?\d*)"),
        "hdl": find(r"hdl\s*[:\-]?\s*(\d+\.?\d*)"),
        "ldl": find(r"ldl\s*[:\-]?\s*(\d+\.?\d*)"),
        "hba1c": find(r"hba1c\s*[:\-]?\s*(\d+\.?\d*)"),
        "hs_crp": find(r"crp\s*[:\-]?\s*(\d+\.?\d*)"),
        "ast": find(r"ast\s*[:\-]?\s*(\d+\.?\d*)"),
        "alt": find(r"alt\s*[:\-]?\s*(\d+\.?\d*)"),
        "vitamin_d": find(r"vitamin\s*d\s*[:\-]?\s*(\d+\.?\d*)"),
    }
