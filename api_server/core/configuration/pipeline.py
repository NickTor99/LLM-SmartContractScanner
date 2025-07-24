# core/pipeline.py
import ast
import logging

from api_server.core.configuration.context import AppContext
from api_server.core.utils import merge_vuln, map_vulnerability

logger = logging.getLogger(__name__)


def run_pipeline(context: AppContext, source_code: str):
    # Controllo: il codice non deve essere vuoto
    if not source_code.strip():
        logger.error("Errore: il Codice è vuoto.")
        return

    # Controllo: in codice deve essere sintatticamente corretto
    try:
        ast.parse(source_code)
    except SyntaxError as e:
        logger.error(f"Errore di sintassi nel codice inserito: {e}")
        return

    model_list = context.get_code_analyzer().get_possible_vulns(source_code)
    logger.info(f"\nL'analisi preliminare ha trovato le seguenti vulnerabilità: {model_list}\n")

    # Fase 2: Recupera da un database vettoriale altri contratti simili per vulnerabilità
    retrieval_list = context.get_retrieval_engine().get_similar_contracts(source_code)
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
        data["analysis"] = context.get_vuln_analyzer().get_vuln_analysis(vuln, source_code)
        results.append(data)

    print("Analisi completata!")

    return results

