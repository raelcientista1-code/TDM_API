import math
import statistics
import json
import logging
import os
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

# ============================================================
# CONFIGURAÇÃO DE LOGGING
# ============================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("tdm_engine.log"),
        logging.StreamHandler()
    ]
)

# ============================================================
# TDM ENGINE
# ============================================================
class TDM:
    """
    TDM — Teoria das Decomposições Multiplicativas
    Auditoria estrutural criptográfica
    """

    def __init__(self, moduli: Optional[List[int]] = None):
        self.version = "TDM-ENGINE-CORE-1.1"

        self.moduli = moduli or [
            3, 5, 7, 11, 13, 17, 19,
            23, 29, 31, 37, 41, 43,
            47, 53
        ]

        logging.info(f"TDM Engine inicializada — versão {self.version}")

    # ========================================================
    # 1. PRÉ-PROCESSAMENTO
    # ========================================================
    def preprocess(self, n: int) -> int:
        if not isinstance(n, int) or n <= 1:
            raise ValueError("Entrada inválida")

        while n % 2 == 0:
            n //= 2

        return n

    # ========================================================
    # 2. MAPA ESTRUTURAL
    # ========================================================
    def structural_map(self, n: int) -> Dict[str, Any]:
        return {
            "residues": [n % m for m in self.moduli],
            "bit_length": n.bit_length(),
            "log_scale": math.log(n),
            "decimal_entropy": self._decimal_entropy(n),
            "digit_diversity": self._digit_diversity(n)
        }

    # ========================================================
    # 3. OPERADOR TDM
    # ========================================================
    def operator(self, s: Dict[str, Any]) -> Dict[str, float]:
        residues = s["residues"]

        mean = statistics.mean(residues)
        stdev = statistics.pstdev(residues)

        entropy_mod = self._entropy(residues)
        entropy_mod_norm = entropy_mod / math.log2(len(self.moduli))

        symmetry = self._residual_symmetry(residues)
        dispersion = stdev / (mean + 1e-12)

        # Penalizações criptográficas
        bit_penalty = max(0.0, 2048 - s["bit_length"]) / 2048
        decimal_penalty = 1.0 - s["decimal_entropy"]
        digit_penalty = 1.0 - s["digit_diversity"]

        return {
            "mean": mean,
            "stdev": stdev,
            "entropy_mod": entropy_mod_norm,
            "symmetry": symmetry,
            "dispersion": dispersion,
            "bit_penalty": bit_penalty,
            "decimal_penalty": decimal_penalty,
            "digit_penalty": digit_penalty,
            "scale": s["log_scale"]
        }

    # ========================================================
    # 4. TRAÇO TDM (UNIFICADO)
    # ========================================================
    def extract_trace(self, f: Dict[str, float]) -> float:
        return (
            f["mean"]
            + 2.0 * f["stdev"]
            + 3.0 * f["entropy_mod"]
            + f["symmetry"]
            + f["dispersion"]
            + 2.5 * f["bit_penalty"]
            + 2.0 * f["decimal_penalty"]
            + 1.5 * f["digit_penalty"]
            + 0.01 * f["scale"]
        )

    # ========================================================
    # 5. CLASSIFICAÇÃO
    # ========================================================
    def classify(self, score: float) -> str:
        if score >= 4.5:
            return "PROVAVEL_CHAVE_ARTIFICIAL"
        if score >= 3.0:
            return "SUSPEITA_ESTRUTURAL"
        return "COMPATIVEL_COM_CHAVE_REAL"

    # ========================================================
    # 6. CÁLCULO INDIVIDUAL
    # ========================================================
    def compute(self, n: int) -> Dict[str, Any]:
        n0 = self.preprocess(n)
        s = self.structural_map(n0)
        f = self.operator(s)
        trace = self.extract_trace(f)

        return {
            "number": n,
            "trace": trace,
            "features": f
        }

    # ========================================================
    # 7. AUDITORIA EM LOTE
    # ========================================================
    def audit(self, numbers: List[int]) -> Dict[str, Any]:
        evaluations = [self.compute(n) for n in numbers]
        traces = [e["trace"] for e in evaluations]

        baseline = {
            "mean": statistics.mean(traces),
            "stdev": statistics.pstdev(traces),
            "min": min(traces),
            "max": max(traces)
        }

        results = []
        for e in evaluations:
            score = abs(e["trace"] - baseline["mean"]) / (baseline["stdev"] + 1e-12)
            results.append({
                "number": e["number"],
                "trace": e["trace"],
                "anomaly_score": score,
                "classification": self.classify(score)
            })

        return {
            "tdm_version": self.version,
            "timestamp": datetime.now(timezone.utc)
                .isoformat().replace("+00:00", "Z"),
            "baseline": baseline,
            "results": results
        }

    # ========================================================
    # FUNÇÕES INTERNAS
    # ========================================================
    def _entropy(self, data: List[int]) -> float:
        counts = {}
        for x in data:
            counts[x] = counts.get(x, 0) + 1

        ent = 0.0
        total = len(data)
        for c in counts.values():
            p = c / total
            ent -= p * math.log2(p)

        return ent

    def _residual_symmetry(self, residues: List[int]) -> float:
        diffs = [abs(residues[i] - residues[i - 1])
                 for i in range(1, len(residues))]
        return statistics.pstdev(diffs) if diffs else 0.0

    def _decimal_entropy(self, n: int) -> float:
        digits = str(abs(n))
        counts = {}
        for d in digits:
            counts[d] = counts.get(d, 0) + 1

        ent = 0.0
        total = len(digits)
        for c in counts.values():
            p = c / total
            ent -= p * math.log2(p)

        return ent / math.log2(10)

    def _digit_diversity(self, n: int) -> float:
        digits = set(str(abs(n)))
        return len(digits) / 10.0
