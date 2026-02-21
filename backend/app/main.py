from fastapi import FastAPI, UploadFile, File, Query, HTTPException
import pdfplumber
import re
import numpy as np
import random
import math

app = FastAPI(title="Hybrid Preventive Intelligence System 2.0.0")

BASELINE = {}
HISTORY = []

def f(x):
    try:
        return float(x)
    except:
        return None

def extract(label, text):
    pattern = rf"{label}[^\n]*?\n?.*?([\d]+\.?[\d]*)"
    m = re.search(pattern, text, re.IGNORECASE)
    return f(m.group(1)) if m else None

def parse_pdf(file):
    text = ""
    with pdfplumber.open(file.file) as pdf:
        for p in pdf.pages:
            t = p.extract_text()
            if t:
                text += t + "\n"
    return {
        "fasting_glucose": extract("Glucose, Fasting", text),
        "hba1c": extract("HbA1c", text),
        "ldl": extract("LDL Cholesterol", text),
        "hdl": extract("HDL Cholesterol", text),
        "triglycerides": extract("Triglycerides", text),
        "ast": extract("AST \\(SGOT\\)", text),
        "alt": extract("ALT \\(SGPT\\)", text),
        "hs_crp": extract("High Sensitivity CRP", text),
        "vitamin_d": extract("Vitamin D, 25 Hydroxy", text),
        "esr": extract("E\\.S\\.R\\.", text),
    }

def norm(v, low, high):
    if v is None:
        return None
    if v <= low:
        return 0
    if v >= high:
        return 1
    return (v - low) / (high - low)

def liver(ast, alt):
    vals=[]
    if ast is not None: vals.append(norm(ast,40,200))
    if alt is not None: vals.append(norm(alt,40,300))
    return min(1,np.mean(vals)) if vals else None

def cardio(ldl,tg,hs):
    vals=[]
    if ldl is not None: vals.append(norm(ldl,100,190))
    if tg is not None: vals.append(norm(tg,150,300))
    if hs is not None: vals.append(norm(hs,1,10))
    return min(1,np.mean(vals)) if vals else None

def metabolic(a1c,glucose):
    vals=[]
    if a1c is not None: vals.append(norm(a1c,5.6,7))
    if glucose is not None: vals.append(norm(glucose,100,160))
    return min(1,np.mean(vals)) if vals else None

def inflammatory(hs,esr):
    vals=[]
    if hs is not None: vals.append(norm(hs,1,10))
    if esr is not None: vals.append(norm(esr,15,60))
    return min(1,np.mean(vals)) if vals else None

def nutritional(vd):
    if vd is None: return None
    return 0 if vd>=75 else min(1,(75-vd)/75)

def resilience(stress,sleep):
    if stress is None or sleep is None: return None
    stress_factor=norm(stress,2,10)
    sleep_factor=1-norm(sleep,6,9)
    return min(1,(stress_factor+sleep_factor)/2)

def compliance(resilience_index):
    if resilience_index is None: return 0.5
    return round(1 - resilience_index*0.6,2)

def override(b):
    if b.get("alt") and b["alt"]>200: return True
    if b.get("hs_crp") and b["hs_crp"]>3: return True
    if b.get("hba1c") and b["hba1c"]>=5.7: return True
    return False

def volatility_multiplier(indices):
    high_domains=sum(1 for v in indices.values() if v and v>0.6)
    return 0.1 + high_domains*0.05

def monte_carlo(score,vol,runs=600):
    sims=[]
    for _ in range(runs):
        sims.append(score*(1+random.uniform(-vol,vol)))
    return {
        "mean":round(np.mean(sims),1),
        "low":round(np.percentile(sims,10),1),
        "high":round(np.percentile(sims,90),1)
    }

def economic_impact(score):
    annual_cost=score*120
    ten_year=annual_cost*10
    preventable_portion=ten_year*0.35
    return {
        "estimated_annual_risk_cost_usd":round(annual_cost,0),
        "ten_year_projected_cost_usd":round(ten_year,0),
        "preventable_cost_opportunity_usd":round(preventable_portion,0)
    }

