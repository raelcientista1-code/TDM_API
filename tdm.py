from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from tdm import TDM  # Certifique-se de que tdm.py está no mesmo diretório

app = FastAPI(title="TDM API")

tdm_engine = TDM()

# Modelo para receber números no endpoint /audit
class NumbersRequest(BaseModel):
    numbers: List[int]

@app.get("/")
def root():
    return {"status": "TDM API rodando"}

@app.post("/audit")
def audit_numbers(request: NumbersRequest):
    report = tdm_engine.audit(request.numbers)
    return report

@app.post("/generate_laudo")
def generate_laudo(request: NumbersRequest):
    report = tdm_engine.audit(request.numbers)
    tdm_engine.generate_laudo(report)
    return {"message": "Laudo gerado com sucesso", "numbers_processed": len(request.numbers)}
