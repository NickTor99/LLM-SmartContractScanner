import unittest
from cli.invoker import CLIInvoker
from cli.comands import RunCommand, SetModelCommand, ModelListCommand


class TestCLIInvoker(unittest.TestCase):

    def test_set_command_run(self):
        """
        Verifica che il comando 'run' venga associato correttamente a RunCommand.
        """
        args = [
            "run",
            "--filepath", "contract.teal",
            "--model", "gpt-4",
            "--vuln-limit", "2",
            "--contract-limit", "3"
        ]
        cli = CLIInvoker()
        cli.set_command(args)
        self.assertIsInstance(cli.command, RunCommand)

    def test_set_command_set_model(self):
        """
        Verifica che il comando 'set-model' venga associato a SetModelCommand.
        """
        args = [
            "set-model",
            "--model_name", "gpt-4",
            "--source", "openai",
            "--api_key", "sk-test"
        ]
        cli = CLIInvoker()
        cli.set_command(args)
        self.assertIsInstance(cli.command, SetModelCommand)

    def test_set_command_model_list(self):
        """
        Verifica che il comando 'model-list' venga associato a ModelListCommand.
        """
        args = ["model-list"]
        cli = CLIInvoker()
        cli.set_command(args)
        self.assertIsInstance(cli.command, ModelListCommand)

    def test_set_command_invalid(self):
        """
        Verifica che un comando non riconosciuto generi un errore di parsing (SystemExit).
        """
        cli = CLIInvoker()
        with self.assertRaises(SystemExit):
            cli.set_command(["invalid-command"])

    def test_set_command_missing_arguments(self):
        """
        Verifica che l'assenza di argomenti obbligatori generi SystemExit.
        """
        cli = CLIInvoker()
        with self.assertRaises(SystemExit):
            cli.set_command(["run", "--model", "gpt-4"])


if __name__ == "__main__":
    unittest.main()
