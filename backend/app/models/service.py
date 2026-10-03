from pydantic import BaseModel, Field
from typing import List

class Service(BaseModel):
    service_id: str = Field(alias="_id")
    category: str
    name: str
    specializations: List[str]

    class Config:
        populate_by_name = True
