from fastapi import APIRouter
from services.modellist_service import ModelListService

router = APIRouter()
modellist_service = ModelListService()

@router.post("/modellist")
def run_analysis():
    return modellist_service.execute_run()