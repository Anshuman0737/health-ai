def generate_intervention_plan(biomarkers, risk_vector):

    plan = []

    if risk_vector.get("liver_index", 0) > 0.6:
        plan.append({
            "domain": "Liver",
            "actions": [
                "Eliminate alcohol intake",
                "Reduce refined carbohydrates",
                "Increase omega-3 intake",
                "Repeat liver panel in 6-8 weeks"
            ]
        })

    if risk_vector.get("cardio_index", 0) > 0.5:
        plan.append({
            "domain": "Cardiovascular",
            "actions": [
                "Reduce saturated fat",
                "Increase fiber intake",
                "150 minutes/week exercise",
                "Repeat lipid panel in 3 months"
            ]
        })

    return plan
