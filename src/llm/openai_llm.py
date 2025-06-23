from openai import OpenAI
from src.llm.llm_model import LLMModel
import logging

logger = logging.getLogger(__name__)


class OpenAILLM(LLMModel):
    def __init__(self, api_key: str, model_name: str, base_url: str):
        try:
            self.client = OpenAI(
                api_key=api_key,
                base_url=base_url
            )
        except Exception as e:
            logger.error(f"Errore durante il caricamento del modello LLM tramite OpenAI: {e}")
            raise RuntimeError(f"Errore nel caricamento del modello: {model_name}") from e

        self.model_name = model_name

    def generate(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

