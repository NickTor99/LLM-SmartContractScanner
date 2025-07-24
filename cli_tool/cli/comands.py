import os
from abc import ABC, abstractmethod
from pathlib import Path
import requests

from report.html_report_generator import HTMLReportGenerator


class Command(ABC):
    @abstractmethod
    def execute(self):
        pass


# ----- RunCommand -----
class RunCommand(Command):
    def __init__(self, model, path, vuln_limit, contract_limit, out):
        self.model = model
        self.path = path
        self.out = out

        if vuln_limit < 0:
            raise ValueError("vuln_limit non può essere negativo")
        if contract_limit < 0:
            raise ValueError("contract_limit non può essere negativo")
        if vuln_limit == 0 and contract_limit == 0:
            raise ValueError("❌ Almeno uno tra 'vuln-limit' e 'contract-limit' deve essere maggiore di zero.")


        self.vuln_limit = vuln_limit
        self.contract_limit = contract_limit


    def execute(self):
        try:
            path = self.get_contract_paths(self.path)
        except Exception as e:
            raise
        with open(path, 'r', encoding='utf-8') as f:
            code = f.read()

        payload = {
            "source_code": code,
            "model": self.model,
            "vuln_limit": self.vuln_limit,
            "contract_limit": self.contract_limit
        }
        response = requests.post(f"{os.getenv('API_URL', 'http://localhost:8000')}/api/run", json=payload)
        results = response.json()["results"]

        report_generator = HTMLReportGenerator(out_dir=os.path.join(os.path.dirname(__file__), "../../output_report"))
        report_generator.generate(results=results, file_path=self.path, report_name=self.out)

    def get_contract_paths(self, path: str, extensions=None) -> Path:
        """Restituisce una lista di Path a file validi per l'analisi."""
        if extensions is None:
            extensions = {".teal", ".py", ".txt"}
        path_obj = Path(path)

        if not path_obj.exists():
            raise FileNotFoundError(f"Percorso '{path}' non trovato.")

        if path_obj.is_file():
            if path_obj.suffix in extensions:
                return path_obj
            else:
                raise ValueError(f"Estensione non supportata: {path_obj.suffix}")

        elif path_obj.is_dir():
            raise FileNotFoundError(f"Percorso '{path}' non trovato.")

        else:
            raise ValueError("Il percorso fornito non è corretto.")



# ----- SetModelCommand -----
class SetModelCommand(Command):
    def __init__(self, model_name, source, api_key=None, base_url=None):
        self.base_url = base_url
        self.api_key = api_key
        self.source = source

        if source == "openai":
            if api_key is None:
                raise ValueError("Per i modelli disponibili tramite libreria openai è necessario specificare una API Key")

            if base_url is None:
                raise ValueError("Per i modelli disponibili tramite libreria openai è necessario specificare un Base URL")


        self.model_name = model_name

    def execute(self):
        config = {
            key: value
            for key, value in {
                "source": self.source,
                "model_name": self.model_name,
                "base_url": self.base_url,
                "api_key": self.api_key
            }.items()
            if value is not None
        }
        response = requests.post(f"{os.getenv('API_URL', 'http://localhost:8000')}/api/setmodel", json=config)
        print(response.json()["results"])


class ModelListCommand(Command):
    def execute(self):
        response = requests.post(f"{os.getenv('API_URL', 'http://localhost:8000')}/api/modellist")
        for r in response.json()["results"]:
            print(r)

