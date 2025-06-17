import json
import logging
from llm.llm_model import LLMModel  # Assicurati di adattare l'import corretto
from utils import load_string

logger = logging.getLogger(__name__)

class VulnAnalysis:
    def __init__(self, llm_model: LLMModel):
        """
        Inizializza il modulo VulnAnalysis con il modello LLM.
        """
        self.llm_model = llm_model

    def get_vuln_analysis(self, vuln: str, code: str) -> str:
        """
        Analizza il codice in base alla vulnerabilità fornita.
        """
        try:
            details = self._get_vuln_details(vuln)
            prompt = self._get_prompt(vuln, details, code)
            response = self.llm_model.generate(prompt=prompt)
            return response
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.error(f"Errore nel caricamento dei dettagli della vulnerabilità: {e}")
            return f"Errore: Impossibile caricare i dettagli della vulnerabilità {vuln}."
        except KeyError as e:
            logger.error(f"Chiave mancante nei dettagli della vulnerabilità: {e}")
            return f"Errore: Dettagli incompleti per la vulnerabilità {vuln}."
        except Exception as e:
            logger.error(f"Errore inatteso durante l'analisi della vulnerabilità: {e}")
            return f"Errore durante l'elaborazione della vulnerabilità {vuln}."

    def _get_prompt(self, vuln: str, details: dict, code: str) -> str:
        """
        Costruisce il prompt da passare al modello LLM.
        """
        try:
            system_prompt = load_string("src/prompts/vuln_analysis_prompt")

            prompt = f"""
### Vulnerability to Analyze:
- **Name:** {vuln}
- **Description:** {details['description']}
- **Attack Scenario:** {details['attack_scenario']}

---

### Precondition for the Vulnerability:
{details['precondition']}

---

### Contract to Analyze:

```pyteal
{code}
"""
            return f"{system_prompt}\n\n{prompt}"
        except KeyError as e:
            logger.error(f"Chiave mancante nel file di dettagli della vulnerabilità: {e}")
            raise
        except Exception as e:
            logger.error(f"Errore nella costruzione del prompt: {e}")
            raise

    def _get_vuln_details(self, vuln: str) -> dict:
        """
        Carica i dettagli della vulnerabilità da file.
        """
        file_path = "src/analysis_module/algorand_vuln_info.json"
        with open(file_path, "r") as file:
            data = json.load(file)

        for d in data.get('vulnerabilities', []):
            if d.get('name') == vuln:
                return d

        raise KeyError(f"Vulnerabilità '{vuln}' non trovata nel file.")
