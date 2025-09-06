import unittest
from unittest.mock import patch, MagicMock
from api.schemas import SetModelRequest
from services.setmodel_service import SetModelService


class TestSetModelService(unittest.TestCase):

    @patch("services.setmodel_service.ConfigManager")
    @patch("services.setmodel_service.LLMFactory")
    def test_SSe1_successful_save(self, mock_llm, mock_save_config):
        mock_save_config = MagicMock()
        mock_save_config.return_value = "modello impostato correttamente"
        service = SetModelService()
        request = SetModelRequest(
            source="openai",
            model_name="gpt-4",
            base_url="https://api.openai.com",
            api_key="fvdbfdbdfbfbfdbd"
        )

        # Act
        result = service.execute(request)

        print(result["results"])

        # Assert
        self.assertEqual(result["status"], "success")
        self.assertIn("Modello impostato", result["results"])

    @patch("services.setmodel_service.ConfigManager")
    @patch("services.setmodel_service.LLMFactory")
    def test_SSe2_save_raises_exception(self, mock_llm, mock_save_config):
        # Arrange
        mock_save_config.side_effect = Exception("Errore nel salvataggio del modello")
        service = SetModelService()
        request = SetModelRequest(
            source="openai",
            model_name="not-existent",
            base_url="",
            api_key=""
        )

        # Act
        result = service.execute(request)

        # Assert
        self.assertEqual(result["status"], "fail")
        self.assertIn("Errore nel salvataggio del modello", result["results"])


if __name__ == "__main__":
    unittest.main()
