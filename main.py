from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import math

app = FastAPI(title="TDM Audit Engine")

class AuditRequest(BaseModel):
    numbers: List[int]
    threshold: float = 1.0

def tdm_trace(n: int) -> float:
    return math.log(n)

def anomaly_score(trace: float) -> float:
    return abs(trace - 90) / 10

@app.post("/audit")
async def audit(req: AuditRequest):
    results = []
    for n in req.numbers:
        trace = tdm_trace(n)
        anomaly = anomaly_score(trace)
        results.append({
            "number": n,
            "trace": trace,
            "anomaly_score": anomaly
        })
    return {"results": results}

@app.get("/health")
async def health():
    return {"status": "ok"}
