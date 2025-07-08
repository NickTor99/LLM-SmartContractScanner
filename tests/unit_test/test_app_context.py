import unittest
from unittest.mock import patch, MagicMock
from configuration.context import AppContext

class TestAppContext(unittest.TestCase):
    @patch("configuration.context.ConfigManager")
    @patch("configuration.context.LLMFactory")
    @patch("configuration.context.CodeAnalysis")
    @patch("configuration.context.VulnAnalysis")
    @patch("configuration.context.CodeDescriptor")
    @patch("configuration.context.EmbeddingModel")
    @patch("configuration.context.RetrievalEngine")
    def test_appcontext_initialization_success(
            self, mock_retrieval, mock_embedder, mock_descriptor,
            mock_vuln, mock_code, mock_factory, mock_config
    ):
        """
        Verifica che tutti i componenti dell'AppContext vengano inizializzati correttamente.
        """
        # Mock ConfigManager
        mock_config_instance = MagicMock()
        mock_config_instance.load_config.return_value = {
            "llm": {"source": "openai", "model_name": "gpt-4", "api_key": "key"},
            "embedding_model_name": "model",
            "embedder_model_device": "cpu",
            "server_api_url": "http://fake.url"
        }
        mock_config.return_value = mock_config_instance

        mock_llm = MagicMock()
        mock_factory.build.return_value = mock_llm

        # Inizializza AppContext
        context = AppContext(model="gpt-4", vuln_limit=1, contract_limit=2)

        # Verifiche sullo stato osservabile
        self.assertEqual(context.llm, mock_llm)
        mock_factory.build.assert_called_once()
        mock_code.assert_called_once()
        mock_vuln.assert_called_once()
        mock_descriptor.assert_called_once()
        mock_embedder.assert_called_once()
        mock_retrieval.assert_called_once()

    @patch("configuration.context.ConfigManager")
    def test_model_not_found_in_config(self, mock_config):
        """
        Verifica che venga sollevata un'eccezione se il modello non è presente nella configurazione.
        """
        mock_config_instance = MagicMock()
        mock_config_instance.load_config.side_effect = ValueError("Modello non trovato")
        mock_config.return_value = mock_config_instance

        with self.assertRaises(ValueError):
            AppContext(model="unknown", vuln_limit=1, contract_limit=2)
