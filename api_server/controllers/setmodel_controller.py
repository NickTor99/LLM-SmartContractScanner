from fastapi import APIRouter
from api_server.api.schemas import SetModelRequest
from api_server.services.setmodel_service import SetModelService

router = APIRouter()
setmodel_service = SetModelService()

@router.post("/setmodel")
def run_analysis(request: SetModelRequest):
    return setmodel_service.execute_run(request)
