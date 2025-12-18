from fastapi import FastAPI
from pydantic import BaseModel
from tdm import TDM  # aqui importa a classe que você já tem

app = FastAPI()
tdm = TDM()

class NumbersRequest(BaseModel):
    numbers: list[int]

@app.get("/")
def root():
    return {"status": "TDM API rodando"}

@app.post("/audit")
def audit(request: NumbersRequest):
    report = tdm.audit(request.numbers)
    return report

@app.post("/generate_laudo")
def generate_laudo(request: NumbersRequest):
    report = tdm.audit(request.numbers)
    tdm.generate_laudo(report)
    return {"status": "Laudo gerado", "numbers": request.numbers}
