import unittest
from unittest.mock import patch
from cli.comands import ModelListCommand


class TestModelListCommand(unittest.TestCase):
    @patch("cli.comands.ConfigManager")
    def test_execute_models_present(self, mock_config):
        """
        Verifica che vengano stampati i modelli presenti nella configurazione.
        """
        mock_config.return_value.get_all_models.return_value = [
            {"model_name": "gpt-4", "source": "openai"},
            {"model_name": "llama", "source": "huggingface"}
        ]

        cmd = ModelListCommand()

        with patch("builtins.print") as mock_print:
            cmd.execute()
            mock_print.assert_any_call("Model name: gpt-4 -> from: openai")
            mock_print.assert_any_call("Model name: llama -> from: huggingface")

    @patch("cli.comands.ConfigManager")
    def test_execute_no_models(self, mock_config):
        """
        Verifica che il comando funzioni correttamente anche quando non ci sono modelli salvati.
        """
        mock_config.return_value.get_all_models.return_value = []

        cmd = ModelListCommand()

        with patch("builtins.print") as mock_print:
            cmd.execute()
            mock_print.assert_not_called()  # oppure: puoi controllare un messaggio vuoto


if __name__ == "__main__":
    unittest.main()
