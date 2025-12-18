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
    traces = [tdm.compute(n) for n in req.numbers]

    mean = statistics.mean(traces)
    stdev = statistics.pstdev(traces) + 1e-12

    results = []
    for n, t in zip(req.numbers, traces):
        score = abs(t - mean) / stdev
        classification = tdm.classify(score)

        results.append({
            "number": n,
            "trace": t,
            "anomaly_score": score,
            "classification": classification
        })

    return {"results": results}





@app.get("/health")
async def health():
    return {"status": "ok"}
