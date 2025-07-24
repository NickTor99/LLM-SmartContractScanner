from api_server.api.schemas import RunRequest
from api_server.core.configuration.context import AppContext
from api_server.core.configuration.pipeline import run_pipeline


class RunService:
    def execute_run(self, request: RunRequest):
        try:
            context = AppContext(model=request.model, vuln_limit=request.vuln_limit, contract_limit=request.contract_limit)
            results = run_pipeline(context=context, source_code=request.source_code)
        except Exception as e:
            return {
                "status": "fail",
                "results": f"{e}",
            }

        return {
            "status": "success",
            "results": results,
        }
