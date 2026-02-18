def generate_clinical_summary(biomarkers: dict):

    summary = []

    if biomarkers.get("ldl") and biomarkers["ldl"] > 130:
        summary.append("Elevated LDL increasing cardiovascular risk.")

    if biomarkers.get("triglycerides") and biomarkers["triglycerides"] > 200:
        summary.append("High triglycerides suggesting metabolic dysfunction.")

    if biomarkers.get("ast") and biomarkers["ast"] > 40:
        summary.append("Elevated AST indicating hepatic stress.")

    if biomarkers.get("alt") and biomarkers["alt"] > 45:
        summary.append("Elevated ALT indicating liver inflammation.")

    if biomarkers.get("vitamin_d") and biomarkers["vitamin_d"] < 30:
        summary.append("Vitamin D insufficiency detected.")

    if not summary:
        summary.append("No major abnormalities detected.")

    return " ".join(summary)
