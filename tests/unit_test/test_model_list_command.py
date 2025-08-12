import json
import unittest
from unittest.mock import patch

from requests import Response

from cli.comands import ModelListCommand


class TestModelListCommand(unittest.TestCase):
    @patch("cli.comands.requests.post")
    def test_execute_models_present(self, mock_config):
        """
        Verifica che vengano stampati i modelli presenti nella configurazione.
        """
        response = Response()
        data = {
            "status": "success",
            "results": [
                "Model name: gpt-4 -> from: openai",
                "Model name: llama -> from: huggingface"
            ]
        }

        response._content = json.dumps(data).encode('utf-8')

        mock_config.return_value = response

        cmd = ModelListCommand()

        with patch("builtins.print") as mock_print:
            cmd.execute()
            mock_print.assert_any_call("Model name: gpt-4 -> from: openai")
            mock_print.assert_any_call("Model name: llama -> from: huggingface")

    @patch("cli.comands.requests.post")
    def test_execute_no_models(self, mock_config):
        """
        Verifica che il comando funzioni correttamente anche quando non ci sono modelli salvati.
        """
        response = Response()
        data = {
            "status": "success",
            "results": []
        }

        response._content = json.dumps(data).encode('utf-8')

        mock_config.return_value = response

        cmd = ModelListCommand()

        with patch("builtins.print") as mock_print:
            cmd.execute()
            mock_print.assert_not_called()  # oppure: puoi controllare un messaggio vuoto


if __name__ == "__main__":
    unittest.main()
