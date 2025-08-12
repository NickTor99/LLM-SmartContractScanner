import unittest
from unittest.mock import MagicMock, patch
from api_server.core.analysis_package.code_analysis import CodeAnalysis


class TestCodeAnalysisIntegration(unittest.TestCase):
    @patch("api_server.core.analysis_package.code_analysis.load_string", return_value="Descrivi il seguente codice:")
    def setUp(self, mock):
        self.llm = MagicMock()
        self.analyzer = CodeAnalysis(llm_model=self.llm)

    def test_code_analysis_success(self):
        code = "def foo(): pass"
        self.llm.generate.return_value = "```list\n[\"arbitrary delete\", \"rekey to\"]\n```"
        result = self.analyzer.get_possible_vulns(code)
        self.assertIsInstance(result, list)

    def test_code_analysis_llm_failure(self):
        code = "contract code"
        self.llm.generate.side_effect = Exception("LLM crashed")
        result = self.analyzer.get_possible_vulns(code)
        self.assertEqual(result, [])

if __name__ == "__main__":
    unittest.main()
