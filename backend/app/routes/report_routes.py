from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.biomarker_extractor import extract_biomarkers_from_pdf
from app.services.risk_engine import calculate_risk_engine
from app.services.clinical_summary import generate_clinical_summary

router = APIRouter()


@router.post("/upload-report")
async def upload_report(file: UploadFile = File(...)):

    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")

    file_bytes = await file.read()

    biomarkers = extract_biomarkers_from_pdf(file_bytes)

    risk_result = calculate_risk_engine(biomarkers)

    clinical_summary = generate_clinical_summary(biomarkers)

    return {
        "filename": file.filename,
        "biomarkers": biomarkers,
        **risk_result,
        "clinical_summary": clinical_summary,
        "extraction_confidence": 0.8
    }
