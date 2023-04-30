from datetime import datetime
from unittest.mock import MagicMock

import pytest

from src.business.pydantic_schemas.company import Company, CompanyCreate
from src.business.pydantic_schemas.country import Country, CountryCreate
from src.business.pydantic_schemas.financials import Financials
from src.business.pydantic_schemas.score import Score, ScoreBase


# Countries ---------------------------------------------------------------------------------------------------------
@pytest.fixture
def test_country_create_1():
    return CountryCreate(alpha_2_iso_code="GB",
                         name="United Kingdom",
                         company_number_regex="^([a-zA-Z]{2}[0-9]{6}|[0-9]{8})$")


@pytest.fixture
def test_country_1(test_country_create_1):
    return Country(alpha_2_iso_code=test_country_create_1.alpha_2_iso_code,
                   name=test_country_create_1.name,
                   company_number_regex=test_country_create_1.company_number_regex,
                   created_at=datetime.now(),
                   updated_at=datetime.now())


@pytest.fixture
def test_country_2():
    return Country(alpha_2_iso_code="US",
                   name="United States",
                   company_number_regex="^[0-9]{2}-[0-9]{7}]$",
                   created_at=datetime.now(),
                   updated_at=datetime.now())


@pytest.fixture
def test_country_list_json(test_country_1, test_country_2):
    return [{
                "alpha_2_iso_code": test_country_1.alpha_2_iso_code,
                "name": test_country_1.name,
                "company_number_regex": test_country_1.company_number_regex,
                "created_at": test_country_1.created_at.isoformat(),
                "updated_at": test_country_1.updated_at.isoformat()
            },
            {
                "alpha_2_iso_code": test_country_2.alpha_2_iso_code,
                "name": test_country_2.name,
                "company_number_regex": test_country_2.company_number_regex,
                "created_at": test_country_2.created_at.isoformat(),
                "updated_at": test_country_2.updated_at.isoformat()
            }]


# Companies ---------------------------------------------------------------------------------------------------------
@pytest.fixture
def test_company_create_1():
    return CompanyCreate(company_number="12345678",
                         country_alpha_2_iso_code="GB",
                         name="Unspecified Limited")


@pytest.fixture
def test_company_1(test_company_create_1):
    return Company(company_number=test_company_create_1.company_number,
                   country_alpha_2_iso_code=test_company_create_1.country_alpha_2_iso_code,
                   name=test_company_create_1.name,
                   id=1,
                   scores=[],
                   created_at=datetime.now(),
                   updated_at=datetime.now())


@pytest.fixture
def test_company_create_2():
    return CompanyCreate(company_number="123", country_alpha_2_iso_code="XX")


@pytest.fixture
def test_company_2(test_company_create_2):
    return Company(company_number=test_company_create_2.company_number,
                   country_alpha_2_iso_code=test_company_create_2.country_alpha_2_iso_code,
                   name="Test Company Ltd",
                   id=2,
                   scores=[],
                   created_at=datetime.now(),
                   updated_at=datetime.now())


# Scores ------------------------------------------------------------------------------------------------------------
@pytest.fixture
def test_score_1():
    return Score(year=2020,
                 zscore=6.54,
                 id=1,
                 created_at=datetime.now(),
                 updated_at=datetime.now())


@pytest.fixture
def test_score_base_1(test_score_1):
    return ScoreBase(year=test_score_1.year, zscore=test_score_1.zscore)


@pytest.fixture
def test_score_2():
    return Score(year=2019,
                 zscore=6.79,
                 id=2,
                 created_at=datetime.now(),
                 updated_at=datetime.now())


@pytest.fixture
def test_score_base_2(test_score_2):
    return ScoreBase(year=test_score_2.year, zscore=test_score_2.zscore)


@pytest.fixture
def test_score_list(test_score_base_1, test_score_base_2):
    return [test_score_base_1, test_score_base_2]


# Financials --------------------------------------------------------------------------------------------------------
@pytest.fixture
def test_zero_financials():
    return Financials(year=2000, ebit=0, equity=0, retained_earnings=0, sales=0, total_assets=0,
                      total_liabilities=0, working_capital=0)


@pytest.fixture
def test_financials_1():
    return Financials(year=2020, ebit=123.45, equity=234.56, retained_earnings=345.67, sales=1234.56,
                      total_assets=345.67, total_liabilities=456.78, working_capital=23.45)


@pytest.fixture
def test_financials_2():
    return Financials(year=2019, ebit=122.63, equity=224.56, retained_earnings=325.33, sales=1214.99,
                      total_assets=325.04, total_liabilities=426.78, working_capital=23.45)


@pytest.fixture
def test_financials_list(test_financials_1, test_financials_2):
    return [test_financials_1, test_financials_2]


@pytest.fixture
def test_invalid_financials_list(test_financials_1, test_zero_financials):
    return [test_financials_1, test_zero_financials]


# Other -------------------------------------------------------------------------------------------------------------
@pytest.fixture
def mock_db():
    return MagicMock()