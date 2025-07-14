# core/pipeline.py
import ast
import logging

from configuration.context import AppContext
from utils import load_string, merge_vuln, map_vulnerability

import os
from pathlib import Path

logger = logging.getLogger(__name__)

def get_contract_paths(path: str, extensions=None) -> Path:
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


def run_pipeline(context: AppContext, path: str):

    try:
        path = get_contract_paths(path)
    except Exception as e:
        raise

    with open(path, 'r', encoding='utf-8') as f:
        code = f.read()

    logger.info(f"\nL'analisi del file {path} iniziata")

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

    results = []


    # Fase 4: Per ogni vulnerabilità da analizzare, esegue un'analisi approfondita con contesto
    for vuln in vulns_to_analyze:
        data = {}
        vuln = map_vulnerability(vuln)  # Mappa eventuali alias o sinonimi della vulnerabilità

        data["vulnerability"] = vuln
        data["analysis"] = context.get_vuln_analyzer().get_vuln_analysis(vuln, code)
        results.append(data)

    print("Analisi completata!")

    return results

