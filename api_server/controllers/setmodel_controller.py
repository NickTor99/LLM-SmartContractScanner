from fastapi import APIRouter, HTTPException, status
from api.schemas import SetModelRequest
from services.setmodel_service import SetModelService

router = APIRouter()
setmodel_service = SetModelService()

@router.post("/setmodel")
def control_request(request: SetModelRequest):

    if request.model_name == "":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Il parametro 'model_name' non può essere vuoto."
        )

    if request.source not in ["openai", "huggingface"]:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Il parametro 'source' deve essere 'openai' o 'huggingface'."
        )

    # api_key e base_url possono essere vuoti, ma controlliamo combinazioni specifiche:
    if request.source == "huggingface":
        # Per huggingface api_key o base_url devono essere valorizzati entrambi o almeno uno
        if request.api_key or request.base_url:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=""
            )
    else:
        # Se uno è vuoto e l'altro no, potrebbe essere un errore
        if not request.api_key or not request.base_url:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Per 'openai', api_key e base_url devono essere entrambi valorizzati."
            )
        if request.api_key == "" or request.base_url == "":
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Per 'openai', api_key e base_url devono essere entrambi valorizzati."
            )

    return setmodel_service.execute(request)
