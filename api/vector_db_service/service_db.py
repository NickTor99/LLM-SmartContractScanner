import logging

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from contract_searcher import ContractSearcher

app = FastAPI()
logger = logging.getLogger(__name__)

class VectorQuery(BaseModel):
    vector: List[float]


# Create a neural searcher instance
contract_searcher = ContractSearcher(collection_name="vulnerable_contracts")

@app.on_event("startup")
def check_db_connection():
    global contract_searcher
    try:
        # Prova a chiamare un metodo dummy o health-check sul DB (opzionale)
        _ = contract_searcher.qdrant_client.get_collections()

        logger.info("Database raggiunto con successo.")
    except Exception as e:
        logger.error(f"Impossibile connettersi al database: {e}")
        # Fermiamo l’avvio del server
        raise RuntimeError("Errore di connessione al database")



@app.post("/api/search_vulns")
def search_startup(payload: VectorQuery):
    return {"result": contract_searcher.search_vulns(vector=payload.vector)}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)