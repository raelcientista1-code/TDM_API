from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from TDM import TDM

app = FastAPI(title="TDM API")
tdm_engine = TDM()

class Numbers(BaseModel):
    numbers: List[int]

@app.get("/")
def root():
    return {"status": "TDM API rodando"}

@app.post("/audit")
def audit_numbers(payload: Numbers):
    report = tdm_engine.audit(payload.numbers)
    return report
