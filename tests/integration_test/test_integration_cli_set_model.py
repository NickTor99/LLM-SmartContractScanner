import json
import unittest
from io import StringIO
from unittest.mock import patch, MagicMock

from requests import Response

from cli.invoker import CLIInvoker


class TestIntegrationCLIInvokerSetModelCommand(unittest.TestCase):

    def setUp(self):
        self.response = Response()
        data = {
            "status": "success",
            "results": "✅ Modello impostato: gpt-4"
        }

        self.response._content = json.dumps(data).encode('utf-8')

        self.response_fail = Response()
        data = {
            "status": "fail",
            "results": "errore"
        }

        self.response_fail._content = json.dumps(data).encode('utf-8')


    @patch("cli.comands.requests.post")
    @patch("sys.stdout", new_callable=StringIO)
    def test_set_model_valid_openai(self,  mock_stdout, mock_response):
        """
        Test T1: Source = openai, tutti i parametri presenti.
        Verifica che il modello venga costruito e salvato nella configurazione.
        """
        mock_response.return_value = self.response

        args = [
            "set-model",
            "--model_name", "gpt-4",
            "--source", "openai",
            "--api_key", "sk-test",
            "--base_url", "https://api.openai.com"
        ]
        cli = CLIInvoker()
        cli.set_command(args)
        cli.run_command()

        output = mock_stdout.getvalue()
        self.assertIn("Modello impostato", output)

    def test_set_model_valid_openai_missing_ApiKey(self):
        """
        Test T2: Source = openai, manca solo ApiKey.
        DA un Errore ApiKey Obbligatorio.
        """

        args = [
            "set-model",
            "--model_name", "gpt-4",
            "--source", "openai",
            "--base_url", "https://api.openai.com"
        ]
        cli = CLIInvoker()

        with self.assertRaises(ValueError):
            cli.set_command(args)
            cli.run_command()

    def test_set_model_valid_openai_missing_Base_URL(self):
        """
        Test T3: Source = openai, manca BaseURL.
        Da un errore BaseUrl obbligatorio.
        """

        args = [
            "set-model",
            "--model_name", "gpt-4",
            "--source", "openai",
            "--api_key", "sk-test"
        ]
        cli = CLIInvoker()

        with self.assertRaises(ValueError):
            cli.set_command(args)
            cli.run_command()

    @patch("cli.comands.requests.post")
    @patch("sys.stdout", new_callable=StringIO)
    def test_set_model_valid_huggingface(self, mock_stdout, mock_response):
        """
        Test T5 variante: Source = huggingface, parametri opzionali assenti.
        """
        mock_response.return_value = self.response

        args = [
            "set-model",
            "--model_name", "sshleifer/tiny-gpt2",
            "--source", "huggingface"
        ]
        cli = CLIInvoker()
        cli.set_command(args)
        cli.run_command()

        output = mock_stdout.getvalue()
        self.assertIn("Modello impostato", output)

    @patch("cli.comands.requests.post")
    @patch("sys.stdout", new_callable=StringIO)
    def test_set_model_valid_huggingface2(self, mock_stdout, mock_response):
        """
        Test T5: Source = huggingface, parametri opzionali presenti e validi.
        """

        mock_response.return_value = self.response

        args = [
            "set-model",
            "--model_name", "sshleifer/tiny-gpt2",
            "--source", "huggingface",
            "--api_key", "sk-test",
            "--base_url", "https://api.huggingface.com"
        ]
        cli = CLIInvoker()
        cli.set_command(args)
        cli.run_command()

        output = mock_stdout.getvalue()
        self.assertIn("Modello impostato", output)


    def test_set_model_invalid_source(self):
        """
        Test T5 variante: source non supportata.
        Verifica che venga sollevata un'eccezione da LLMFactory.
        """

        args = [
            "set-model",
            "--model_name", "fake-model",
            "--source", "invalid"
        ]
        cli = CLIInvoker()

        with self.assertRaises(SystemExit):
            cli.set_command(args)
            cli.run_command()


if __name__ == "__main__":
    unittest.main()
