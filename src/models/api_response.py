from typing import Any, Optional
from pydantic import BaseModel


class ApiResponse(BaseModel):
    success: bool
    status_code: int
    data: Optional[Any]
    message: Optional[str]
