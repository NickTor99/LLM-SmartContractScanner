from src.analysis_module.code_analysis import CodeAnalysis
from llm.openai_llm import OpenAILLM
from retrieval_module.code_descriptor import CodeDescriptor
from retrieval_module.embedding_model import EmbeddingModel
from retrieval_module.retrieval_engine import RetrievalEngine
from analysis_module.vuln_analysis import VulnAnalysis
from utils import *
from dotenv import load_dotenv
import os

load_dotenv()  # Carica le variabili da .env
api_key = os.getenv("API_KEY")

# Percorso al file contenente il contratto da analizzare
path = "C:\\Users\\Smart\\Desktop\\contract.txt"

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

# Fase 4: Per ogni vulnerabilità da analizzare, esegue un'analisi approfondita con contesto
for vuln in vulns_to_analyze:
    vuln = map_vulnerability(vuln)  # Mappa eventuali alias o sinonimi della vulnerabilità
    print(vuln_analysis.get_vuln_analysis(vuln, code))  # Stampa il risultato dell'analisi specifica

