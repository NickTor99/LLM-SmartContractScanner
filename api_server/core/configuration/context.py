import logging
import os

from api_server.core.configuration.config_manager import ConfigManager
from api_server.core.configuration.llm_factory import LLMFactory
from api_server.core.analysis_package.code_analysis import CodeAnalysis
from api_server.core.retrieval_package.code_descriptor import CodeDescriptor
from api_server.core.retrieval_package.embedding_model import EmbeddingModel
from api_server.core.retrieval_package.retrieval_engine import RetrievalEngine
from api_server.core.analysis_package.vuln_analysis import VulnAnalysis

logger = logging.getLogger(__name__)
class AppContext:
    def __init__(self, model: str, vuln_limit: int, contract_limit: int):
        self.config_manager = ConfigManager()
        self.config = self.config_manager.load_config(model)
        self.config.update({"vuln_limit": vuln_limit})
        self.config.update({"contract_limit": contract_limit})
        self.llm = None
        self.code_analyzer = None
        self.vuln_analyzer = None
        self.retrieval_engine = None
        self._initialize()

    def _initialize(self):
        # 1. Costruisce il modello LLM
        self.llm = LLMFactory.build(self.config["llm"])

        logger.info(f"Modello {self.llm.model_name} impostato correttamente!")

        # 2. Inizializza i componenti con il modello e le configurazioni
        self.code_analyzer = CodeAnalysis(
            llm_model=self.llm,
            num_model=self.config.get("vuln_limit"))

        logger.info(f"Code Analyzer impostato correttamente!")

        code_descriptor = CodeDescriptor(llm_model=self.llm)

        embedder = EmbeddingModel(
            device=self.config.get("embedder_model_device"),
            model_name=self.config.get("embedding_model_name")
        )

        self.retrieval_engine = RetrievalEngine(
            url=f"{os.getenv('API_URL', 'http://localhost:8000')}{self.config.get('server_api_url')}",
            descriptor=code_descriptor,
            embedder=embedder,
            num_retrieve=self.config.get("contract_limit")
        )

        logger.info(f"Retrieval Engine impostato correttamente!")

        self.vuln_analyzer = VulnAnalysis(llm_model=self.llm)

        logger.info(f"Vuln Analyzer impostato correttamente!")


    def get_code_analyzer(self) -> CodeAnalysis:
        return self.code_analyzer

    def get_vuln_analyzer(self) -> VulnAnalysis:
        return self.vuln_analyzer

    def get_retrieval_engine(self) -> RetrievalEngine:
        return self.retrieval_engine


