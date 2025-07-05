# core/pipeline.py
import ast
import logging

from configuration.context import AppContext
from utils import load_string, merge_vuln, map_vulnerability

import os
from pathlib import Path

logger = logging.getLogger(__name__)

def get_contract_paths(path: str, extensions=None) -> list[Path]:
    """Restituisce una lista di Path a file validi per l'analisi."""
    if extensions is None:
        extensions = {".teal", ".py", ".txt"}
    path_obj = Path(path)

    if not path_obj.exists():
        raise FileNotFoundError(f"Percorso '{path}' non trovato.")

    if path_obj.is_file():
        if path_obj.suffix in extensions:
            return [path_obj]
        else:
            raise ValueError(f"Estensione non supportata: {path_obj.suffix}")

    elif path_obj.is_dir():
        # Raccoglie tutti i file validi nella directory (ricorsivamente se vuoi)
        files = [f for f in path_obj.glob("*") if f.is_file() and f.suffix in extensions]
        if not files:
            raise ValueError("Nessun file valido trovato nella cartella.")
        return files

    else:
        raise ValueError("Il percorso fornito non è né file né directory.")


def run_pipeline(context: AppContext, path: str):

    paths = get_contract_paths(path)

    for contract_path in paths:
        # Carica il contenuto del contratto come stringa
        code = load_string(str(contract_path))

        # Controllo: il codice non deve essere vuoto
        if not code.strip():
            logger.error("Errore: il Codice è vuoto.")
            return

        # Controllo: in codice deve essere sintatticamente corretto
        try:
            ast.parse(code)
        except SyntaxError as e:
            logger.error(f"Errore di sintassi nel codice inserito: {e}")
            return

        model_list = context.get_code_analyzer().get_possible_vulns(code)
        logger.info(f"\nL'analisi preliminare ha trovato le seguenti vulnerabilità: {model_list}\n")

        # Fase 2: Recupera da un database vettoriale altri contratti simili per vulnerabilità
        retrieval_list = context.get_retrieval_engine().get_similar_contracts(code)
        logger.info(f"Tramite il retrieval di contratti simili sono state trovate le seguenti vulnerabilità: {retrieval_list}\n\n")

        # Fase 3: Unione dei risultati ottenuti dalle due fasi precedenti
        vulns_to_analyze = merge_vuln(model_list, retrieval_list)

        logger.info(f"\n{50*'-'}Inizio analisi dettagliata delle vulnerabilità{50*'-'}\n")

        results = ""
        # Fase 4: Per ogni vulnerabilità da analizzare, esegue un'analisi approfondita con contesto
        for vuln in vulns_to_analyze:
            vuln = map_vulnerability(vuln)  # Mappa eventuali alias o sinonimi della vulnerabilità
            results = f"{results}{'-'*50}\n\n{context.get_vuln_analyzer().get_vuln_analysis(vuln, code)}"

        logger.info(results)
        logger.info("Analisi completata!")
