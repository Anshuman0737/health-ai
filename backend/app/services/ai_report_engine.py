import os
from groq import Groq

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.3-70b-versatile"

client = Groq(api_key=GROQ_API_KEY)


def generate_ai_clinical_report(biomarkers, risk_result):

    prompt = f"""
You are a preventive medicine intelligence specialist.

Strict rules:
- Do NOT diagnose disease.
- Do NOT claim certainty.
- Emphasize risk gradients and physiological stress.
- Reference specific biomarker values.
- If key biomarkers are missing, explicitly mention reduced certainty.
- Highlight severe deviations (e.g., ALT > 250).

Biomarkers:
{biomarkers}

Deterministic Risk Engine Output:
{risk_result}

Respond in structured sections:

=== EXECUTIVE SUMMARY ===
4–6 sentence overview of risk profile.

=== DOMINANT RISK DOMAINS ===
Explain elevations using actual values.

=== MECHANISTIC INTERPRETATION ===
Describe physiological stress patterns.

=== TARGETED PREVENTIVE STRATEGY ===
Domain-specific interventions.

=== FOLLOW-UP INTELLIGENCE PLAN ===
Reassessment timeline adjusted to risk severity and data completeness.
"""

    try:
        completion = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=1200
        )
        return completion.choices[0].message.content.strip()
    except Exception:
        return "AI generation unavailable. Deterministic engine active."
