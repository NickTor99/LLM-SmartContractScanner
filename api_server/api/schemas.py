from pydantic import BaseModel
from typing import List, Optional

class VectorQuery(BaseModel):
    vector: List[float]


class RunRequest(BaseModel):
    source_code: str
    model: str
    vuln_limit: int
    contract_limit: int


class SetModelRequest(BaseModel):
    source: str
    model_name: str
    base_url: Optional[str] = None
    api_key: Optional[str] = None
