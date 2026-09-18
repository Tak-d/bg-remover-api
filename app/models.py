from pydantic import BaseModel


class ApiResponse(BaseModel):
    message: str
    status: str = "ok"