import unittest
from unittest.mock import MagicMock, patch
from src.retrieval_module.code_descriptor import CodeDescriptor


class TestCodeDescriptor(unittest.TestCase):

    @patch("src.retrieval_module.code_descriptor.load_string", return_value="Descrivi il seguente codice:")
    def test_init_successful(self, mock_load_string):
        # Setup dello Stub LLM
        mock_llm = MagicMock()

        # Init
        descriptor = CodeDescriptor(mock_llm)

        # Verifica
        self.assertEqual(descriptor.prompt, "Descrivi il seguente codice:")
        self.assertEqual(descriptor.llm_model, mock_llm)

    @patch("src.retrieval_module.code_descriptor.load_string", side_effect=Exception("File non trovato"))
    def test_init_failure(self, mock_load_string):

        mock_llm = MagicMock()

        with self.assertRaises(RuntimeError) as context:
            CodeDescriptor(mock_llm)

        self.assertIn("Impossibile caricare il prompt per CodeDescriptor", str(context.exception))

    @patch("src.retrieval_module.code_descriptor.load_string", return_value="Prompt base")
    def test_get_description_successful(self, mock_load_string):
        mock_llm = MagicMock()
        mock_llm.generate.return_value = "Questa funzione somma due numeri."

        descriptor = CodeDescriptor(mock_llm)
        result = descriptor.get_description("def add(a, b): return a + b")

        self.assertEqual(result, "Questa funzione somma due numeri.")
        mock_llm.generate.assert_called_once()

    @patch("src.retrieval_module.code_descriptor.load_string", return_value="Prompt base")
    def test_get_description_failure(self, mock_load_string):
        mock_llm = MagicMock()
        mock_llm.generate.side_effect = Exception("Errore interno LLM")

        descriptor = CodeDescriptor(mock_llm)
        result = descriptor.get_description("def add(a, b): return a + b")

        self.assertEqual(result, "Errore nella generazione della descrizione")


if __name__ == "__main__":
    unittest.main()

