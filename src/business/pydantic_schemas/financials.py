from pydantic.main import BaseModel


class Financials(BaseModel):
    year: int
    ebit: float
    equity: float
    retained_earnings: float
    sales: float
    total_assets: float
    total_liabilities: float
    working_capital: float

    # class Config:
    # Add validation for year (int) and possibly floats here
