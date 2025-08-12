import json
import unittest
from io import StringIO
from unittest.mock import patch, MagicMock

from requests import Response

from cli.comands import SetModelCommand


class TestSetModelCommand(unittest.TestCase):

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
    def test_execute_valid_model(self, mock_stdout, mock_config):
        """
        Verifica che un modello valido venga costruito e salvato correttamente.
        """
        mock_config.return_value = self.response # modello costruito correttamente

        cmd = SetModelCommand(
            model_name="gpt-4",
            source="openai",
            api_key="sk-test",
            base_url="https://api.openai.com"
        )
        cmd.execute()

        output = mock_stdout.getvalue()
        self.assertIn("Modello impostato", output)

    @patch("cli.comands.requests.post")
    def test_execute_invalid_source(self, mock_build):
        """
        Verifica che venga gestato correttamente un errore da LLMFactory.build().
        """
        mock_build.side_effect = ValueError("Fonte del modello LLM non supportata: invalid")

        cmd = SetModelCommand(
            model_name="invalid-model",
            source="invalid"
        )

        with self.assertRaises(ValueError):
            cmd.execute()

    @patch("cli.comands.requests.post")
    @patch("sys.stdout", new_callable=StringIO)
    def test_execute_missing_optional_params(self, mock_stdout, mock_config):
        """
        Verifica che il comando funzioni anche senza api_key e base_url (opzionali).
        """
        mock_config.return_value = self.response
        cmd = SetModelCommand(
            model_name="llama",
            source="huggingface"
        )
        cmd.execute()
        output = mock_stdout.getvalue()
        self.assertIn("Modello impostato", output)

    @patch("cli.comands.requests.post")
    @patch("sys.stdout", new_callable=StringIO)
    def test_execute_missing_model_name(self, mock_build, mock_config):
        """
        Verifica che venga sollevato un errore se il nome del modello è mancante.
        """
        mock_build.return_value = MagicMock()
        mock_config.side_effect=ValueError()
        cmd = SetModelCommand(
            model_name="",
            source="openai",
            api_key="sk-test",
            base_url="https://api.openai.com"

        )

        with self.assertRaises(ValueError):
            cmd.execute()

    @patch("cli.comands.requests.post")
    @patch("sys.stdout", new_callable=StringIO)
    def test_execute_invalid_parameter(self, mock_build, mock_config):
        """
        Verifica che venga sollevato un errore se la sorgente non è valida.
        """
        mock_build.return_value = MagicMock()
        mock_config.side_effect=ValueError()
        cmd = SetModelCommand(
            model_name="llama",
            source="non_valida",
            api_key="non valida",
            base_url="non valida"

        )

        with self.assertRaises(ValueError):
            cmd.execute()

    @patch("cli.comands.requests.post")
    @patch("sys.stdout", new_callable=StringIO)
    def test_execute_missing_api_key(self, mock_build, mock_config):
        """
        Verifica che venga sollevato un errore se manca Api-Key.
        """
        mock_build.return_value = MagicMock()
        mock_config.side_effect=ValueError()
        cmd = SetModelCommand(
            model_name="llama",
            source="openai",
            api_key="",
            base_url="https://api.openai.com"

        )

        with self.assertRaises(ValueError):
            cmd.execute()

    @patch("cli.comands.requests.post")
    @patch("sys.stdout", new_callable=StringIO)
    def test_execute_missing_api_key_baseurl(self, mock_stdout, mock_build):
        """
        Verifica che un modello valido venga costruito e salvato correttamente.
        """
        mock_build.return_value = self.response  # modello costruito correttamente

        cmd = SetModelCommand(
            model_name="gpt-4",
            source="huggingface",
            api_key="",
            base_url=""
        )
        cmd.execute()

        output = mock_stdout.getvalue()
        self.assertIn("Modello impostato", output)

    @patch("cli.comands.requests.post")
    @patch("sys.stdout", new_callable=StringIO)
    def test_execute_missing_api_key(self, mock_build, mock_config):
        """
        Verifica che venga sollevato un errore se manca Api-Key.
        """
        mock_build.return_value = MagicMock()
        mock_config.side_effect=ValueError()
        cmd = SetModelCommand(
            model_name="llama",
            source="huggingface",
            api_key="",
            base_url="https://api.openai.com"

        )

        with self.assertRaises(ValueError):
            cmd.execute()



    @patch("cli.comands.requests.post")
    @patch("sys.stdout", new_callable=StringIO)
    def test_execute_missing_baseurl(self, mock_build, mock_config):
        """
        Verifica che venga sollevato un errore se manca baseurl.
        """
        mock_build.return_value = MagicMock()
        mock_config.side_effect=ValueError()
        cmd = SetModelCommand(
            model_name="llama",
            source="openai",
            api_key="sk-test",
            base_url=""

        )

        with self.assertRaises(ValueError):
            cmd.execute()

if __name__ == "__main__":
    unittest.main()