def intervention_roi(base,new):
    delta=new-base
    return {
        "absolute_risk_reduction":-delta if delta<0 else 0,
        "relative_percent_change":round((delta/base)*100,2) if base else 0,
        "impact_magnitude":"High" if abs(delta)>20 else "Moderate" if abs(delta)>10 else "Low"
    }

def compute(b,stress=None,sleep=None):
    l=liver(b.get("ast"),b.get("alt"))
    c=cardio(b.get("ldl"),b.get("triglycerides"),b.get("hs_crp"))
    m=metabolic(b.get("hba1c"),b.get("fasting_glucose"))
    i=inflammatory(b.get("hs_crp"),b.get("esr"))
    n=nutritional(b.get("vitamin_d"))
    r=resilience(stress,sleep)

    indices={
        "liver_index":l,
        "cardio_index":c,
        "metabolic_index":m,
        "inflammatory_index":i,
        "nutritional_index":n,
        "resilience_index":r
    }

    valid=[v for v in indices.values() if v is not None]
    if not valid: raise HTTPException(status_code=400,detail="Insufficient data")

    weighted=(0.25*(l or 0)+0.25*(c or 0)+0.2*(m or 0)+0.2*(i or 0)+0.05*(n or 0)+0.05*(r or 0))
    score=int(weighted*100)

    if override(b): score=max(score,60)

    if score<30: level="Low Risk"
    elif score<60: level="Moderate Risk"
    else: level="High Risk"

    vol=volatility_multiplier(indices)
    p5=monte_carlo(score,vol)
    p10=monte_carlo(score*1.15,vol*1.4)

    compliance_prob=compliance(r)
    econ=economic_impact(score)

    return score,level,{k:round(v or 0,2) for k,v in indices.items()},vol,p5,p10,compliance_prob,econ

@app.post("/upload-report")
async def upload_report(file:UploadFile=File(...)):
    biomarkers=parse_pdf(file)
    score,level,vector,vol,p5,p10,comp,econ=compute(biomarkers)
    BASELINE.clear()
    BASELINE.update(biomarkers)
    HISTORY.append(score)
    return {
        "biomarkers":biomarkers,
        "risk_score":score,
        "risk_level":level,
        "risk_vector":vector,
        "volatility_index":round(vol,2),
        "event_probability_projection":{"5_year":p5,"10_year":p10},
        "compliance_probability":comp,
        "economic_impact_model":econ,
        "executive_summary":f"Systemic risk classified as {level}. Projected 10-year envelope peaks at {p10['high']}. Estimated preventable economic burden ${econ['preventable_cost_opportunity_usd']}."
    }

@app.post("/simulate-risk")
async def simulate_risk(
    ldl:float|None=Query(None),
    triglycerides:float|None=Query(None),
    alt:float|None=Query(None),
    hs_crp:float|None=Query(None),
    vitamin_d:float|None=Query(None),
    stress_level:int|None=Query(None),
    sleep_hours:float|None=Query(None),
):
    if not BASELINE:
        raise HTTPException(status_code=400,detail="Upload baseline first")

    scenario=BASELINE.copy()
    if ldl is not None: scenario["ldl"]=ldl
    if triglycerides is not None: scenario["triglycerides"]=triglycerides
    if alt is not None: scenario["alt"]=alt
    if hs_crp is not None: scenario["hs_crp"]=hs_crp
    if vitamin_d is not None: scenario["vitamin_d"]=vitamin_d

    new_score,new_level,new_vector,vol,p5,p10,comp,econ=compute(scenario,stress_level,sleep_hours)
    base_score,_,_,_,_,_,_,_=compute(BASELINE)

    roi=intervention_roi(base_score,new_score)
    HISTORY.append(new_score)

    trajectory="Improving" if new_score<base_score else "Worsening" if new_score>base_score else "Stable"

    return {
        "baseline_risk_score":base_score,
        "simulated_risk_score":new_score,
        "risk_delta":roi,
        "risk_level":new_level,
        "risk_vector":new_vector,
        "volatility_index":round(vol,2),
        "trajectory_direction":trajectory,
        "event_probability_projection":{"5_year":p5,"10_year":p10},
        "compliance_probability":comp,
        "economic_impact_model":econ,
        "executive_summary":f"Scenario shifts risk from {base_score} to {new_score}. Direction: {trajectory}. Intervention classified as {roi['impact_magnitude']} impact."
    }