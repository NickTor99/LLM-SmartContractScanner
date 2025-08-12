import unittest
from unittest.mock import patch
from api.schemas import RunRequest
from services.run_service import RunService

class TestRunService(unittest.TestCase):

    @patch("services.run_service.run_pipeline")
    @patch("services.run_service.AppContext")
    def test_Rse1_successful_execution(self, mock_context, mock_run_pipeline):
        # Arrange
        mock_run_pipeline.return_value = {"data": "pipeline output"}
        service = RunService()
        request = RunRequest(
            model="gpt-4",
            source_code="codice valido",
            vuln_limit=5,
            contract_limit=2
        )

        # Act
        result = service.execute_run(request)

        # Assert
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["results"], {"data": "pipeline output"})

    @patch("services.run_service.run_pipeline")
    @patch("services.run_service.AppContext")
    def test_Rse2_execution_raises_exception(self, mock_context, mock_run_pipeline):
        # Arrange
        mock_run_pipeline.side_effect = Exception("Errore nel pipeline")
        service = RunService()
        request = RunRequest(
            model="gpt-4",
            source_code="codice non valido",
            vuln_limit=5,
            contract_limit=2
        )

        # Act
        result = service.execute_run(request)

        # Assert
        self.assertEqual(result["status"], "fail")
        self.assertIn("Errore nel pipeline", result["results"])


if __name__ == "__main__":
    unittest.main()
