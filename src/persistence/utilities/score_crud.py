import logging

from sqlalchemy.orm import Session

from src.business.pydantic_schemas.score import ScoreCreate
from src.db.models.score import Score

logger = logging.getLogger("uvicorn")


def get_score(db: Session, id: int):
    return db.query(Score).filter(Score.id == id).first()


def get_scores_by_company_id(db: Session, id: int, skip: int = 0, limit: int = 100):
    return db.query(Score).filter(Score.company_id == id).offset(skip).limit(limit).all()


def get_scores(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Score).offset(skip).limit(limit).all()


def create_score(db: Session, score: ScoreCreate):
    db_score = Score(company_id=score.company_id, year=score.year, zscore=score.zscore)
    db.add(db_score)
    db.commit()
    db.refresh(db_score)
    logger.info("Score inserted into database: " + str(db_score))
    return db_score
