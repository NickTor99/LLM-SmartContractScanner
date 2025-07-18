import unittest
from unittest.mock import patch, MagicMock
from cli.comands import RunCommand

class TestRunCommand(unittest.TestCase):
    @patch("cli.comands.run_pipeline")
    @patch("cli.comands.AppContext")
    def test_execute_success(self, mock_context, mock_pipeline):
        """
        Verifica che RunCommand invochi correttamente AppContext e run_pipeline.
        """
        mock_generator = MagicMock()
        mock_context_instance = MagicMock()
        mock_context_instance.get_report_generator.return_value = mock_generator

        mock_context.return_value = mock_context_instance


        cmd = RunCommand("deepseek-chat", "valid.teal", 2, 3, out="report")
        cmd.execute()
        mock_context.assert_called_once_with(model="deepseek-chat", vuln_limit=2, contract_limit=3)
        mock_pipeline.assert_called_once()
        mock_generator.generate.assert_called_once()

    @patch("cli.comands.run_pipeline")
    @patch("cli.comands.AppContext")
    def test_execute_model_missing(self, mock_context, mock_pipeline):
        """
        Verifica che RunCommand sollevi un errore se il modello non è disponibile nella config.
        """
        mock_context.side_effect = ValueError("Model not found")
        cmd = RunCommand("missing-model", "valid.teal", 2, 3, out=None)
        with self.assertRaises(ValueError):
            cmd.execute()

    @patch("cli.comands.run_pipeline")
    @patch("cli.comands.AppContext")
    def test_execute_filepath_missing(self, mock_context, mock_pipeline):
        """
        Verifica che RunCommand sollevi un errore se il file non è presente nel sistema.
        """
        mock_pipeline.side_effect = FileNotFoundError("File not found")
        cmd = RunCommand("deepseek-chat", "", 2, 3, out=None)
        with self.assertRaises(FileNotFoundError):
            cmd.execute()


    @patch("cli.comands.run_pipeline")
    @patch("cli.comands.AppContext")
    def test_execute_negative_limit(self, mock_context, mock_pipeline):
        """
        Verifica che RunCommand sollevi un errore se il modello non è disponibile nella config.
        """

        with self.assertRaises(ValueError):
            cmd = RunCommand("deepseek-chat", "valid.teal", -2, 3, out=None)
            cmd.execute()

        with self.assertRaises(ValueError):
            cmd = RunCommand("deepseek-chat", "valid.teal", 2, -3, out=None)
            cmd.execute()

    @patch("cli.comands.run_pipeline")
    @patch("cli.comands.AppContext")
    def test_execute_zero_limit(self, mock_context, mock_pipeline):
        """
        Verifica che RunCommand sollevi un errore se il modello non è disponibile nella config.
        """

        with self.assertRaises(ValueError):
            cmd = RunCommand("deepseek-chat", "valid.teal", 0, 0, out=None)
            cmd.execute()

    # Change Request 2: Report output

    @patch("cli.comands.run_pipeline")
    @patch("cli.comands.AppContext")
    def test_execute_with_out_path(self, mock_context, mock_pipeline):
        """
        RC7: out non specificato
        """
        mock_generator = MagicMock()
        mock_context_instance = MagicMock()
        mock_context_instance.get_report_generator.return_value = mock_generator

        mock_context.return_value = mock_context_instance


        cmd = RunCommand("deepseek-chat", "valid.teal", 2, 3, out=None)
        cmd.execute()
        mock_context.assert_called_once_with(model="deepseek-chat", vuln_limit=2, contract_limit=3)
        mock_pipeline.assert_called_once()
        mock_generator.generate.assert_called_once()

