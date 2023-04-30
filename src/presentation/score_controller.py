import logging
from typing import List, Dict

import fastapi
from fastapi import Path, Depends, HTTPException, Body
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.business.company_service import get_or_create_company, get_company_by_company_number_and_iso_code
from src.business.pydantic_schemas.company import Company
from src.business.pydantic_schemas.financials import Financials
from src.business.pydantic_schemas.score import ScoreBase, Score
from src.business.score_service import validate_financials, request_scores
from src.db.db_setup import get_db
from src.persistence.utilities.score_crud import get_scores_by_company_id

score_router = fastapi.APIRouter()
logger = logging.getLogger("uvicorn")


@score_router.post("/company/{country_iso_code}/{company_number}",
                   response_model=Dict[str, List[ScoreBase]],
                   tags=["required_endpoint"],
                   responses={
                       200: {
                           "description": "Successful Response",
                           "content": {
                               "application/json": {
                                   "example": {"scores": [{"year": 2020, "zscore": 6.47}]}
                               }
                           },
                       },
                       400: {
                           "description": "Bad Request",
                           "content": {
                               "application/json": {
                                   "example": {"detail": "Company didn't exist and failed to create new company or "
                                                         "either total_assets or total_liabilities are 0 which "
                                                         "causes a zero division error for the Altman Z-Score."}
                               }
                           },
                       },
                   }
                   )
async def calculate_score(financials_payload: dict[str, list[Financials]] = Body(example={
    "financials": [
        {
            "year": 2020,
            "ebit": 123.45,
            "equity": 234.56,
            "retained_earnings": 345.67,
            "sales": 1234.56,
            "total_assets": 345.67,
            "total_liabilities": 456.78,
            "working_capital": 23.45
        }],
}),
        country_iso_code: str = Path(..., description="Must be a valid (alpha 2) country ISO code, "
                                                      "capitals only.",
                                     regex="^[A-Z]{2}$"),
        company_number: str = Path(..., description="Must be a valid company number for the country."),
        db: Session = Depends(get_db)):
    logger.info("Received valid request with financials to calculate Z-score(s) for company_number=" + company_number +
                " (" + country_iso_code + ").")
    company: Company = get_or_create_company(company_number, country_iso_code, db)
    if company is None:
        raise HTTPException(status_code=400,
                            detail="Failed to retrieve existing and create new company because the country doesn't "
                                   "exist or the company number violates the country's formatting rules for company "
                                   "numbers.")
    financials_list: list[Financials] = financials_payload.get("financials")
    valid_financials: bool = validate_financials(financials_list)
    if valid_financials is False:
        raise HTTPException(status_code=400,
                            detail="Invalid financials provided. Financials contain 0 values for at least one of the "
                                   "denominators in Altman's Z-Score (total_assets or total_liabilities).")
    return {"scores": request_scores(financials_list=financials_list, company=company, db=db)}


@score_router.get("/company/{country_iso_code}/{company_number}",
                  tags=["company"],
                  response_model=Dict[str, List[Score]],
                  responses={
                      200: {
                          "description": "Successful Response",
                          "content": {
                              "application/json": {
                                  "example": {"scores": [{"year": 2020, "zscore": 6.47}]}
                              }
                          },
                      },
                      404: {
                          "description": "Company Not Found",
                          "content": {
                              "application/json": {
                                  "example": {"detail": "Company does not exist. Please verify that you have entered "
                                                        "the correct country_iso_code and company_number."}
                              }
                          },
                      },
                  }
                  )
async def get_scores_by_company(company_number: str,
                                country_iso_code: str = Path(...,
                                                             description="Must be a valid (alpha 2) country ISO code, "
                                                                         "capitals only. ",
                                                             regex="^[A-Z]{2}$"),
                                skip: int = 0, limit: int = 100,
                                db: Session = Depends(get_db)):
    existing_company = get_company_by_company_number_and_iso_code(db=db, company_number=company_number,
                                                                  country_iso_code=country_iso_code)
    if existing_company is None:
        return JSONResponse(status_code=404, content={"message": "Company does not exist. Please verify that you have "
                                                                 "entered the correct country_iso_code and "
                                                                 "company_number."})
    else:
        logger.info("Company retrieved: " + existing_company.name + " (company_id=" + str(existing_company.id) + ").")
        return {"scores": get_scores_by_company_id(db=db, id=existing_company.id, skip=skip, limit=limit)}
