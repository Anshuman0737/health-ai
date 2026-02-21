from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Optional
from app.services.biomarker_extractor import extract_biomarkers_from_pdf
from app.services.risk_engine import calculate_risk_engine
from app.services.clinical_summary import generate_clinical_summary
from app.services.intervention_engine import generate_intervention_plan
from app.services.ai_report_engine import generate_ai_clinical_report

router = APIRouter()


@router.post("/upload-report")
async def upload_report(
    file: UploadFile = File(...),
    age: Optional[int] = None,
    gender: Optional[str] = None,
    bmi: Optional[float] = None,
    systolic_bp: Optional[float] = None,
    smoking: Optional[bool] = None,
    sleep_hours: Optional[float] = None,
    stress_level: Optional[int] = None,
    exercise_days: Optional[int] = None,
    alcohol_frequency: Optional[int] = None
):

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF supported")

    file_bytes = await file.read()

    biomarkers = extract_biomarkers_from_pdf(file_bytes)

    demographics = {
        "age": age,
        "gender": gender,
        "bmi": bmi,
        "systolic_bp": systolic_bp,
        "smoking": smoking
    }

    behavioral = {
        "sleep_hours": sleep_hours,
        "stress_level": stress_level,
        "exercise_days": exercise_days,
        "alcohol_frequency": alcohol_frequency
    }

    risk_result = calculate_risk_engine(biomarkers, demographics, behavioral)

    intervention_plan = generate_intervention_plan(
        biomarkers,
        risk_result["risk_vector"]
    )

    clinical_summary = generate_clinical_summary(biomarkers)

    ai_report = generate_ai_clinical_report(
        biomarkers,
        risk_result
    )

    return {
        "filename": file.filename,
        "biomarkers": biomarkers,
        **risk_result,
        "intervention_plan": intervention_plan,
        "clinical_summary": clinical_summary,
        "ai_clinical_report": ai_report,
        "extraction_confidence": 0.9
    }


@router.post("/simulate-risk")
async def simulate_risk(
    ldl: Optional[float] = None,
    triglycerides: Optional[float] = None,
    hdl: Optional[float] = None,
    alt: Optional[float] = None,
    sleep_hours: Optional[float] = None,
    stress_level: Optional[int] = None
):

    biomarkers = {
        "ldl": ldl,
        "triglycerides": triglycerides,
        "hdl": hdl,
        "alt": alt
    }

    demographics = {}
    behavioral = {
        "sleep_hours": sleep_hours,
        "stress_level": stress_level
    }

    result = calculate_risk_engine(biomarkers, demographics, behavioral)

    return result
