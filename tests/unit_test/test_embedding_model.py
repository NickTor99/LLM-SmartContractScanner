from cli_tool.retrieval_package.embedding_model import EmbeddingModel
import unittest
from unittest.mock import patch, MagicMock


class TestEmbeddingModelRealModel(unittest.TestCase):

    def setUp(self):
        # Usa CPU per garantire compatibilità ovunque
        self.embedding_model = EmbeddingModel(device="cpu")

    def test_init_failure(self):
        with self.assertRaises(RuntimeError):
            EmbeddingModel(model_name="non-existent")

    def test_encode_failure(self):
        mock_model = MagicMock()
        self.embedding_model.model = mock_model
        mock_model.encode.side_effect = Exception("Encoding error")
        result = self.embedding_model.encode("error test")
        self.assertEqual(result, [])

    def test_encode_valid_input(self):
        text = "This is a simple smart contract function."
        embedding = self.embedding_model.encode(text)
        print(embedding)
        self.assertIsInstance(embedding, list)
        self.assertTrue(len(embedding) > 0)
        self.assertTrue(all(isinstance(x, float) for x in embedding))

    def test_encode_exceeds_max_tokens(self):
        # Costruiamo una stringa che sicuramente eccede i token massimi (es. > 2048 token)
        long_text = "This is a line of the smart contract. " * 1000  # Ripetizione = ~10k token

        with self.assertRaises(Exception):
            embedding = self.embedding_model.encode(long_text)

    def test_encode_empty_input(self):
        text = ""
        embedding = self.embedding_model.encode(text)
        self.assertIsInstance(embedding, list)
        self.assertTrue(len(embedding) > 0)  # Il modello dovrebbe comunque restituire un embedding valido
