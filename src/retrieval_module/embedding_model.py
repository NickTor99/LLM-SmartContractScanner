import logging
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)


class EmbeddingModel:
    def __init__(
            self,
            model_name: str = "hkunlp/instructor-xl",
            device: str = "cpu",
            instruction: str = "Represent the semantic behavior of the smart contract for similarity-based retrieval."
    ):
        """
        Inizializza il modello di embedding usando SentenceTransformer.
        """
        self.device = device
        self.instruction = instruction

        try:
            self.model = SentenceTransformer(model_name, device=device)
            self.max_length = self.model.tokenizer.model_max_length
        except Exception as e:
            logger.error(f"Errore durante il caricamento del modello di embedding: {e}")
            raise RuntimeError(f"Errore nel caricamento del modello: {model_name}") from e


    def encode(self, text: str) -> list:
        """
        Genera un vettore embedding a partire da un testo.
        """
        total_input = f"{self.instruction} {text}"
        token_count = len(self.model.tokenizer.tokenize(total_input))
        if token_count > self.max_length:
            raise Exception(f"Input troppo lungo: {token_count} token (max {self.max_length})")
        try:
            input_data = [[self.instruction, text]]
            embedding = self.model.encode(input_data)
            return embedding[0].tolist()
        except Exception as e:
            logger.error(f"Errore durante la generazione dell'embedding: {e}")
            return []

