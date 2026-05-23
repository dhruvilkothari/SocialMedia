from datetime import datetime, timezone
from typing import Optional, Any
from pydantic import BaseModel, Field

class ApiResponse(BaseModel):
    data: Optional[Any] = None
    status_code: int = Field(...)
    # Use default_factory to generate a new timestamp for every instance
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    additional_data: Optional[dict] = None

    class Config:
        from_attributes  = True


