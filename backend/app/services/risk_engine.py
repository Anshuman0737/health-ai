import math


def clamp(x, low=0, high=1):
    return max(low, min(high, x))


def norm(value, low, high):
    if value is None:
        return None
    return clamp((value - low) / (high - low))


def sigmoid(x):
    return 1 / (1 + math.exp(-x))


def behavioral_index(behavioral):
    if not behavioral:
        return 0.2

    sleep = behavioral.get("sleep_hours")
    stress = behavioral.get("stress_level")
    exercise = behavioral.get("exercise_days")
    alcohol = behavioral.get("alcohol_frequency")

    sleep_penalty = clamp((7 - sleep) / 4, 0, 1) if sleep is not None else 0.2
    stress_penalty = clamp((stress - 4) / 6, 0, 1) if stress is not None else 0.2
    inactivity_penalty = clamp((3 - exercise) / 3, 0, 1) if exercise is not None else 0.2
    alcohol_penalty = clamp(alcohol / 5, 0, 1) if alcohol is not None else 0.2

    return (
        sleep_penalty * 0.3 +
        stress_penalty * 0.3 +
        inactivity_penalty * 0.2 +
        alcohol_penalty * 0.2
    )


def safe_weighted_average(values, weights):
    total = 0
    weight_sum = 0
    for v, w in zip(values, weights):
        if v is not None:
            total += v * w
            weight_sum += w
    return total / weight_sum if weight_sum else 0.2


def calculate_risk_engine(biomarkers, demographics=None, behavioral=None):

    ldl = biomarkers.get("ldl")
    tg = biomarkers.get("triglycerides")
    hdl = biomarkers.get("hdl")
    alt = biomarkers.get("alt")
    ast = biomarkers.get("ast")
    crp = biomarkers.get("hs_crp")
    hba1c = biomarkers.get("hba1c")
    vitd = biomarkers.get("vitamin_d")

    ldl_norm = norm(ldl, 100, 190)
    tg_norm = norm(tg, 150, 400)
    hdl_inv = 1 - norm(hdl, 40, 70) if hdl is not None else None
    alt_norm = norm(alt, 40, 300)
    ast_norm = norm(ast, 40, 200)
    crp_norm = norm(crp, 1, 8)
    hba1c_norm = norm(hba1c, 5.7, 8.5)
    vitd_def = norm(30 - vitd, 0, 30) if vitd is not None else None

    cardio_index = safe_weighted_average(
        [ldl_norm, tg_norm, hdl_inv, crp_norm],
        [0.35, 0.25, 0.2, 0.2]
    )

    liver_index = safe_weighted_average(
        [alt_norm, ast_norm],
        [0.6, 0.4]
    )

    metabolic_index = hba1c_norm if hba1c_norm is not None else 0.2
    inflammatory_index = crp_norm if crp_norm is not None else 0.2
    nutritional_index = vitd_def if vitd_def is not None else 0.2
    behavior_index = behavioral_index(behavioral)

    synergy = 1.0

    if cardio_index > 0.5 and inflammatory_index > 0.5:
        synergy += 0.15

    if liver_index > 0.5 and behavior_index > 0.4:
        synergy += 0.12

    if metabolic_index > 0.4 and tg_norm is not None and tg_norm > 0.4:
        synergy += 0.1

    severity = 0
    if alt is not None and alt > 250:
        severity += 0.15
    if ldl is not None and ldl > 180:
        severity += 0.12
    if crp is not None and crp > 5:
        severity += 0.1

    composite = (
        cardio_index * 0.25 +
        liver_index * 0.22 +
        metabolic_index * 0.13 +
        inflammatory_index * 0.1 +
        nutritional_index * 0.1 +
        behavior_index * 0.2
    )

    composite = composite * synergy + severity

    values = [
        ldl_norm, tg_norm, hdl_inv,
        alt_norm, ast_norm,
        crp_norm, hba1c_norm,
        vitd_def
    ]

    missing_count = len([v for v in values if v is None])
    composite += missing_count * 0.02

    composite = clamp(composite)

    probability_curve = sigmoid((composite - 0.35) * 7)
    risk_score = round(probability_curve * 100)

    if risk_score < 30:
        level = "Low Risk"
    elif risk_score < 60:
        level = "Moderate Risk"
    elif risk_score < 80:
        level = "High Risk"
    else:
        level = "Critical Risk"

    five_year = round(clamp(risk_score * 0.8, 0, 99), 1)
    ten_year = round(clamp(risk_score * 1.25, 0, 99), 1)

    if risk_score > 65:
        trajectory = "Accelerating"
    elif risk_score > 45:
        trajectory = "Elevated but reversible"
    else:
        trajectory = "Stable"

    risk_vector = {
        "cardio_index": round(cardio_index, 2),
        "liver_index": round(liver_index, 2),
        "metabolic_index": round(metabolic_index, 2),
        "inflammatory_index": round(inflammatory_index, 2),
        "nutritional_index": round(nutritional_index, 2),
        "behavioral_index": round(behavior_index, 2)
    }

    priorities = sorted(
        risk_vector.items(),
        key=lambda x: x[1],
        reverse=True
    )[:2]

    priority_domains = [p[0] for p in priorities]

    total_fields = len(values)
    filled = total_fields - missing_count
    completeness = round(filled / total_fields, 2)
    confidence = round(0.5 + completeness * 0.45, 2)

    return {
        "model_type": "Temporal synergy-weighted preventive intelligence engine",
        "risk_score": risk_score,
        "risk_level": level,
        "risk_vector": risk_vector,
        "risk_priorities": priority_domains,
        "risk_trajectory": trajectory,
        "event_probability_projection": {
            "5_year_risk_percent": five_year,
            "10_year_risk_percent": ten_year
        },
        "risk_uncertainty": {
            "data_completeness": completeness,
            "model_confidence": confidence
        },
        "model_explainability": {
            "methodology": "Synergy-amplified severity-escalated multi-domain model with temporal projection",
            "calibration_status": "Heuristic interaction model (non-clinical)",
            "intended_use": "Preventive awareness support only"
        }
    }