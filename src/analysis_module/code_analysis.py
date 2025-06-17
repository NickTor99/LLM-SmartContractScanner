import json
import re
from llm.llm_model import LLMModel
from utils import load_string
import logging
from typing import List

logger = logging.getLogger(__name__)

class CodeAnalysis:
    def __init__(self, llm_model: LLMModel, num_model: int = 2):
        """
        Inizializza il modulo ModelAnalysis con i prompt e il modello LLM.

        :param llm_model: Oggetto o interfaccia del modello LLM.
        :param num_model: Numero di possibili vulnerabilità che il modello restituirà.
        """
        try:
            self.prompt = load_string("src/prompts/code_analysis_prompt")
        except Exception as e:
            logger.error(f"Errore nel caricamento del prompt per CodeAnalysis: {e}")
            raise RuntimeError("Impossibile caricare il prompt per CodeAnalysis.") from e

        self.llm_model = llm_model
        self.num_model = num_model

    def get_possible_vulns(self, code: str) -> List[str]:
        """
        Analizza il codice fornito per identificare possibili vulnerabilità.

        :param code: Codice sorgente da analizzare.
        :return: Lista di vulnerabilità potenzialmente presenti nel codice.
        """
        full_prompt = f"{self.prompt}\n\n{code}"
        try:
            response = self.llm_model.generate(prompt=full_prompt)
        except Exception as e:
            logger.error(f"Errore durante la generazione con il modello LLM: {e}")
            return []
        try:
            return self._parse_response(response)
        except Exception as e:
            logger.error(f"Errore durante il parsing della risposta: {e}")
            return []

    def _parse_response(self, response: str) -> List[str]:
        """
        Elabora la risposta del modello LLM e ne estrae le vulnerabilità.

        :param response: Risposta testuale del modello.
        :return: Lista di vulnerabilità individuate.
        """
        try:
            res = re.split(r"```list", response)[1].strip()
            res = re.split(r"```", res)[0].strip()
        except IndexError as e:
            logger.warning("Formato della risposta inatteso. Nessuna sezione '```list' trovata.")
            return []

        try:
            model_results = json.loads(res)[:self.num_model]
        except json.JSONDecodeError as e:
            logger.warning(f"Errore nel parsing JSON della risposta: {e}")
            return []

        return model_results

