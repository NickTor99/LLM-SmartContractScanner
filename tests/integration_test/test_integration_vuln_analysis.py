import json
import unittest
from unittest.mock import MagicMock, patch, mock_open
from src.analysis_module.vuln_analysis import VulnAnalysis


class TestCodeAnalysisIntegration(unittest.TestCase):
    def setUp(self):
        self.llm = MagicMock()
        self.analyzer = VulnAnalysis(llm_model=self.llm)

    @patch("src.analysis_module.vuln_analysis.load_string", return_value="System Prompt")
    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps({
        "vulnerabilities": [{
            "name": "example_vuln",
            "description": "descrizione",
            "attack_scenario": "scenario",
            "precondition": "condizione"
        }]
    }))
    def test_code_analysis_success(self, mock_file, mock_load_string):
        code = "def foo(): pass"
        vuln = "example_vuln"
        self.llm.generate.return_value = "il contratto è vulnerabile..."
        result = self.analyzer.get_vuln_analysis(code=code, vuln=vuln)
        self.assertIsInstance(result, str)

    @patch("src.analysis_module.vuln_analysis.load_string", return_value="System Prompt")
    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps({
        "vulnerabilities": [{
            "name": "example_vuln",
            "description": "descrizione",
            "attack_scenario": "scenario",
            "precondition": "condizione"
        }]
    }))
    def test_code_analysis_llm_failure(self, mock_file, mock_load_string):
        code = "contract code"
        vuln = "example_vuln"
        self.llm.generate.side_effect = Exception("LLM crashed")
        with self.assertRaises(Exception):
            result = self.analyzer.get_vuln_analysis(code=code, vuln=vuln)


if __name__ == "__main__":
    unittest.main()