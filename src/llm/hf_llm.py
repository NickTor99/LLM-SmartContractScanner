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
            self.max_input_tokens = self.generator.model.config.max_position_embeddings
        except Exception as e:
            logger.error(f"Errore durante il caricamento della pipeline del modello LLM HuggingFace: {e}")
            raise RuntimeError(f"Errore nel caricamento della pipeline: {model_name}") from e

    def generate(self, prompt: str) -> str:
        try:
            result = self.generator(prompt, do_sample=True, top_p=0.95, temperature=0.1)
            return result[0]["generated_text"]

        except Exception as e:
            num_tokens = len(self.tokenizer.encode(prompt))
            if num_tokens > self.max_input_tokens:
                logger.error(f"Prompt troppo lungo: {num_tokens} token (limite: {self.max_input_tokens})")
            else:
                logger.error(f"Errore durante la generazione del testo: {e}")
            raise


