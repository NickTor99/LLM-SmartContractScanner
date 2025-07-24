import logging
from api_server.core.llm.llm_model import LLMModel
from api_server.core.utils import load_string

logger = logging.getLogger(__name__)


class CodeDescriptor:
    def __init__(self, llm_model: LLMModel):
        try:
            self.prompt = load_string("prompts/code_description_prompt")
        except Exception as e:
            logger.error(f"Errore nel caricamento del prompt di descrizione: {e}")
            raise RuntimeError("Impossibile caricare il prompt per CodeDescriptor.") from e

        self.llm_model = llm_model


    def get_description(self, code: str) -> str:
        full_prompt = f"{self.prompt}\n\n{code}"
        try:
            response = self.llm_model.generate(prompt=full_prompt)
        except Exception as e:
            logger.error(f"Errore durante la generazione della descrizione con LLM: {e}")
            return "Errore nella generazione della descrizione"

        return response

