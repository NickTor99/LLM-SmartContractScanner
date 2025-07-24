from fastapi import APIRouter
from api_server.services.modellist_service import ModelListService

router = APIRouter()
modellist_service = ModelListService()

@router.post("/modellist")
def run_analysis():
    return modellist_service.execute_run()