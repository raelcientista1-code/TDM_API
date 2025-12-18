from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from tdm_engine import tdm_trace, anomaly_score

app = FastAPI(title="TDM Audit Engine")

class AuditRequest(BaseModel):
    numbers: List[int]
    threshold: float = 1.0

@app.post("/audit")
async def audit(req: AuditRequest):
    results = []

    for n in req.numbers:
        trace = tdm_trace(n)
        anomaly = anomaly_score(trace)

        classification = (
            "COMPATIVEL_COM_CHAVE_REAL"
            if anomaly <= req.threshold
            else "ANOMALIA_DETECTADA"
        )

        results.append({
            "number": n,
            "trace": trace,
            "anomaly_score": anomaly,
            "classification": classification
        })

    return {
        "threshold": req.threshold,
        "results": results
    }
