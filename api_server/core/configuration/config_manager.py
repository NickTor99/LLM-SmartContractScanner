import json
import os


class ConfigManager:
    CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "config.json"))

    def __init__(self):
        if not os.path.exists(self.CONFIG_PATH):
            self._create_default_config()

    def _create_default_config(self):
        default_config = {
            "embedding_model_name": "hkunlp/instructor-xl",
            "embedding_device": "cpu",
            "embedding_instruction": "Represent the semantic behavior of the smart contract for similarity-based retrieval.",
            "llm": []
        }
        self.save_config(default_config)

    def load_config(self, model_name: str) -> dict:
        with open(self.CONFIG_PATH, "r") as f:
            config = json.load(f)

        # Cerca il modello richiesto
        llm_match = next((llm for llm in config.get("llm", []) if llm.get("model_name") == model_name), None)

        if llm_match is None:
            raise ValueError(f"Modello LLM '{model_name}' non trovato nella configurazione.")

        # Sovrascrive la lista con solo il modello selezionato
        config["llm"] = llm_match
        return config


    def save_config(self, config: dict):
        with open(self.CONFIG_PATH, "w") as f:
            json.dump(config, f, indent=4)

    def add_model_config(self, model_config: dict):
        with open(self.CONFIG_PATH, "r") as f:
            config = json.load(f)
        llm_list = config.get("llm", [])
        llm_list.append(model_config)
        config["llm"] = llm_list
        self.save_config(config)

    def get_all_models(self) -> list:
        with open(self.CONFIG_PATH, "r") as f:
            config = json.load(f)
        return config.get("llm", [])



