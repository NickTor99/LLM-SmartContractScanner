import unittest
from unittest.mock import patch
from cli.invoker import CLIInvoker
from cli.comands import ModelListCommand


class TestIntegrationCLIInvokerModelListCommand(unittest.TestCase):

    @patch("cli.comands.ConfigManager")
    def test_model_list_with_models(self, mock_config):
        """
        Test M3: Configurazione con modelli salvati
        Verifica che il comando 'model-list' stampi i modelli correttamente.
        """
        mock_config.return_value.get_all_models.return_value = [
            {"model_name": "gpt-4", "source": "openai"},
            {"model_name": "llama", "source": "huggingface"}
        ]

        cli = CLIInvoker()
        cli.set_command(["model-list"])

        with patch("builtins.print") as mock_print:
            cli.run_command()

            mock_print.assert_any_call("Model name: gpt-4 -> from: openai")
            mock_print.assert_any_call("Model name: llama -> from: huggingface")

    @patch("cli.comands.ConfigManager")
    def test_model_list_empty(self, mock_config):
        """
        Test M1: Configurazione vuota
        Verifica che non venga stampato nulla se la configurazione è priva di modelli.
        """
        mock_config.return_value.get_all_models.return_value = []

        cli = CLIInvoker()
        cli.set_command(["model-list"])

        with patch("builtins.print") as mock_print:
            cli.run_command()
            mock_print.assert_not_called()  # Nessun modello, nessuna stampa

    @patch("cli.comands.ConfigManager")
    def test_model_list_with_models(self, mock_config):
        """
        Test M2: Configurazione con un solo modello salvati
        Verifica che il comando 'model-list' stampi i modelli correttamente.
        """
        mock_config.return_value.get_all_models.return_value = [
            {"model_name": "gpt-4", "source": "openai"}
        ]

        cli = CLIInvoker()
        cli.set_command(["model-list"])

        with patch("builtins.print") as mock_print:
            cli.run_command()

            mock_print.assert_any_call("Model name: gpt-4 -> from: openai")

if __name__ == "__main__":
    unittest.main()
