import unittest
from unittest.mock import patch, MagicMock
from cli.comands import SetModelCommand


class TestSetModelCommand(unittest.TestCase):
    @patch("cli.comands.ConfigManager")
    @patch("cli.comands.LLMFactory.build")
    def test_execute_valid_model(self, mock_build, mock_config):
        """
        Verifica che un modello valido venga costruito e salvato correttamente.
        """
        mock_build.return_value = MagicMock()  # modello costruito correttamente

        cmd = SetModelCommand(
            model_name="gpt-4",
            source="openai",
            api_key="sk-test",
            base_url="https://api.openai.com"
        )
        cmd.execute()

        mock_build.assert_called_once()
        mock_config.return_value.add_model_config.assert_called_once()

    @patch("cli.comands.LLMFactory.build")
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

    @patch("cli.comands.ConfigManager")
    @patch("cli.comands.LLMFactory.build")
    def test_execute_missing_optional_params(self, mock_build, mock_config):
        """
        Verifica che il comando funzioni anche senza api_key e base_url (opzionali).
        """
        mock_build.return_value = MagicMock()
        cmd = SetModelCommand(
            model_name="llama",
            source="huggingface"
        )
        cmd.execute()
        mock_build.assert_called_once()
        mock_config.return_value.add_model_config.assert_called_once()


    @patch("cli.comands.ConfigManager")
    @patch("cli.comands.LLMFactory.build")
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

    @patch("cli.comands.ConfigManager")
    @patch("cli.comands.LLMFactory.build")
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

    @patch("cli.comands.ConfigManager")
    @patch("cli.comands.LLMFactory.build")
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

    @patch("cli.comands.ConfigManager")
    @patch("cli.comands.LLMFactory.build")
    def test_execute_missing_api_key_baseurl(self, mock_build, mock_config):
        """
        Verifica che un modello valido venga costruito e salvato correttamente.
        """
        mock_build.return_value = MagicMock()  # modello costruito correttamente

        cmd = SetModelCommand(
            model_name="gpt-4",
            source="huggingface",
            api_key="",
            base_url=""
        )
        cmd.execute()

        mock_build.assert_called_once()
        mock_config.return_value.add_model_config.assert_called_once()

    @patch("cli.comands.ConfigManager")
    @patch("cli.comands.LLMFactory.build")
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



    @patch("cli.comands.ConfigManager")
    @patch("cli.comands.LLMFactory.build")
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
