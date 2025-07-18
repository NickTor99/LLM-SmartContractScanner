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
            "--contract-limit", "3",
            "--out", 'report',

        ]
        cli = CLIInvoker()
        cli.set_command(args)
        self.assertIsInstance(cli.command, RunCommand)

    def test_set_command_run_missing(self):
        args = [
            "run",
            "--model", "gpt-4",
            "--vuln-limit", "2",
            "--contract-limit", "3"
        ]
        cli = CLIInvoker()
        with self.assertRaises(SystemExit):
            cli.set_command(args)

        args = [
            "run",
            "--filepath", "contract.teal",
            "--model", "gpt-4",
            "--contract-limit", "3"
        ]
        cli.set_command(args)
        self.assertIsInstance(cli.command, RunCommand)

        args = [
            "run",
            "--filepath", "contract.teal",
            "--model", "gpt-4",
            "--vuln-limit", "2"
        ]
        cli.set_command(args)
        self.assertIsInstance(cli.command, RunCommand)

        args = [
            "run",
            "--filepath", "contract.teal",
            "--vuln-limit", "2",
            "--contract-limit", "3"
        ]
        cli = CLIInvoker()
        with self.assertRaises(SystemExit):
            cli.set_command(args)

    def test_set_command_set_model(self):
        """
        Verifica che il comando 'set-model' venga associato a SetModelCommand.
        """
        args = [
            "set-model",
            "--model_name", "gpt-4",
            "--source", "openai",
            "--api_key", "sk-test",
            "--base_url", "url_test"
        ]
        cli = CLIInvoker()
        cli.set_command(args)
        self.assertIsInstance(cli.command, SetModelCommand)

    def test_set_command_set_model_missing(self):
        """
        Verifica che il comando 'set-model' venga associato a SetModelCommand.
        """
        args = [
            "set-model",
            "--source", "openai",
            "--api_key", "sk-test"
        ]
        cli = CLIInvoker()
        with self.assertRaises(SystemExit):
            cli.set_command(args)

        args = [
            "set-model",
            "--model_name", "gpt-4",
            "--api_key", "sk-test"
        ]
        with self.assertRaises(SystemExit):
            cli.set_command(args)

        args = [
            "set-model",
            "--model_name", "gpt-4",
            "--source", "openai"
        ]
        with self.assertRaises(ValueError):
            cli.set_command(args)

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



    # Change Request 2: Report output

    def test_run_missing_out_param(self):
        """
        C13: run senza --out => Inizializzazione valida (parametro opzionale)
        """
        cli = CLIInvoker()
        args = [
            "run",
            "--filepath", "contract.teal",
            "--model", "gpt-4",
            "--vuln-limit", "1",
            "--contract-limit", "2"
        ]

        cli.set_command(args)

    def test_run_invalid_out_param(self):
        """
        C14: run con valore di --out non valido => Errore: il valore di --out non deve contenere caratteri speciali
        """
        cli = CLIInvoker()
        args = [
            "run",
            "--filepath", "contract.teal",
            "--model", "gpt-4",
            "--vuln-limit", "1",
            "--contract-limit", "2",
            "--out", "<report>"
        ]

        with self.assertRaises(SystemExit):
            cli.set_command(args)


if __name__ == "__main__":
    unittest.main()
