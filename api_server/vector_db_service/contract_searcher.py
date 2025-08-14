import os

from qdrant_client import QdrantClient
import logging

logger = logging.getLogger(__name__)



class ContractSearcher:
    def __init__(self, collection_name: str, url_db: str = os.getenv("QDRANT_URL", "http://localhost:6333")):
        self.collection_name = collection_name

        # initialize Qdrant client
        self.qdrant_client = QdrantClient(url_db,check_compatibility=False)


    def search_vulns(self, vector: list) -> list:

        try:
            # Use `vector` for search for closest vectors in the collection
            search_result = self.qdrant_client.query_points(
                collection_name=self.collection_name,
                query=vector,
                query_filter=None,  # If you don't want any filters for now
                limit=10,  # 10 closest results is enough
            ).points
        except Exception as e:
            logger.error(f"Collection {self.collection_name} non trovata")
            raise RuntimeError(f"Collection not found") from e
        # `search_result` contains found vector ids with similarity scores along with the stored payload
        # In this function you are interested in payload only
        vulns = []
        for hit in search_result:
            vulns.append({"contract_id": hit.payload['contract_id'],"vulnerability":hit.payload['vulnerability'],"score": round(hit.score,3)})
        return vulns

