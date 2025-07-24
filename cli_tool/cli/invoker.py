# cli/invoker.py
import argparse
import re

from cli.comands import *

class CLIInvoker:
    def __init__(self):
        self.command = None

    def run_command(self):
        self.command.execute()

    def set_command(self, args):
        parser = self._get_parser()
        # Parsing

        parsed_args = parser.parse_args(args)

        if parsed_args.command == "run":
            self.command = RunCommand(model=parsed_args.model, path=parsed_args.filepath, vuln_limit=parsed_args.vuln_limit, contract_limit=parsed_args.contract_limit, out=parsed_args.out)

        if parsed_args.command == "set-model":
            self.command = SetModelCommand(model_name=parsed_args.model_name, source=parsed_args.source, api_key=parsed_args.api_key, base_url=parsed_args.base_url)

        if parsed_args.command == "model-list":
            self.command = ModelListCommand()

    def _get_parser(self):
        parser = argparse.ArgumentParser(description="LLM SmartContractScanner CLI")

        subparsers = parser.add_subparsers(dest="command", required=True)

        # Comando: run
        run_parser = subparsers.add_parser("run", help="Avvia l'analisi completa")
        run_parser.add_argument(
            "--filepath",
            type=str, required=True,
            help="Percorso al contratto da analizzare"
        )
        run_parser.add_argument(
            "--model",
            type=str,
            required=True,
            help="Nome del modello LLM da utilizzare")
        run_parser.add_argument(
            "--vuln-limit",
            type=int,
            default=2,
            help="Numero max di vulnerabilità da rilevare durante la fase il code analisys")
        run_parser.add_argument(
            "--contract-limit",
            type=int,
            default=2,
            help="Numero di contratti simili da recuperare")
        run_parser.add_argument(
            "--out",
            type=valid_report_filename,
            help="Nome del file di report generato dall'analisi.",
            default=None
        )

        # Comando: set-model
        setmodel_parser = subparsers.add_parser("set-model", help="Configure a new model for the system")
        setmodel_parser.add_argument(
            "--model_name",
            type=str,
            required=True,
            help="Name/identifier of the model (e.g., 'gpt-4', 'llama3-8b')"
        )
        setmodel_parser.add_argument(
            "--source",
            type=str,
            required=True,
            choices=["openai", "huggingface"],  # Suggested restriction
            help="Backend provider for the model"
        )
        setmodel_parser.add_argument(
            "--base_url",
            type=str,
            required=False,  # Often optional (defaults to provider's URL)
            help="Custom API endpoint (required for LocalAI or proxies)"
        )
        setmodel_parser.add_argument(
            "--api_key",
            type=str,
            required=False,
            help="API key (if required by the provider)"
        )

        # Comando: model-list
        modellist_parser = subparsers.add_parser("model-list", help="Mostra le configurazioni correnti")

        return parser



def valid_report_filename(value: str) -> str:
    # Definisci una regex per nomi di file validi cross-platform
    if not re.match(r'^[\w,\s-]', value):
        raise argparse.ArgumentTypeError(f"'{value}' non è un nome file valido.")
    # Blocca nomi riservati su Windows
    reserved = {"CON", "PRN", "AUX", "NUL", "COM1", "LPT1", "COM2", "LPT2"}
    if value.split('.')[0].upper() in reserved:
        raise argparse.ArgumentTypeError(f"'{value}' è un nome riservato.")
    return value
