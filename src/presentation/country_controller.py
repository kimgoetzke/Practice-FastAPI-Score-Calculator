from typing import List

import fastapi
from fastapi import Depends, HTTPException, Path
from sqlalchemy.orm import Session

from src.business.pydantic_schemas.country import Country, CountryCreate
from src.db.db_setup import get_db
from src.persistence.utilities.country_crud import get_country, get_countries, create_country

country_router = fastapi.APIRouter(tags=["country"])


@country_router.get("/country/{country_iso_code}")
async def get_country_by_alpha_2_iso_code(country_iso_code: str = Path(...,
                                                                       description="Must be a valid (alpha 2) country "
                                                                                   "ISO code, capitals only.",
                                                                       regex="^[A-Z]{2}$"),
                                          db: Session = Depends(get_db)):
    db_country = get_country(db=db, alpha_2_iso_code=country_iso_code)
    if db_country is None:
        raise HTTPException(status_code=404, detail="Country not found.")
    return db_country


@country_router.get("/country", response_model=List[Country])
async def get_all_countries(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_countries = get_countries(db=db, skip=skip, limit=limit)
    return db_countries


@country_router.post("/country", response_model=Country, status_code=201)
async def create_new_country(country: CountryCreate, db: Session = Depends(get_db)):
    existing_country: Country = get_country(db=db, alpha_2_iso_code=country.alpha_2_iso_code)
    if existing_country is not None and existing_country.alpha_2_iso_code == country.alpha_2_iso_code:
        raise HTTPException(status_code=400, detail="Country exists in database. Duplicates not permitted.")
    else:
        return create_country(db=db, country=country)
