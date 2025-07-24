import unittest
from unittest.mock import MagicMock

from qdrant_client.http.exceptions import UnexpectedResponse

from api_server.vector_db_service.contract_searcher import ContractSearcher  # Adatta il path se necessario

class TestContractSearcher(unittest.TestCase):

    def setUp(self):
        # Setup con client Qdrant mockato
        self.searcher = ContractSearcher(collection_name="contracts")
        self.searcher.qdrant_client = MagicMock()


    def test_invalid_collection_name(self):
        self.searcher.qdrant_client.query_points.side_effect = RuntimeError("Collection not found")

        with self.assertRaises(RuntimeError):
            self.searcher.search_vulns([0.1] * 768)

    def test_invalid_url_db(self):
        # Simuliamo errore di connessione al server Qdrant
        with self.assertRaises(Exception):
            ContractSearcher(collection_name="contracts", url_db="http://invalid:6333").search_vulns([0.1] * 768)

    def test_search_vulns_successful(self):
        # Mock del risultato del metodo query_points
        mock_result = MagicMock()
        mock_result.points = [
            MagicMock(payload={'contract_id': '1', 'vulnerability': 'reentrancy'}, score=0.91234),
            MagicMock(payload={'contract_id': '2', 'vulnerability': 'overflow'}, score=0.851234)
        ]
        self.searcher.qdrant_client.query_points.return_value = mock_result

        vector = [0.1] * 768  # Esempio di vettore
        result = self.searcher.search_vulns(vector)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["contract_id"], "1")
        self.assertEqual(result[1]["vulnerability"], "overflow")
        self.assertAlmostEqual(result[0]["score"], 0.912, places=3)

    def test_search_vulns_empty_result(self):
        mock_result = MagicMock()
        mock_result.points = []
        self.searcher.qdrant_client.query_points.return_value = mock_result

        vector = [0.0] * 768
        result = self.searcher.search_vulns(vector)
        self.assertEqual(result, [])

    def test_search_vulns_missing_fields(self):
        # Testa comportamento quando manca un campo nel payload
        mock_result = MagicMock()
        mock_result.points = [
            MagicMock(payload={"contract_id": "3"}, score=0.75)
        ]
        self.searcher.qdrant_client.query_points.return_value = mock_result

        with self.assertRaises(KeyError):
            self.searcher.search_vulns([0.1] * 768)
