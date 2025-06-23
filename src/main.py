from src.analysis_module.code_analysis import CodeAnalysis
from src.llm.openai_llm import OpenAILLM
from src.retrieval_module.code_descriptor import CodeDescriptor
from src.retrieval_module.embedding_model import EmbeddingModel
from src.retrieval_module.retrieval_engine import RetrievalEngine
from src.analysis_module.vuln_analysis import VulnAnalysis
from src.utils import *
from dotenv import load_dotenv
import os


def main(path: str = None):

    if path is None:
        # Carica il percorso al file contenente il contratto da analizzare
        path = get_valid_filepath()

    load_dotenv()  # Carica le variabili da .env
    api_key = os.getenv("API_KEY")

    # Carica il contenuto del contratto come stringa
    code = load_string(path)

    # Inizializza un'istanza del modello LLM di OpenAI (in questo caso DeepSeek), passando chiave API e URL personalizzato
    llm = OpenAILLM(
        api_key=api_key,
        model_name="deepseek-chat",
        base_url="https://api.deepseek.com"
    )

    # Inizializza il modulo per l'analisi delle vulnerabilità potenziali basata su LLM
    code_analyzer = CodeAnalysis(llm_model=llm)

    # Inizializza il modulo che genera una descrizione in linguaggio naturale del codice
    code_descriptor = CodeDescriptor(llm_model=llm)

    # Inizializza il modello di embedding per convertire le descrizioni in vettori (per il retrieval)
    embedder = EmbeddingModel(device="cpu")

    # Inizializza il motore di retrieval per trovare codici simili tramite descrizioni e vettori
    retrieval = RetrievalEngine(url="http://localhost:8000/api/search_vulns", descriptor=code_descriptor, embedder=embedder)

    # Inizializza il modulo di analisi approfondita per vulnerabilità specifiche, con supporto RAG
    vuln_analysis = VulnAnalysis(llm_model=llm)

    # ----------------------
    # Inizio della pipeline di analisi
    # ----------------------

    # Fase 1: LLM analizza il codice per estrarre una lista di potenziali vulnerabilità
    model_list = code_analyzer.get_possible_vulns(code)
    print(f"Model List: {model_list}\n\n")

    # Fase 2: Recupera da un database vettoriale altri contratti simili per vulnerabilità
    retrieval_list = retrieval.get_similar_contracts(code)
    print(f"Retrieved List: {retrieval_list}\n\n")

    # Fase 3: Unione dei risultati ottenuti dalle due fasi precedenti
    vulns_to_analyze = merge_vuln(model_list, retrieval_list)

    results = ""
    # Fase 4: Per ogni vulnerabilità da analizzare, esegue un'analisi approfondita con contesto
    for vuln in vulns_to_analyze:
        vuln = map_vulnerability(vuln)  # Mappa eventuali alias o sinonimi della vulnerabilità
        results = f"{results}{'-'*50}\n\n{vuln_analysis.get_vuln_analysis(vuln, code)}"

    print(results)
    print("Analisi completata!")


if __name__ == "__main__":
    main()