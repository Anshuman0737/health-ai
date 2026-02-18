def generate_recommendations(biomarkers, risk_level):

    if risk_level == "Critical Risk":
        return [
            "Urgent physician consultation required.",
            "Comprehensive cardiovascular evaluation advised.",
            "Immediate liver function assessment recommended.",
            "Strict metabolic risk management required."
        ]

    if risk_level == "High Risk":
        return [
            "Schedule physician consultation soon.",
            "Adopt structured diet and exercise program.",
            "Monitor lipid and glucose levels quarterly."
        ]

    if risk_level == "Moderate Risk":
        return [
            "Lifestyle modification recommended.",
            "Increase cardiovascular exercise.",
            "Annual metabolic screening advised."
        ]

    return [
        "Maintain healthy lifestyle.",
        "Annual health screening advised."
    ]
