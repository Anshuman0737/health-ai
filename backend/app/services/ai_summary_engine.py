def generate_clinical_summary(biomarkers):

    if not biomarkers:
        return "No clinically relevant biomarkers detected in report."

    summary_parts = []

    # Cardiovascular Risk
    cardio_flags = []

    if biomarkers.get("total_cholesterol", 0) >= 200:
        cardio_flags.append("elevated total cholesterol")

    if biomarkers.get("ldl", 0) >= 130:
        cardio_flags.append("high LDL cholesterol")

    if biomarkers.get("triglycerides", 0) >= 150:
        cardio_flags.append("elevated triglycerides")

    if biomarkers.get("hdl", 100) < 40:
        cardio_flags.append("low HDL cholesterol")

    if biomarkers.get("hs_crp", 0) > 3:
        cardio_flags.append("high inflammatory marker (hs-CRP)")

    if cardio_flags:
        summary_parts.append(
            "Cardiovascular risk indicators detected: " + ", ".join(cardio_flags) + "."
        )

    # Metabolic Risk
    if biomarkers.get("hba1c", 0) >= 5.7:
        summary_parts.append("HbA1c suggests prediabetic metabolic state.")

    if biomarkers.get("fasting_glucose", 0) >= 100:
        summary_parts.append("Elevated fasting glucose detected.")

    # Liver Function
    liver_flags = []

    if biomarkers.get("ast", 0) > 40:
        liver_flags.append("elevated AST")

    if biomarkers.get("alt", 0) > 40:
        liver_flags.append("elevated ALT")

    if liver_flags:
        summary_parts.append(
            "Liver stress markers present: " + ", ".join(liver_flags) + "."
        )

    # Vitamin D
    if biomarkers.get("vitamin_d", 100) < 20:
        summary_parts.append("Vitamin D deficiency detected.")

    if not summary_parts:
        return "No major clinical risk indicators detected. Continue preventive monitoring."

    return " ".join(summary_parts)
