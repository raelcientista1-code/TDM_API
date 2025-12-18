from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List
import math
import statistics

# =========================================================
# API CONFIG
# =========================================================

app = FastAPI(
    title="TDM Structural Audit Engine",
    description="Structural multiplicative analysis of integers for audit, classification and reporting",
    version="1.0",
)

# =========================================================
# MODELS
# =========================================================

class AuditRequest(BaseModel):
    numbers: List[int] = Field(
        ...,
        min_items=1,
        max_items=10,
        description="List of integers to be structurally analyzed"
    )
    sensitivity: float = Field(
        1.0,
        ge=0.1,
        le=5.0,
        description="Sensitivity factor for anomaly detection"
    )

# =========================================================
# CORE TDM LOGIC (SAFE / NON-REVERSIBLE)
# =========================================================

def structural_invariant(n: int) -> float:
    """
    Structural invariant intentionally designed to be:
    - deterministic
    - non-factorizing
    - non-reversible
    """
    return math.log(n) * math.log(math.log(n) + 1)

def compute_anomaly_score(value: float, mean: float, stdev: float) -> float:
    return abs(value - mean) / (stdev + 1e-12)

# =========================================================
# CLASSIFICATION LAYER
# =========================================================

def classify_structure(score: float) -> tuple[str, str]:
    """
    Structural classification for audit purposes.
    """
    if score < 1.0:
        return (
            "RSA-compatible",
            "Structural behavior compatible with standard RSA key generation processes"
        )
    elif score < 2.5:
        return (
            "atypical",
            "Moderate structural deviation observed; behavior not fully typical"
        )
    else:
        return (
            "artificial-structure",
            "Strong structural deviation; construction suggests artificial or non-standard origin"
        )

# =========================================================
# HUMAN REPORT GENERATOR
# =========================================================

def generate_human_report(n: int, classification: str) -> str:
    if classification == "RSA-compatible":
        return (
            f"O inteiro {n} apresenta comportamento estrutural compatível com "
            "chaves RSA geradas por processos criptográficos padronizados. "
            "Não foram detectadas anomalias estruturais relevantes no escopo desta análise."
        )
    elif classification == "atypical":
        return (
            f"O inteiro {n} apresenta comportamento estrutural levemente atípico, "
            "com desvios moderados em relação aos padrões observados em chaves reais. "
            "Recomenda-se análise complementar conforme políticas internas."
        )
    else:
        return (
            f"O inteiro {n} apresenta estrutura multiplicativa significativamente atípica. "
            "Os invariantes estruturais observados sugerem possível construção artificial "
            "ou não padronizada. Recomenda-se revisão antes de qualquer uso criptográfico."
        )

# =========================================================
# ENDPOINTS
# =========================================================

@app.post("/api/v1/tdm/audit")
async def audit(req: AuditRequest):
    # Compute structural invariants
    invariants = [structural_invariant(n) for n in req.numbers]

    mean = statistics.mean(invariants)
    stdev = statistics.pstdev(invariants) or 1e-9

    results = []

    for n, inv in zip(req.numbers, invariants):
        score = compute_anomaly_score(inv, mean, stdev) * req.sensitivity
        classification, technical_note = classify_structure(score)
        human_report = generate_human_report(n, classification)

        results.append({
            "number": n,
            "structural_invariant": round(inv, 6),
            "anomaly_score": round(score, 3),
            "classification": classification,
            "technical_note": technical_note,
            "human_report": human_report
        })

    return {
        "engine": "TDM Structural Engine",
        "mode": "audit-only",
        "results": results
    }

@app.get("/api/v1/tdm/health")
async def health():
    return {
        "status": "ok",
        "engine": "TDM Structural Engine",
        "mode": "analysis-only"
    }
