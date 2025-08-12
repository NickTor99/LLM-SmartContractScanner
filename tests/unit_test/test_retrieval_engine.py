import unittest
from json import JSONDecodeError
from unittest.mock import MagicMock, patch

import requests

from api_server.core.retrieval_package.retrieval_engine import RetrievalEngine
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

    @patch("api_server.core.retrieval_package.retrieval_engine.ContractSearcher.search_vulns")
    def test_get_similar_contracts_success(self, mock_post):
        mock_post.return_value = [
                {"vulnerability": "arbitrary_delete", "score": 0.9},
                {"vulnerability": "rekey_to", "score": 0.85}
            ]

        with patch("api_server.core.utils.map_vulnerability", side_effect=lambda x: x):
            results = self.engine.get_similar_contracts("contract code")

        self.assertEqual(results, ["Arbitrary delete", "Unchecked Rekey to"])

    @patch("api_server.core.retrieval_package.retrieval_engine.ContractSearcher.search_vulns")
    def test_get_similar_contracts_http_error(self, mock_post):
        mock_post.side_effect = mock_post.side_effect = Exception()

        with self.assertRaises(Exception):
            results = self.engine.get_similar_contracts("contract code")


    @patch("api_server.core.retrieval_package.retrieval_engine.ContractSearcher.search_vulns")
    def test_get_similar_contracts_invalid_json(self, mock_post):
        mock_post.side_effect = mock_post.side_effect = Exception()

        with self.assertRaises(Exception):
            results = self.engine.get_similar_contracts("contract code")


    def test_get_similar_contracts_descriptor_or_embedder_error(self):
        self.mock_descriptor.get_description.side_effect = Exception("fail")
        with self.assertRaises(Exception):
            results = self.engine.get_similar_contracts("contract code")

