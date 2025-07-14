import unittest
from unittest.mock import mock_open, patch
from report.html_report_generator import HTMLReportGenerator


class TestHTMLReportGenerator(unittest.TestCase):

    def setUp(self):
        self.generator = HTMLReportGenerator()

    @patch("builtins.open", new_callable=mock_open)
    def test_generate_valid_report(self, mock_file):
        """
        RG1: Lista ben formata, percorso valido, nome non specificato
        """
        data = [{"vulnerability": "SQL Injection", "analysis": "Severe flaw"}]
        self.generator.generate(data, file_path="out/test.teal", report_name=None)
        self.assertTrue(mock_file.called)

    @patch("builtins.open", new_callable=mock_open)
    def test_generate_empty_list(self, mock_file):
        """
        RG2: Lista vuota, percorso valido, nome non specificato
        """
        data = []
        self.generator.generate(data, file_path="out/test.teal", report_name=None)
        mock_file().write.assert_any_call("Nessuna vulnerabilità rilevata.\n")

    def test_generate_malformed_data(self):
        """
        RG3: Lista malformata
        """
        malformed_data = [{"invalid_key": "no vuln"}]
        with self.assertRaises(Exception):
            self.generator.generate(malformed_data, file_path="out/test.teal", report_name=None)

    @patch("builtins.open", new_callable=mock_open)
    def test_generate_partial_data(self, mock_file):
        """
        RG4: Lista con dati parziali, percorso valido, nome valido
        """
        partial_data = [{"vulnerability": "XSS", "analysis": None}]
        self.generator.generate(partial_data, file_path="out/test.teal", report_name="partial")
        self.assertTrue(mock_file.called)

    @patch("builtins.open", new_callable=mock_open)
    def test_generate_empty_path(self, mock_file):
        """
        RG5: Percorso vuoto, nome valido
        """
        valid_data = [{"vulnerability": "DoS", "analysis": "Detected"}]
        self.generator.generate(valid_data, file_path="", report_name="fromname")
        self.assertTrue(mock_file.called)

    @patch("builtins.open", side_effect=OSError("Invalid path"))
    def test_generate_invalid_path(self, mock_file):
        """
        RG6: Percorso non valido
        """
        valid_data = [{"vulnerability": "DoS", "analysis": "Detected"}]
        with self.assertRaises(OSError):
            self.generator.generate(valid_data, file_path="invalid///path.teal", report_name="fail")

    @patch("builtins.open", new_callable=mock_open)
    def test_generate_existing_report_name(self, mock_file):
        """
        RG7: Nome report già esistente (simulato)
        """
        valid_data = [{"vulnerability": "RCE", "analysis": "critical"}]
        self.generator.generate(valid_data, file_path="out/test.teal", report_name="existing_report")
        self.assertTrue(mock_file.called)


if __name__ == "__main__":
    unittest.main()
