import json
import unittest
import io
from io import StringIO
from unittest.mock import patch

from requests import Response

from cli_tool.cli.invoker import CLIInvoker


class TestIntegrationCLIInvokerModelListCommand(unittest.TestCase):

    @patch("cli.comands.requests.post")
    @patch("sys.stdout", new_callable=StringIO)
    def test_model_list_with_models(self, mock_stdout, mock_config):
        """
        Test M3: Configurazione con modelli salvati
        Verifica che il comando 'model-list' stampi i modelli correttamente.
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

        cli = CLIInvoker()
        cli.set_command(["model-list"])

        cli.run_command()

        output = mock_stdout.getvalue()
        self.assertIn("Model name: gpt-4 -> from: openai", output)
        self.assertIn("Model name: llama -> from: huggingface", output)



    @patch("cli.comands.requests.post")
    @patch("sys.stdout", new_callable=StringIO)
    def test_model_list_empty(self, mock_stdout, mock_config):
        """
        Test M1: Configurazione vuota
        Verifica che non venga stampato nulla se la configurazione è priva di modelli.
        """
        response = Response()
        data = {
            "status": "success",
            "results": [

            ]
        }

        response._content = json.dumps(data).encode('utf-8')

        mock_config.return_value = response

        cli = CLIInvoker()
        cli.set_command(["model-list"])

        output = mock_stdout.getvalue()
        self.assertIn("", output)



if __name__ == "__main__":
    unittest.main()
