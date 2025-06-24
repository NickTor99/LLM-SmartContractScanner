import json
import unittest
from unittest.mock import MagicMock, patch

import requests

from src.retrieval_module.retrieval_engine import RetrievalEngine
from src.retrieval_module.embedding_model import EmbeddingModel
from src.retrieval_module.code_descriptor import CodeDescriptor
from requests.models import Response

class TestRetrievalEngineIntegration(unittest.TestCase):

    @patch("src.retrieval_module.code_descriptor.load_string", return_value="Descrivi il seguente codice:")
    def setUp(self, mock_load_string):
        self.embedder = EmbeddingModel(device="cpu")

        self.llm_model = MagicMock()

        self.descriptor = CodeDescriptor(self.llm_model)

        self.engine = RetrievalEngine(url="http://localhost:6333", embedder=self.embedder, descriptor=self.descriptor)

    def create_fake_response(self, data, status=200):
        response = Response()
        response.status_code = status
        response._content = json.dumps(data).encode('utf-8')
        return response

    @patch("src.retrieval_module.retrieval_engine.requests.post")
    def test_retrieval_simple_contract(self, mock_post):
        #Mock delle risposte di dipendenze esterne
        self.embedder.encode = MagicMock(return_value=[0.2, 0.4, 0.5])
        self.llm_model.generate = MagicMock(return_value="il codice fa questo...")

        mock_post.return_value = self.create_fake_response({
            "result": [
                {"vulnerability": "arbitrary_delete", "score": 0.9},
                {"vulnerability": "rekey_to", "score": 0.85}
            ]
        })

        code = "def approval(): return True"
        with patch("src.utils.map_vulnerability", side_effect=lambda x: x):
            result = self.engine.get_similar_contracts(code)
        self.assertIsInstance(result, list)
        self.assertTrue(all('Arbitrary delete' in r or 'Unchecked Rekey to' in r for r in result))

    @patch("src.retrieval_module.retrieval_engine.requests.post")
    def test_retrieval_empty_code(self, mock_post):
        #Mock delle risposte di dipendenze esterne
        self.embedder.encode = MagicMock(return_value=[0.2, 0.4, 0.5]) # codice vuoto fa comunque restituire un vettore pieno
        self.llm_model.generate = MagicMock(return_value="")

        mock_post.return_value = self.create_fake_response({
            "result": [
                {"vulnerability": "arbitrary_delete", "score": 0.9},
                {"vulnerability": "rekey_to", "score": 0.85}
            ]
        })

        result = self.engine.get_similar_contracts("")
        self.assertTrue(len(result) == 0) #se il codice è vuoto non devono essere rilevati contratti vulnerabili

    def test_embedder_failure(self):
        self.embedder.encode = MagicMock(side_effect=Exception())
        self.llm_model.generate = MagicMock(return_value="il codice fa questo...")

        code = "sample code"
        with self.assertRaises(Exception):
            result = self.engine.get_similar_contracts(code)

    def test_descriptor_failure(self):
        self.embedder.encode = MagicMock(return_value=[0.2, 0.4, 0.5]) #codice vuoto fa comunque restituire un vettore pieno
        self.descriptor.get_description = MagicMock(side_effect=Exception())

        code = "sample code"
        with self.assertRaises(Exception):
            result = self.engine.get_similar_contracts(code)

    @patch("src.retrieval_module.retrieval_engine.requests.post")
    def test_searcher_failure(self, mock_post):
        self.embedder.encode = MagicMock(return_value=[0.2, 0.4, 0.5])
        self.llm_model.generate = MagicMock(return_value="il codice fa questo...")
        response_error = Response()
        response_error.status_code = 500
        mock_post.return_value = response_error

        code = "sample code"
        with self.assertRaises(requests.exceptions.RequestException):
            result = self.engine.get_similar_contracts(code)

if __name__ == '__main__':
    unittest.main()
