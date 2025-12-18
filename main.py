from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from TDM import TDM  # Certifique-se que o arquivo TDM.py está no mesmo diretório

# Inicializa FastAPI e TDM
app = FastAPI(title="TDM API", version="1.0")
tdm = TDM()

# Modelo para auditoria
class AuditRequest(BaseModel):
    numbers: List[int]
    threshold: float = 3.0

# Endpoint raiz
@app.get("/")
def root():
    return {"status": "TDM API rodando"}

# Endpoint de auditoria
@app.post("/audit")
def audit(request: AuditRequest):
    report = tdm.audit(request.numbers, request.threshold)
    return report

# Endpoint de geração de laudo
@app.post("/generate_laudo")
def generate_laudo(request: AuditRequest):
    report = tdm.audit(request.numbers, request.threshold)
    tdm.generate_laudo(report)
    return {"status": "Laudo gerado com sucesso", "numbers": request.numbers}
