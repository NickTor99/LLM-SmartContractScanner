import json
from typing import List
import requests
from requests import Response
import logging
from src.retrieval_module.code_descriptor import CodeDescriptor
from src.retrieval_module.embedding_model import EmbeddingModel
from src.utils import map_vulnerability


logger = logging.getLogger(__name__)


class RetrievalEngine:
    def __init__(self, url: str, descriptor: CodeDescriptor, embedder: EmbeddingModel, num_retrieve=2):
        """
        Inizializza il modulo RetrievalEngine con l'URL di ricerca, descrittore e modello di embedding.
        """
        self.url = url
        self.descriptor = descriptor
        self.embedder = embedder
        self.num_retrieve = num_retrieve

    def get_similar_contracts(self, code: str) -> List[str]:
        """
        Ottiene i contratti simili analizzando il codice tramite descrizione e vettori embedding.
        """
        if code == "":
            logger.error("Errore: il codice inserito è vuoto")
            return []

        try:
            description = self.descriptor.get_description(code)
            vector = self.embedder.encode(description)
        except Exception as e:
            logger.error(f"Errore durante la generazione della descrizione o embedding: {e}")
            raise

        try:
            response = requests.post(self.url, json={"vector": vector}, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error(f"Errore nella richiesta HTTP al servizio di retrieval: {e}")
            raise

        try:
            return self._filter_response(response)
        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"Errore nel parsing della risposta del servizio di retrieval: {e}")
            raise

    def _filter_response(self, response: Response) -> list:
        """
        Filtra la risposta e restituisce i nomi delle vulnerabilità più rilevanti.
        """
        retrieval_results = {}
        for j in json.loads(response.text)['result']:
            name = map_vulnerability(j['vulnerability'])
            retrieval_results[name] = j['score']
        top_retrieval = list(retrieval_results)[:self.num_retrieve]
        return top_retrieval
