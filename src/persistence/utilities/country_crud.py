from sqlalchemy.orm import Session

from src.business.pydantic_schemas.country import CountryCreate
from src.db.models.country import Country


def get_country(db: Session, alpha_2_iso_code: str):
    return db.query(Country).filter(Country.alpha_2_iso_code == alpha_2_iso_code).first()


def get_country_by_id(db: Session, id: int):
    return db.query(Country).filter(Country.id == id).first()


def get_country_by_name(db: Session, name: str):
    return db.query(Country).filter(Country.name == name).first()


def get_countries(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Country).offset(skip).limit(limit).all()


def create_country(db: Session, country: CountryCreate):
    db_country = Country(alpha_2_iso_code=country.alpha_2_iso_code,
                         name=country.name,
                         company_number_regex=country.company_number_regex)
    db.add(db_country)
    db.commit()
    db.refresh(db_country)
    return db_country
