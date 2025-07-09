import unittest
from unittest.mock import mock_open, patch, MagicMock
import json
from configuration.config_manager import ConfigManager


class TestConfigManager(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps({
        "llm": [
            {"model_name": "gpt-4", "source": "openai"}
        ]
    }))
    def test_load_config_model_present(self, mock_file):
        manager = ConfigManager()
        config = manager.load_config("gpt-4")
        self.assertEqual(config["llm"]["model_name"], "gpt-4")


    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps({
        "llm": []
    }))
    def test_load_config_model_absent(self, mock_file):
        manager = ConfigManager()
        with self.assertRaises(ValueError):
            manager.load_config("nonexistent")


    @patch("builtins.open", new_callable=mock_open)
    def test_save_config(self, mock_file):
        config_data = {
            "llm": [{"model_name": "gpt-4", "source": "openai"}]
        }
        manager = ConfigManager()
        manager.save_config(config_data)

        mock_file.assert_called_once_with("configuration/config.json", "w")
        handle = mock_file()
        handle.write.assert_called()


    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps({
        "llm": [{"model_name": "existing", "source": "openai"}]
    }))
    def test_add_model_config(self, mock_file):
        # Simula lettura e scrittura
        handle = mock_file()
        handle.write = MagicMock()
        manager = ConfigManager()
        new_model = {"model_name": "gpt-4", "source": "openai"}
        manager.add_model_config(new_model)

        self.assertTrue(handle.write.called)


    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps({
        "llm": [{"model_name": "gpt-4", "source": "openai"}]
    }))
    def test_get_all_models(self, mock_file):
        manager = ConfigManager()
        models = manager.get_all_models()
        self.assertEqual(len(models), 1)
        self.assertEqual(models[0]["model_name"], "gpt-4")


if __name__ == "__main__":
    unittest.main()
