import unittest
from unittest.mock import patch, MagicMock
from cli.invoker import CLIInvoker
from cli.comands import SetModelCommand


class TestIntegrationCLIInvokerSetModelCommand(unittest.TestCase):

    @patch("cli.comands.ConfigManager")
    @patch("cli.comands.LLMFactory.build")
    def test_set_model_valid_openai(self, mock_build, mock_config):
        """
        Test T1: Source = openai, tutti i parametri presenti.
        Verifica che il modello venga costruito e salvato nella configurazione.
        """
        mock_build.return_value = MagicMock()

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

        mock_build.assert_called_once()
        mock_config.return_value.add_model_config.assert_called_once()

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
        cli.set_command(args)

        with self.assertRaises(ValueError):
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
        cli.set_command(args)

        with self.assertRaises(ValueError):
            cli.run_command()

    @patch("cli.comands.LLMFactory.build")
    def test_set_model_valid_huggingface(self, mock_build):
        """
        Test T5 variante: Source = huggingface, parametri opzionali assenti.
        """
        mock_build.return_value = MagicMock()

        args = [
            "set-model",
            "--model_name", "sshleifer/tiny-gpt2",
            "--source", "huggingface"
        ]
        cli = CLIInvoker()
        cli.set_command(args)
        cli.run_command()

        mock_build.assert_called_once()

    @patch("cli.comands.LLMFactory.build")
    def test_set_model_valid_huggingface2(self, mock_build):
        """
        Test T5: Source = huggingface, parametri opzionali presenti e validi.
        """

        mock_build.return_value = MagicMock()

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

        mock_build.assert_called_once()


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
