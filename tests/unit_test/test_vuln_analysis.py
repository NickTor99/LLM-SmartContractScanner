import unittest
from unittest.mock import patch, MagicMock, mock_open
import json

from src.analysis_module.vuln_analysis import VulnAnalysis  # Adatta al tuo path

class TestVulnAnalysis(unittest.TestCase):

    def setUp(self):
        self.mock_llm = MagicMock()
        self.vuln_analysis = VulnAnalysis(llm_model=self.mock_llm)

        self.vuln_name = "example_vuln"
        self.code = "some pyteal code"
        self.vuln_details = {
            "name": self.vuln_name,
            "description": "descrizione",
            "attack_scenario": "scenario",
            "precondition": "condizione"
        }

        self.vuln_file_data = {
            "vulnerabilities": [self.vuln_details]
        }

    @patch("src.analysis_module.vuln_analysis.load_string", return_value="System Prompt")
    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps({
        "vulnerabilities": [{
            "name": "example_vuln",
            "description": "descrizione",
            "attack_scenario": "scenario",
            "precondition": "condizione"
        }]
    }))
    def test_get_vuln_analysis_success(self, mock_file, mock_load_string):
        self.mock_llm.generate.return_value = "LLM response"
        result = self.vuln_analysis.get_vuln_analysis(self.vuln_name, self.code)

        self.assertEqual(result, "LLM response")
        self.mock_llm.generate.assert_called_once()

    @patch("src.analysis_module.vuln_analysis.load_string", return_value="System Prompt")
    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps({
        "vulnerabilities": [{
            "name": "example_vuln",
            "description": "descrizione",
            "attack_scenario": "scenario",
            "precondition": "condizione"
        }]
    }))
    def test_get_vuln_analysis_empty_code(self, mock_file, mock_load_string):
        self.mock_llm.generate.return_value = "LLM response"

        with self.assertRaises(Exception):
            result = self.vuln_analysis.get_vuln_analysis(self.vuln_name, "")

    @patch("builtins.open", new_callable=mock_open, read_data="not valid json")
    def test_get_vuln_analysis_json_decode_error(self, mock_file):
        result = self.vuln_analysis.get_vuln_analysis(self.vuln_name, self.code)
        self.assertIn("Errore: Impossibile caricare", result)

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_get_vuln_analysis_file_not_found(self, mock_file):
        result = self.vuln_analysis.get_vuln_analysis(self.vuln_name, self.code)
        self.assertIn("Errore: Impossibile caricare", result)

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps({"vulnerabilities": []}))
    def test_get_vuln_analysis_key_error(self, mock_file):
        result = self.vuln_analysis.get_vuln_analysis(self.vuln_name, self.code)
        self.assertIn("Errore: Dettagli incompleti", result)

    @patch("src.analysis_module.vuln_analysis.load_string", return_value="System Prompt")
    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps({
        "vulnerabilities": [{
            "name": "example_vuln",
            "description": "descrizione"
            # manca "attack_scenario" e "precondition"
        }]
    }))
    def test_get_vuln_analysis_missing_detail_field(self, mock_file, mock_load_string):
        # manca attack_scenario e precondition -> KeyError in _get_prompt
        result = self.vuln_analysis.get_vuln_analysis(self.vuln_name, self.code)
        self.assertIn("Errore: Dettagli incompleti", result)

    def test_get_prompt_structure(self):
        # Test diretto su _get_prompt
        details = {
            "description": "desc",
            "attack_scenario": "scenario",
            "precondition": "precondizione"
        }
        with patch("src.analysis_module.vuln_analysis.load_string", return_value="System Prompt"):
            prompt = self.vuln_analysis._get_prompt("example", details, "code")
            self.assertIn("System Prompt", prompt)
            self.assertIn("desc", prompt)
            self.assertIn("scenario", prompt)
            self.assertIn("precondizione", prompt)
            self.assertIn("code", prompt)

if __name__ == '__main__':
    unittest.main()
