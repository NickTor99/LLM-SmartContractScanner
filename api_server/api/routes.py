from fastapi import FastAPI
from controllers import run_controller, setmodel_controller, modellist_controller
import logging

from vector_db_service.contract_searcher import ContractSearcher

logger = logging.getLogger(__name__)

contract_searcher = ContractSearcher(collection_name="vulnerable_contracts")

def create_app() -> FastAPI:
    app = FastAPI(
        title="LLM-SmartContractScanner API"
    )

    # Include routers
    app.include_router(run_controller.router, prefix="/api")
    app.include_router(setmodel_controller.router, prefix="/api")
    app.include_router(modellist_controller.router, prefix="/api")


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

    return app
