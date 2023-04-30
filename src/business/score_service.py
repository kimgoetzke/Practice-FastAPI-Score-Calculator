import logging

from sqlalchemy.orm import Session

from src.business.pydantic_schemas.company import Company
from src.business.pydantic_schemas.financials import Financials
from src.business.pydantic_schemas.score import ScoreCreate, ScoreBase
from src.persistence.utilities.score_crud import create_score

logger = logging.getLogger("uvicorn")


def validate_financials(financials: list[Financials]):
    for f in financials:
        if f.total_assets == 0 or f.total_liabilities == 0:
            return False
    return True


def request_scores(financials_list: list[Financials], company: Company, db: Session):
    logger.info("Score(s) to be calculated for: " + company.name + " (company_number=" + str(company.company_number) +
                ", country_alpha_2_iso_code=" + company.country_alpha_2_iso_code + ").")
    scores: list[ScoreCreate] = []
    for f in financials_list:
        score: ScoreCreate = ScoreCreate(company_id=company.id, year=f.year, zscore=calculate_score(f))
        scores.append(score)
    logger.info("Created objects: " + str(scores))
    scores_report: list[ScoreBase] = []
    for s in scores:
        create_score(db=db, score=s)
        score_for_report: ScoreBase = ScoreBase(year=s.year, zscore=s.zscore)
        scores_report.append(score_for_report)
    logger.info("Report scores created: " + str(scores_report))
    return scores_report


def calculate_score(financials: Financials):
    a: float = 1.2 * (financials.working_capital / financials.total_assets)
    b: float = 1.4 * (financials.retained_earnings / financials.total_assets)
    c: float = 3.3 * (financials.ebit / financials.total_assets)
    d: float = 0.6 * (financials.equity / financials.total_liabilities)
    e: float = 1.0 * (financials.sales / financials.total_assets)
    score = round(a + b + c + d + e, 2)
    logger.info("Calculated zscore for " + str(financials.year) + ": " + str(score) + ".")
    return score
