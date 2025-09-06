import unittest
from unittest.mock import patch, MagicMock
from services.modellist_service import ModelListService


class TestGetModelsService(unittest.TestCase):

    @patch("services.modellist_service.ConfigManager.get_all_models")
    def test_SSe1_successful_retrieval(self, mock_get_models):
        # Arrange
        mock_get_models.return_value = [{'model_name': "gpt-4", 'source': 'openai'}]
        service = ModelListService()

        # Act
        result = service.execute()

        # Assert
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["results"], ['Model name: gpt-4 -> from: openai'])

    @patch("services.modellist_service.ConfigManager.get_all_models")
    def test_SSe2_retrieval_raises_exception(self, mock_get_models):
        # Arrange
        mock_get_models.side_effect = Exception("Errore nel recupero modelli")
        service = ModelListService()

        # Act
        result = service.execute()

        # Assert
        self.assertEqual(result["status"], "fail")
        self.assertIn("Errore nel recupero modelli", result["results"])


if __name__ == "__main__":
    unittest.main()
