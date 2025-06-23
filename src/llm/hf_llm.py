from src.llm.llm_model import LLMModel
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch
import logging

logger = logging.getLogger(__name__)


class HFLLM(LLMModel):
    def __init__(self, model_name: str, device: str = None):
        # Se non specificato, usa GPU se disponibile
        if device is None:
            device = 0 if torch.cuda.is_available() else -1

        try:
            # Carica tokenizer e modello
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForCausalLM.from_pretrained(model_name)
        except Exception as e:
            logger.error(f"Errore durante il caricamento del modello LLM tramite HuggingFace: {e}")
            raise RuntimeError(f"Errore nel caricamento del modello: {model_name}") from e

        try:
            # Crea pipeline di generazione
            self.generator = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                device=device
            )
        except Exception as e:
            logger.error(f"Errore durante il caricamento della pipeline del modello LLM HuggingFace: {e}")
            raise RuntimeError(f"Errore nel caricamento della pipeline: {model_name}") from e

    def generate(self, prompt: str) -> str:
        result = self.generator(prompt, max_new_tokens=512, do_sample=True, top_p=0.95, temperature=0.7)
        return result[0]["generated_text"]
