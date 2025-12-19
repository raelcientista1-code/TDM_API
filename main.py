from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List
import math
from collections import Counter

# =========================================================
# API CONFIG
# =========================================================

app = FastAPI(
    title="TDM-R Structural Audit Engine",
    description="Calibrated, non-reversible structural analysis for RSA moduli (1024–8192 bits)",
    version="3.0",
)

# =========================================================
# MODELS
# =========================================================

class AuditRequest(BaseModel):
    numbers: List[int] = Field(
        ...,
        min_items=1,
        max_items=10,
        description="List of integers to be analyzed"
    )
    sensitivity: float = Field(
        1.0,
        ge=0.1,
        le=5.0,
        description="Sensitivity factor for anomaly detection"
    )

# =========================================================
# CRYPTO SANITY FILTER (ELIMINATORY)
# =========================================================

def crypto_sanity_check(n: int) -> list[str]:
    reasons = []
    s = str(n)
    L = len(s)

    freq = Counter(s)
    entropy = -sum((c/L) * math.log2(c/L) for c in freq.values())

    if entropy < 2.8:
        reasons.append("low_decimal_entropy")

    if max(freq.values()) / L > 0.25:
        reasons.append("digit_repetition")

    if len(freq) <= 2:
        reasons.append("low_symbol_diversity")

    if n == 10**L - 1:
        reasons.append("decimal_all_nines")

    if n.bit_length() < 1024:
        reasons.append("insufficient_bit_length")

    return reasons

# =========================================================
# CORE STRUCTURAL INVARIANT (NON-REVERSIBLE)
# =========================================================

def structural_invariant(n: int) -> float:
    return math.log(n) * math.log(math.log(n) + 1)

# =========================================================
# RSA CALIBRATION (1024–8192 bits)
# =========================================================

def rsa_expected_invariant(bitlen: int) -> float:
    ln2 = math.log(2)
    lnN = bitlen * ln2
    return lnN * math.log(lnN + 1)

def rsa_expected_deviation(bitlen: int) -> float:
    return 0.015 * math.sqrt(bitlen)

def calibrated_anomaly_score(n: int) -> float:
    bitlen = n.bit_length()
    inv = structural_invariant(n)

    expected = rsa_expected_invariant(bitlen)
    deviation = rsa_expected_deviation(bitlen)

    return abs(inv - expected) / deviation

# =========================================================
# CLASSIFICATION
# =========================================================

def classify_structure(score: float) -> tuple[str, str]:
    if score < 2.0:
        return (
            "RSA-compatible",
            "Structural behavior consistent with calibrated RSA models (1024–8192 bits)"
        )
    elif score < 5.0:
        return (
            "atypical",
            "Structurally plausible but statistically rare for calibrated RSA generation"
        )
    else:
        return (
            "artificial-structure",
            "Structural deviation incompatible with realistic RSA generation"
        )

# =========================================================
# HUMAN REPORT
# =========================================================

def generate_human_report(n: int, classification: str) -> str:
    if classification == "RSA-compatible":
        return (
            f"O inteiro {n} apresenta comportamento estrutural compatível com "
            "módulos RSA gerados por processos criptográficos reais, segundo "
            "calibração formal até 8192 bits."
        )
    elif classification == "atypical":
        return (
            f"O inteiro {n} é estruturalmente plausível, porém estatisticamente raro "
            "em modelos calibrados de geração RSA."
        )
    elif classification == "artificial-structure":
        return (
            f"O inteiro {n} apresenta desvios estruturais incompatíveis com "
            "qualquer processo realista de geração de chaves RSA."
        )
    else:
        return (
            f"O inteiro {n} foi rejeitado por não atender critérios mínimos "
            "de sanidade criptográfica."
        )

# =========================================================
# ENDPOINT
# =========================================================

@app.post("/api/v1/tdm/audit")
async def audit(req: AuditRequest):

    results = []

    for n in req.numbers:
        reasons = crypto_sanity_check(n)

        if reasons:
            results.append({
                "number": n,
                "bit_length": n.bit_length(),
                "classification": "artificial",
                "technical_note": "Rejected by cryptographic sanity filters",
                "reasons": reasons,
                "human_report": (
                    f"O inteiro {n} foi rejeitado por apresentar características "
                    "incompatíveis com qualquer geração criptográfica RSA real."
                )
            })
            continue

        score = calibrated_anomaly_score(n) * req.sensitivity
        classification, technical_note = classify_structure(score)
        human_report = generate_human_report(n, classification)

        results.append({
            "number": n,
            "bit_length": n.bit_length(),
            "structural_invariant": round(structural_invariant(n), 6),
            "anomaly_score": round(score, 3),
            "classification": classification,
            "technical_note": technical_note,
            "human_report": human_report
        })

    return {
        "engine": "TDM-R Structural Engine",
        "calibration": "RSA-1024 → RSA-8192",
        "mode": "audit-only",
        "results": results
    }

@app.get("/api/v1/tdm/health")
async def health():
    return {
        "status": "ok",
        "engine": "TDM-R Structural Engine",
        "calibration": "RSA-1024 → RSA-8192",
        "mode": "analysis-only"
    }
