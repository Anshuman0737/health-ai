def generate_clinical_summary(biomarkers):

    findings = []

    if biomarkers.get("ldl") and biomarkers["ldl"] > 130:
        findings.append("Elevated LDL increasing cardiovascular risk.")

    if biomarkers.get("triglycerides") and biomarkers["triglycerides"] > 200:
        findings.append("High triglycerides suggesting metabolic dysfunction.")

    if biomarkers.get("alt") and biomarkers["alt"] > 250:
        findings.append("Marked ALT elevation indicating significant hepatic stress.")

    if biomarkers.get("vitamin_d") and biomarkers["vitamin_d"] < 30:
        findings.append("Vitamin D insufficiency detected.")

    return " ".join(findings) if findings else "No major abnormalities detected."
