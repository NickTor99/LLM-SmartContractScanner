from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from vector_db_service.contract_searcher import ContractSearcher

app = FastAPI()


class VectorQuery(BaseModel):
    vector: List[float]


# Create a neural searcher instance
contract_searcher = ContractSearcher(collection_name="vulnerable_contracts")


@app.post("/api/search_vulns")
def search_startup(payload: VectorQuery):
    return {"result": contract_searcher.search_vulns(vector=payload.vector)}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)