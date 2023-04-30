from sqlalchemy.orm import Session

from src.business.pydantic_schemas.company import CompanyCreate
from src.db.models.company import Company


def get_company(db: Session, id: int):
    return db.query(Company).filter(Company.id == id).first()


def get_company_by_company_number(db: Session, company_number: str):
    return db.query(Company).filter(Company.company_number == company_number).first()


def get_companies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Company).offset(skip).limit(limit).all()


def create_company(db: Session, company: CompanyCreate):
    db_company = Company(company_number=company.company_number,
                         country_alpha_2_iso_code=company.country_alpha_2_iso_code,
                         name=company.name)
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company
