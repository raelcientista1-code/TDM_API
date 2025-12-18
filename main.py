from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from tdm import tdm

app = FastAPI(title="tdm API")
tdm_engine = tdm()

class Numbers(BaseModel):
    numbers: List[int]

@app.get("/")
def root():
    return {"status": "tdm API rodando"}

@app.post("/audit")
def audit_numbers(payload: Numbers):
    report = tdm_engine.audit(payload.numbers)
    return report
