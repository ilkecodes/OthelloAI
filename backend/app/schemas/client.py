from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ClientBase(BaseModel):
    name: str
    industry: Optional[str] = None
    keywords: Optional[str] = None  # String olarak, virgülle ayrılmış

class ClientCreate(ClientBase):
    pass

class ClientResponse(ClientBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
