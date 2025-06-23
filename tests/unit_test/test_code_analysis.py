import unittest
from unittest.mock import MagicMock, patch
from src.analysis_module.code_analysis import CodeAnalysis  # adatta l'import se il path è diverso

class TestCodeAnalysis(unittest.TestCase):
    def setUp(self):
        # Mock LLMModel
        self.mock_llm = MagicMock()
        self.mock_llm.generate = MagicMock()
        # Patch load_string globally for each test
        self.patcher = patch('src.analysis_module.code_analysis.load_string', return_value="Prompt di esempio")
        self.mock_load_string = self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_init_successful(self):
        analysis = CodeAnalysis(llm_model=self.mock_llm)
        self.assertEqual(analysis.prompt, "Prompt di esempio")
        self.assertEqual(analysis.llm_model, self.mock_llm)

    def test_init_failure(self):
        self.patcher.stop()  # interrompo patch attuale
        with patch('src.analysis_module.code_analysis.load_string', side_effect=Exception("Errore")):
            with self.assertRaises(RuntimeError):
                CodeAnalysis(llm_model=self.mock_llm)

    def test_get_possible_vulns_success(self):
        response = "```list\n[\"arbitrary delete\", \"rekey to\"]\n```"
        self.mock_llm.generate.return_value = response
        analysis = CodeAnalysis(llm_model=self.mock_llm)
        vulns = analysis.get_possible_vulns("some code")
        self.assertEqual(vulns, ["arbitrary delete", "rekey to"])
        self.mock_llm.generate.assert_called_once()

    def test_get_possible_vulns_generation_error(self):
        self.mock_llm.generate.side_effect = Exception("LLM failure")
        analysis = CodeAnalysis(llm_model=self.mock_llm)
        vulns = analysis.get_possible_vulns("some code")
        self.assertEqual(vulns, [])

    def test_get_possible_vulns_parse_error(self):
        # Missing ```list section or invalid JSON
        self.mock_llm.generate.return_value = "```list\nnot a json```"
        analysis = CodeAnalysis(llm_model=self.mock_llm)
        vulns = analysis.get_possible_vulns("some code")
        self.assertEqual(vulns, [])

    def test_parse_response_success(self):
        analysis = CodeAnalysis(llm_model=self.mock_llm)
        response = "```list\n[\"arbitrary delete\", \"rekey to\"]\n```"
        result = analysis._parse_response(response)
        self.assertEqual(result, ["arbitrary delete", "rekey to"])

    def test_parse_response_missing_section(self):
        analysis = CodeAnalysis(llm_model=self.mock_llm)
        response = "no list here"
        result = analysis._parse_response(response)
        self.assertEqual(result, [])

    def test_parse_response_json_error(self):
        analysis = CodeAnalysis(llm_model=self.mock_llm)
        response = "```list\ninvalid json\n```"
        result = analysis._parse_response(response)
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()
