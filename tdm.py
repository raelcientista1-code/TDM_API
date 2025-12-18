import math
import statistics
import json
from datetime import datetime, timezone
from typing import List, Dict, Any
import logging
import os

# Configuração de log
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("tdm_engine.log"),
        logging.StreamHandler()
    ]
)

class TDM:
    """
    TDM — Teoria das Decomposicoes Multiplicativas
    Produto: TDM Engine (versao expandida)
    """

    def __init__(self, moduli: List[int] = None):
        self.version = "TDM-ENGINE-PROD-1.0"
        self.moduli = moduli or [
            3, 5, 7, 11, 13, 17, 19, 23,
            29, 31, 37, 41, 43, 47, 53
        ]
        logging.info(f"TDM Engine inicializada, versão {self.version}")

    def preprocess(self, n: int) -> int:
        if n <= 0:
            raise ValueError("Número inválido")
        while n % 2 == 0:
            n //= 2
        return n

    def structural_map(self, n: int) -> Dict[str, Any]:
        residues = [n % m for m in self.moduli]
        return {
            "residues": residues,
            "log_scale": math.log(n),
            "bit_length": n.bit_length(),
        }

    def operator(self, structure: Dict[str, Any]) -> Dict[str, Any]:
        r = structure["residues"]
        entropy = self._entropy(r)

        # 🔧 CORREÇÃO 1 — evita divisão por zero
        den = math.log2(len(self.moduli)) if len(self.moduli) > 1 else 1.0
        entropy_norm = entropy / den

        symmetry = self._residual_symmetry(r)

        return {
            "mean": statistics.mean(r),
            "stdev": statistics.pstdev(r),
            "entropy": entropy,
            "entropy_norm": entropy_norm,
            "symmetry": symmetry,
            "scale": structure["log_scale"],
        }

    def extract_trace(self, features: Dict[str, Any]) -> float:
        return (
            features["mean"]
            + 2.0 * features["stdev"]
            + 3.0 * features["entropy_norm"]
            + features["symmetry"]
            + 0.01 * features["scale"]
        )

    def classify(self, score: float) -> str:
        if score > 4.5:
            return "PROVAVEL_CHAVE_ARTIFICIAL"
        elif score > 3.0:
            return "SUSPEITA_ESTRUTURAL"
        else:
            return "COMPATIVEL_COM_CHAVE_REAL"

    def compute(self, n: int) -> float:
        try:
            n0 = self.preprocess(n)
            structure = self.structural_map(n0)
            features = self.operator(structure)
            trace = self.extract_trace(features)
            return trace
        except Exception as e:
            logging.error(f"Erro ao processar {n}: {e}")
            return float("nan")

    def audit(self, numbers: List[int], threshold: float = 3.0) -> Dict[str, Any]:
        traces = [self.compute(n) for n in numbers]
        baseline = {
            "mean": statistics.mean(traces),
            "stdev": statistics.pstdev(traces),
            "min": min(traces),
            "max": max(traces),
        }

        results = []
        for n, t in zip(numbers, traces):
            score = abs(t - baseline["mean"]) / (baseline["stdev"] + 1e-12)
            classification = self.classify(score)
            results.append({
                "number": n,
                "trace": t,
                "anomaly_score": score,
                "classification": classification,
            })

        report = {
            "tdm_version": self.version,
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "baseline": baseline,
            "threshold": threshold,
            "results": results,
        }

        logging.info(f"Auditoria finalizada para {len(numbers)} números")
        return report

    def generate_laudo(self, report: Dict[str, Any], folder: str = "reports") -> None:
        os.makedirs(folder, exist_ok=True)

        txt_path = os.path.join(
            folder,
            f"laudo_tdm_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )
        json_path = txt_path.replace(".txt", ".json")

        lines = [
            "LAUDO TECNICO - TDM",
            "=" * 60,
            f"Versao do motor : {report['tdm_version']}",
            f"Data (UTC)      : {report['timestamp']}",
            "",
            "1. BASELINE ESTATISTICO",
            "-" * 60
        ]

        for k, v in report["baseline"].items():
            lines.append(f"{k:<10}: {v:.6f}")

        lines.append("\n2. ANALISE ESTRUTURAL\n" + "-" * 60)

        for r in report["results"]:
            lines.append(f"Numero           : {r['number']}")
            lines.append(f"Traco TDM        : {r['trace']:.6f}")
            lines.append(f"Score estrutural : {r['anomaly_score']:.6f}")
            lines.append(f"Classificacao    : {r['classification']}")
            lines.append("-" * 60)

        text = "\n".join(lines)

        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(text)

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=True)

        logging.info(f"Laudo gerado: {txt_path} e {json_path}")

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
        # 🔧 CORREÇÃO 2 — evita pstdev em lista vazia
        if len(residues) < 2:
            return 0.0

        diffs = [
            abs(residues[i] - residues[i - 1])
            for i in range(1, len(residues))
        ]

        return statistics.pstdev(diffs)

