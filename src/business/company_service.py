import logging
import re

from sqlalchemy.orm import Session
from src.business.pydantic_schemas.company import Company, CompanyCreate
from src.business.pydantic_schemas.country import Country
from src.persistence.utilities.company_crud import get_company_by_company_number, create_company
from src.persistence.utilities.country_crud import get_country

logger = logging.getLogger("uvicorn")


def get_company_by_company_number_and_iso_code(db: Session, company_number: str, country_iso_code: str):
    existing_company: Company = get_company_by_company_number(db=db, company_number=company_number)
    logger.info("Company: Exists=" + str(existing_company is not None) + ".")
    if existing_company is None or existing_company.country_alpha_2_iso_code != country_iso_code:
        return None
    else:
        return existing_company


def create_company_if_not_exist(company: CompanyCreate, db: Session):
    existing_company: Company = get_company_by_company_number(db=db, company_number=company.company_number)
    if existing_company is not None and existing_company.country_alpha_2_iso_code == company.country_alpha_2_iso_code:
        logger.error("Company exists in database. Duplicates not allowed.")
        return None
    return __create_new_company(company=company, db=db)


def get_or_create_company(company_number, country_iso_code, db):
    company: Company = get_company_by_company_number_and_iso_code(db=db, company_number=company_number,
                                                                  country_iso_code=country_iso_code)
    if company is None:
        logger.info("Company doesn't exist. Attempting to create new company...")
        new_company: CompanyCreate = CompanyCreate(company_number=company_number,
                                                   country_alpha_2_iso_code=country_iso_code)
        db_company: Company = __create_new_company(company=new_company, db=db)
        company = db_company
    return company


def __create_new_company(company: CompanyCreate, db: Session):
    existing_country: Country = get_country(alpha_2_iso_code=company.country_alpha_2_iso_code, db=db)
    if existing_country is None:
        logger.error(f"Cannot create company for country that doesn't exist. The country "
                     f"({company.country_alpha_2_iso_code}) must be created first.")
        return None
    valid_company_number: bool = validate_company_number_with_regex(company_number=company.company_number,
                                                                    regex=existing_country.company_number_regex)
    if not valid_company_number:
        logger.error(f"Invalid company number. Number doesn't comply with the formatting rules for "
                     f"{company.country_alpha_2_iso_code} company numbers.")
        return None
    db_company = create_company(db=db, company=company)
    return db_company


def validate_company_number_with_regex(company_number: str, regex: str):
    if re.search(regex, company_number) is None:
        return False
    return True
