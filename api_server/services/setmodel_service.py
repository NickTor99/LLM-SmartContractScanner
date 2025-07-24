from api_server.api.schemas import SetModelRequest
from api_server.core.configuration.config_manager import ConfigManager
from api_server.core.configuration.llm_factory import LLMFactory


class SetModelService:
    def execute_run(self, request: SetModelRequest):
        try:
            _ = LLMFactory.build(request.dict())
            config_manager = ConfigManager()
            config_manager.add_model_config(request.dict())
        except Exception as e:
            return {
                "status": "fail",
                "results": f"{e}",
            }

        return {
            "status": "success",
            "results": f"✅ Modello impostato: {request.model_name}",
        }
