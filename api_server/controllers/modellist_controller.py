from fastapi import APIRouter
from services.modellist_service import ModelListService

router = APIRouter()
modellist_service = ModelListService()


@router.post("/modellist")
def control_request():
    return modellist_service.execute()

