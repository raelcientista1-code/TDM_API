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

    Produto: TDM Engine
    Natureza: Auditoria estrutural criptográfica
    Escopo: Detecção de padrões artificiais e anomalias matemáticas
    """

    # --------------------------------------------------------
    # Inicialização
    # --------------------------------------------------------
    def __init__(self, moduli: Optional[List[int]] = None):
        self.version = "TDM-ENGINE-CORE-1.0"

        # Conjunto modular fixo (não sensível)
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
        """
        Normaliza o número sem extrair fatores relevantes.
        Remove potências triviais de 2 (estrutura pública).
        """
        if not isinstance(n, int) or n <= 1:
            raise ValueError("Entrada inválida")

        while n % 2 == 0:
            n //= 2

        return n

    # ========================================================
    # 2. MAPA ESTRUTURAL
    # ========================================================
    def structural_map(self, n: int) -> Dict[str, Any]:
        """
        Cria a assinatura estrutural modular do número.
        """
        residues = [n % m for m in self.moduli]

        return {
            "residues": residues,
            "bit_length": n.bit_length(),
            "log_scale": math.log(n)
        }

    # ========================================================
    # 3. OPERADOR TDM
    # ========================================================
    def operator(self, structure: Dict[str, Any]) -> Dict[str, float]:
        residues = structure["residues"]

        mean = statistics.mean(residues)
        stdev = statistics.pstdev(residues)

        entropy = self._entropy(residues)
        entropy_norm = entropy / math.log2(len(self.moduli))

        symmetry = self._residual_symmetry(residues)

        dispersion = stdev / (mean + 1e-12)

        return {
            "mean": mean,
            "stdev": stdev,
            "entropy": entropy,
            "entropy_norm": entropy_norm,
            "symmetry": symmetry,
            "dispersion": dispersion,
            "scale": structure["log_scale"]
        }

    # ========================================================
    # 4. EXTRAÇÃO DO TRAÇO TDM
    # ========================================================
    def extract_trace(self, features: Dict[str, float]) -> float:
        """
        Traço escalar invariável.
        """
        return (
            features["mean"]
            + 2.0 * features["stdev"]
            + 3.0 * features["entropy_norm"]
            + features["symmetry"]
            + features["dispersion"]
            + 0.01 * features["scale"]
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
        """
        Avalia um único número e retorna estrutura completa.
        """
        n0 = self.preprocess(n)
        structure = self.structural_map(n0)
        features = self.operator(structure)
        trace = self.extract_trace(features)

        return {
            "number": n,
            "trace": trace,
            "features": features
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

        report = {
            "tdm_version": self.version,
            "timestamp": datetime.now(timezone.utc)
                .isoformat().replace("+00:00", "Z"),
            "baseline": baseline,
            "results": results
        }

        logging.info(f"Auditoria concluída — {len(numbers)} entradas")
        return report

    # ========================================================
    # 8. LAUDO TÉCNICO (HUMANO + JSON)
    # ========================================================
    def generate_laudo(self, report: Dict[str, Any], folder: str = "reports") -> None:
        os.makedirs(folder, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")

        txt_path = os.path.join(folder, f"laudo_tdm_{ts}.txt")
        json_path = os.path.join(folder, f"laudo_tdm_{ts}.json")

        lines = [
            "LAUDO TÉCNICO — TDM ENGINE",
            "=" * 70,
            f"Versão      : {report['tdm_version']}",
            f"Data (UTC) : {report['timestamp']}",
            "",
            "BASELINE",
            "-" * 70
        ]

        for k, v in report["baseline"].items():
            lines.append(f"{k:<10}: {v:.6f}")

        lines.append("\nANÁLISE INDIVIDUAL")
        lines.append("-" * 70)

        for r in report["results"]:
            lines.extend([
                f"Número        : {r['number']}",
                f"Traço TDM     : {r['trace']:.6f}",
                f"Score         : {r['anomaly_score']:.6f}",
                f"Classificação : {r['classification']}",
                "-" * 70
            ])

        with open(txt_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        logging.info(f"Laudo gerado: {txt_path}")

    # ========================================================
    # FUNÇÕES INTERNAS (NÃO EXPOSTAS)
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
        diffs = [
            abs(residues[i] - residues[i - 1])
            for i in range(1, len(residues))
        ]
        return statistics.pstdev(diffs) if diffs else 0.0


