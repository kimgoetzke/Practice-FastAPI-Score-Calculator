import logging
from typing import List

import fastapi
from fastapi import Depends, HTTPException, Body
from sqlalchemy.orm import Session

from src.business.company_service import create_company_if_not_exist
from src.business.pydantic_schemas.company import Company, CompanyCreate
from src.db.db_setup import get_db
from src.persistence.utilities.company_crud import get_company, get_companies

company_router = fastapi.APIRouter(tags=["company"])
logger = logging.getLogger("uvicorn")


@company_router.get("/company", response_model=List[Company])
async def get_all_companies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    companies = get_companies(db=db, skip=skip, limit=limit)
    return companies


@company_router.post("/company", response_model=Company, status_code=201)
async def create_company(company: CompanyCreate, db: Session = Depends(get_db)):
    logger.info("Request to create company received: " + str(company) + ".")
    db_company = create_company_if_not_exist(company=company, db=db)
    if db_company is None:
        raise HTTPException(status_code=400, detail="Failed to created company because one of the following is true: "
                                                    "1) company exists, 2) country doesn't exist, 3) or company number "
                                                    "violates the country's formatting rules for company numbers.")
    return db_company
