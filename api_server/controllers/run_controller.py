from fastapi import APIRouter
from api_server.api.schemas import RunRequest
from api_server.services.run_service import RunService

router = APIRouter()
run_service = RunService()

@router.post("/run")
def run_analysis(request: RunRequest):
    return run_service.execute_run(request)
