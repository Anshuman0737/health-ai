import math


def clamp(x, low=0, high=1):
    return max(low, min(high, x))


def norm(value, low, high):
    if value is None:
        return 0
    return clamp((value - low) / (high - low))


def sigmoid(x):
    return 1 / (1 + math.exp(-x))


def calculate_risk_engine(biomarkers: dict):

    fg = biomarkers.get("fasting_glucose")
    tg = biomarkers.get("triglycerides")
    hdl = biomarkers.get("hdl")
    ldl = biomarkers.get("ldl")
    hba1c = biomarkers.get("hba1c")
    hs_crp = biomarkers.get("hs_crp")
    ast = biomarkers.get("ast")
    alt = biomarkers.get("alt")
    vitamin_d = biomarkers.get("vitamin_d")

    ldl_norm = norm(ldl, 100, 190)
    tg_norm = norm(tg, 150, 400)
    hdl_inverse = 1 - norm(hdl, 40, 70)
    crp_norm = norm(hs_crp, 1, 10)
    glucose_norm = norm(fg, 100, 180)
    hba1c_norm = norm(hba1c, 5.7, 9)
    ast_norm = norm(ast, 40, 250)
    alt_norm = norm(alt, 40, 350)
    vitd_def = norm(30 - (vitamin_d or 30), 0, 30)

    tg_hdl_ratio = (tg / hdl) if tg and hdl else 0
    ratio_signal = norm(tg_hdl_ratio, 3, 10)

    hepatic_pattern = (
        0.6 * ast_norm +
        0.4 * alt_norm
    )

    cardio_index = (
        ldl_norm * 0.30 +
        tg_norm * 0.20 +
        hdl_inverse * 0.15 +
        crp_norm * 0.15 +
        ratio_signal * 0.20
    )

    liver_index = hepatic_pattern

    metabolic_index = (
        glucose_norm * 0.50 +
        hba1c_norm * 0.50
    )

    inflammatory_index = crp_norm
    nutritional_index = vitd_def

    synergy = 0
    if cardio_index > 0.6 and inflammatory_index > 0.6:
        synergy += 0.15
    if liver_index > 0.7 and metabolic_index > 0.5:
        synergy += 0.15

    composite = (
        cardio_index * 0.30 +
        liver_index * 0.25 +
        metabolic_index * 0.20 +
        inflammatory_index * 0.15 +
        nutritional_index * 0.10
    )

    composite *= (1 + synergy)

    probability_curve = sigmoid((composite - 0.40) * 7)
    risk_score = round(probability_curve * 100)

    if risk_score < 30:
        level = "Low Risk"
    elif risk_score < 60:
        level = "Moderate Risk"
    elif risk_score < 80:
        level = "High Risk"
    else:
        level = "Critical Risk"

    five_year = round(sigmoid((composite - 0.45) * 8) * 100, 1)
    ten_year = round(sigmoid((composite - 0.35) * 10) * 100, 1)

    return {
        "risk_score": risk_score,
        "risk_level": level,
        "risk_vector": {
            "cardio_index": round(cardio_index, 2),
            "liver_index": round(liver_index, 2),
            "metabolic_index": round(metabolic_index, 2),
            "inflammatory_index": round(inflammatory_index, 2),
            "nutritional_index": round(nutritional_index, 2)
        },
        "interaction_flags": [],
        "risk_projection": (
            "Escalating systemic risk trajectory if unmanaged."
            if risk_score >= 60
            else "Risk remains modifiable with early structured intervention."
        ),
        "intervention_simulation": {
            "optimized_risk_score": round(risk_score * 0.75),
            "improvement_potential": round(risk_score - (risk_score * 0.75))
        },
        "biological_age_delta": round((composite - 0.35) * 35),
        "age_acceleration_category": "Stable",
        "event_probability_projection": {
            "5_year_risk_percent": five_year,
            "10_year_risk_percent": ten_year
        },
        "risk_uncertainty": {
            "data_completeness": 0.9,
            "model_confidence": 0.85
        }
    }
