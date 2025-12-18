import math
import statistics
import json
from datetime import datetime, timezone
from typing import List, Dict, Any
import logging
import os

# =========================
# Configuração de logging
# =========================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("tdm_engine.log"),
        logging.StreamHandler()
    ]
)

# =========================
# Classe principal TDM
# =========================
class TDM:
    """
    TDM — Teoria das Decomposições Multiplicativas
    Produto: TDM Engine (versão expandida)
    """

    def __init__(self, moduli: List[int] | None = None):
        self.version = "TDM-ENGINE-PROD-1.0"
        self.moduli = moduli or [
            3, 5, 7, 11, 13, 17, 19, 23,
            29, 31, 37, 41, 43, 47, 53
        ]
        logging.info(f"TDM Engine inicializada — versão {self.version}")

    # =========================
    # Pré-processamento
    # =========================
    def preprocess(self, n: int) -> int:
        if not isinstance(n, int) or n <= 0:
            raise ValueError("Número inválido")
        while n % 2 == 0:
            n //= 2
        return n

    # =========================
    # Estrutura modular
    # =========================
    def structural_map(self, n: int) -> Dict[str, Any]:
        residues = [n % m for m in self.moduli]
        return {
            "residues": residues,
            "log_scale": math.log(n),
            "bit_length": n.bit_length()
        }

    # =========================
    # Operador estrutural
    # =========================
    def operator(self, structure: Dict[str, Any]) -> Dict[str, Any]:
        residues = structure["residues"]

        entropy = self._entropy(residues)
        den = math.log2(len(self.moduli)) if len(self.moduli) > 1 else 1.0
        entropy_norm = entropy / den

        symmetry = self._residual_symmetry(residues)

        return {
            "mean": statistics.mean(residues),
            "stdev": statistics.pstdev(residues),
            "entropy": entropy,
            "entropy_norm": entropy_norm,
            "symmetry": symmetry,
            "scale": structure["log_scale"]
        }

    # =========================
    # Traço TDM
    # =========================
    def extract_trace(self, features: Dict[str, Any]) -> float:
        return (
            features["mean"]
            + 2.0 * features["stdev"]
            + 3.0 * features["entropy_norm"]
            + features["symmetry"]
            + 0.01 * features["scale"]
        )

    # =========================
    # Classificação
    # =========================
    def classify(self, score: float) -> str:
        if score > 4.5:
            return "PROVAVEL_CHAVE_ARTIFICIAL"
        if score > 3.0:
            return "SUSPEITA_ESTRUTURAL"
        return "COMPATIVEL_COM_CHAVE_REAL"

    # =========================
    # Cálculo individual
    # =========================
    def compute(self, n: int) -> float:
        try:
            n0 = self.preprocess(n)
            structure = self.structural_map(n0)
            features = self.operator(structure)
            return self.extract_trace(features)
        except Exception as e:
            logging.error(f"Erro ao processar {n}: {e}")
            return float("nan")

    # =========================
    # Auditoria em lote
    # =========================
    def audit(self, numbers: List[int], threshold: float = 3.0) -> Dict[str, Any]:
        traces = [self.compute(n) for n in numbers]

        baseline = {
            "mean": statistics.mean(traces),
            "stdev": statistics.pstdev(traces),
            "min": min(traces),
            "max": max(traces)
        }

        results = []
        for n, t in zip(numbers, traces):
            score = abs(t - baseline["mean"]) / (baseline["stdev"] + 1e-12)
            results.append({
                "number": n,
                "trace": t,
                "anomaly_score": score,
                "classification": self.classify(score)
            })

        report = {
            "tdm_version": self.version,
            "timestamp": datetime.now(timezone.utc)
            .isoformat()
            .replace("+00:00", "Z"),
            "baseline": baseline,
            "threshold": threshold,
            "results": results
        }

        logging.info(f"Auditoria concluída — {len(numbers)} números")
        return report

    # =========================
    # Laudo técnico
    # =========================
    def generate_laudo(self, report: Dict[str, Any], folder: str = "reports") -> None:
        os.makedirs(folder, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        txt_path = os.path.join(folder, f"laudo_tdm_{timestamp}.txt")
        json_path = os.path.join(folder, f"laudo_tdm_{timestamp}.json")

        lines = [
            "LAUDO TÉCNICO — TDM",
            "=" * 60,
            f"Versão        : {report['tdm_version']}",
            f"Data (UTC)   : {report['timestamp']}",
            "",
            "BASELINE",
            "-" * 60
        ]

        for k, v in report["baseline"].items():
            lines.append(f"{k:<8}: {v:.6f}")

        lines.append("\nANÁLISE\n" + "-" * 60)

        for r in report["results"]:
            lines.extend([
                f"Número         : {r['number']}",
                f"Traço TDM      : {r['trace']:.6f}",
                f"Score          : {r['anomaly_score']:.6f}",
                f"Classificação  : {r['classification']}",
                "-" * 60
            ])

        with open(txt_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        logging.info(f"Laudo salvo em {txt_path}")

    # =========================
    # Funções internas
    # =========================
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
        if len(residues) < 2:
            return 0.0
        diffs = [
            abs(residues[i] - residues[i - 1])
            for i in range(1, len(residues))
        ]
        return statistics.pstdev(diffs)

