import unittest
from json import JSONDecodeError
from unittest.mock import MagicMock, patch

import requests

from src.retrieval_module.retrieval_engine import RetrievalEngine
from requests.models import Response
import json


class TestRetrievalEngine(unittest.TestCase):

    def setUp(self):
        # Stub di CodeDescriptor
        self.mock_descriptor = MagicMock()
        self.mock_descriptor.get_description.return_value = "contract description"

        # Stub di EmbeddingModel
        self.mock_embedder = MagicMock()
        self.mock_embedder.encode.return_value = [0.1, 0.2, 0.3]

        self.engine = RetrievalEngine(
            url="http://fake-service/retrieve",
            descriptor=self.mock_descriptor,
            embedder=self.mock_embedder,
            num_retrieve=2
        )

    def create_fake_response(self, data, status=200):
        response = Response()
        response.status_code = status
        response._content = json.dumps(data).encode('utf-8')
        return response

    @patch("src.retrieval_module.retrieval_engine.requests.post")
    def test_get_similar_contracts_success(self, mock_post):
        mock_post.return_value = self.create_fake_response({
            "result": [
                {"vulnerability": "arbitrary_delete", "score": 0.9},
                {"vulnerability": "rekey_to", "score": 0.85}
            ]
        })

        with patch("src.utils.map_vulnerability", side_effect=lambda x: x):
            results = self.engine.get_similar_contracts("contract code")

        self.assertEqual(results, ["Arbitrary delete", "Unchecked Rekey to"])

    @patch("src.retrieval_module.retrieval_engine.requests.post")
    def test_get_similar_contracts_http_error(self, mock_post):
        mock_post.side_effect = requests.exceptions.RequestException()

        with self.assertRaises(requests.exceptions.RequestException):
            results = self.engine.get_similar_contracts("contract code")


    @patch("src.retrieval_module.retrieval_engine.requests.post")
    def test_get_similar_contracts_invalid_json(self, mock_post):
        response = Response()
        response.status_code = 200
        response._content = b"Not a JSON"
        mock_post.return_value = response

        with self.assertRaises(JSONDecodeError):
            results = self.engine.get_similar_contracts("contract code")


    def test_get_similar_contracts_descriptor_or_embedder_error(self):
        self.mock_descriptor.get_description.side_effect = Exception("fail")
        with self.assertRaises(Exception):
            results = self.engine.get_similar_contracts("contract code")

