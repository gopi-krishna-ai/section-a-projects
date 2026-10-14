from fastapi import APIRouter
from backend.schemas import ExecuteCodeRequest, ExecuteCodeResponse
from backend.services.executor import execute_python_code

router = APIRouter(prefix="/api/execution", tags=["Execution"])

@router.post("/run", response_model=ExecuteCodeResponse)
def run_code(payload: ExecuteCodeRequest):
    res = execute_python_code(payload.code, payload.stdin_input)
    return ExecuteCodeResponse(
        stdout=res["stdout"],
        stderr=res["stderr"],
        exit_code=res["exit_code"],
        execution_time_ms=res["execution_time_ms"],
        error_type=res["error_type"]
    )
