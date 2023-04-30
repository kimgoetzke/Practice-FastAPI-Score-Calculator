from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from src.business.pydantic_schemas.score import Score


class CompanyBase(BaseModel):
    company_number: str
    country_alpha_2_iso_code: str
    name: Optional[str] = "Unknown"


class CompanyCreate(CompanyBase):
    pass


class Company(CompanyBase):
    id: int
    scores: Optional[list[Score]] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
