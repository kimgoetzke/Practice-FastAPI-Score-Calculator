from datetime import datetime
from typing import Optional
from pydantic import BaseModel, validator


class CountryBase(BaseModel):
    alpha_2_iso_code: str
    name: str
    company_number_regex: Optional[str] = ""


class CountryCreate(CountryBase):
    pass

    @validator("alpha_2_code", check_fields=False)
    def alpha_2_code_is_valid(cls, value):
        if len(value) != 2:
            raise InvalidCountryCodeError(value=value,
                                          message="Country code must be 2 characters long and must not contain digits.")
        return value

    @validator("company_number_regex")
    def set_company_number_regex(cls, value):
        return value or "^.*$"


class Country(CountryBase):
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        validate_assignment = True


class InvalidCountryCodeError(Exception):
    def __init__(self, value: str, message: str) -> None:
        self.value = value
        self.message = message
        super().__init__(message)
