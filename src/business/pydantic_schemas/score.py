from datetime import datetime
from pydantic import BaseModel


class ScoreBase(BaseModel):
    year: int
    zscore: float


class ScoreCreate(ScoreBase):
    company_id: int


class Score(ScoreBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
