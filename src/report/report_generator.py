from abc import abstractmethod, ABC
import os
import re
import logging
from typing import List

logger = logging.getLogger(__name__)

class ReportGenerator(ABC):
    def __init__(self, out_dir: str):
        self.out_dir = out_dir

    def generate(self, results: List[dict], file_path: str, report_name: str=None):
        data = self.prepare_data(results)
        content = self.render(data, file_path)
        output_path = self.make_outpath(report_name, file_path)
        self.write(content, output_path)

    def prepare_data(self, results: List[dict]) -> List[dict]:
        # Regex più robuste e insensibili al caso
        pattern1 = re.compile(
            r"#+\s*Step\s*3\s*[-–]\s*Final\s*Evaluation\s*[:：]?(.*?)#+\s*Step\s*4\s*[-–]\s*Remediation",
            re.IGNORECASE | re.DOTALL
        )
        pattern2 = re.compile(
            r"\*\*\s*Vulnerable\s*Code\s*Snippet\s*:\*\*(.*?)\*\*\s*Secure\s*Code\s*Snippet\s*:\*\*(.*?)($|\n|\r)",
            re.IGNORECASE | re.DOTALL
        )
        pattern3 = re.compile(
            r"\*\*\s*Secure\s*Code\s*Snippet\s*:\*\*(.*?)($)",
            re.IGNORECASE | re.DOTALL
        )

        processed_data = []

        for i, result in enumerate(results):
            try:
                analysis = result.get("analysis", "")
                vulnerability = result.get("vulnerability", "Unknown")

                if not analysis:
                    logger.warning(f"[Entry {i}] Campo 'analysis' mancante o vuoto. Saltato.")
                    continue

                match_eval = pattern1.search(analysis)
                if not match_eval:
                    logger.warning(f"[Entry {i}] Nessuna sezione di valutazione trovata per '{vulnerability}'. Saltato.")
                    continue

                eval_text = match_eval.group(1).strip()
                if "not vulnerable" in eval_text.lower():
                    logger.info(f"[Entry {i}] '{vulnerability}' non risulta vulnerabile. Saltato.")
                    continue

                entry = {
                    "vulnerability": vulnerability,
                    "description": eval_text
                }

                match_vulnerable_code = pattern2.search(analysis)
                if match_vulnerable_code:
                    entry["vulnerable_code"] = match_vulnerable_code.group(1).strip()

                match_secure_code = pattern3.search(analysis)
                if match_secure_code:
                    entry["secure_code"] = match_secure_code.group(1).strip()
                    logger.info(f"[Entry {i}] Codice sicuro rilevato ma manca snippet vulnerabile.")
                else:
                    logger.warning(f"[Entry {i}] Nessun codice trovato per '{vulnerability}'.")

                processed_data.append(entry)

            except Exception as e:
                logger.error(f"[Entry {i}] Errore durante l'elaborazione: {e}", exc_info=True)

        return processed_data

    @abstractmethod
    def render(self, data: List[dict],  contract_path: str):
        pass

    def make_outpath(self, report_name, file_path) -> str:
        if report_name is None:
            report_name = str(os.path.basename(file_path)).split(".")[0]

        out_path = os.path.join(self.out_dir, f"{report_name}.html")

        i = 2
        while os.path.exists(out_path):
            out_path = os.path.join(self.out_dir, f"{report_name}{i}.html")
            i = i+1

        return out_path

    def write(self, content: str, output_path: str):
        with open(output_path, "w") as f:
            f.write(content)










