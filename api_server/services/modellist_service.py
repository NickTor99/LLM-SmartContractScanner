from core.configuration.config_manager import ConfigManager


class ModelListService:
    def execute_run(self):
        try:
            config = ConfigManager()
            results = []
            for model in config.get_all_models():
                results.append(f"Model name: {model['model_name']} -> from: {model['source']}")
        except Exception as e:
            return {
                "status": "fail",
                "results": f"{e}",
            }

        return {
            "status": "success",
            "results": results,
        }
