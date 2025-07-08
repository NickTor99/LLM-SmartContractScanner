from abc import ABC, abstractmethod
from configuration.context import AppContext
from configuration.llm_factory import LLMFactory
from configuration.pipeline import run_pipeline
from configuration.config_manager import ConfigManager

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass


# ----- RunCommand -----
class RunCommand(Command):
    def __init__(self, model, path, vuln_limit, contract_limit):
        self.model = model
        self.path = path
        self.vuln_limit = vuln_limit
        self.contract_limit = contract_limit


    def execute(self):
        context = AppContext(model=self.model, vuln_limit=self.vuln_limit, contract_limit=self.contract_limit)
        run_pipeline(context=context, path=self.path)


# ----- SetModelCommand -----
class SetModelCommand(Command):
    def __init__(self, model_name, source, api_key=None, base_url=None):
        self.base_url = base_url
        self.api_key = api_key
        self.source = source
        self.model_name = model_name

    def execute(self):
        config = {
            "source": self.source,
            "model_name": self.model_name,
            "base_url": self.base_url,
            "api_key": self.api_key
        }
        try:
            llm = LLMFactory.build(config)
        except Exception as e:
            return

        config_manager = ConfigManager()
        config_manager.add_model_config(config)
        print(f"✅ Modello impostato: {self.model_name}")


class ModelListCommand(Command):
    def execute(self):
        config = ConfigManager()
        for model in config.get_all_models():
            print(f"Model name: {model['model_name']} -> from: {model['source']}")

