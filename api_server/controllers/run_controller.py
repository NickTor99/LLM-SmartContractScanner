from fastapi import APIRouter, HTTPException, status
from api.schemas import RunRequest
from services.run_service import RunService

router = APIRouter()
run_service = RunService()

@router.post("/run")
def control_request(request: RunRequest):
    if request.model == "":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Il parametro model non può essere vuoto."
        )

    if request.source_code == "":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Il parametro source_code non può essere vuoto."
        )

    if request.vuln_limit < 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Il parametro vuln_limit deve essere maggiore o uguale a zero."
        )

    if request.contract_limit < 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Il parametro contract_limit deve essere maggiore o uguale a zero."
        )

    result = run_service.execute(request)

    if result["status"] == "success":
        return result
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result["results"]
        )
