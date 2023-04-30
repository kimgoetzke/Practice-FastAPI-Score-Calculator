from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.db.db_setup import Base
from src.db.models.mixins import Timestamp


class Score(Timestamp, Base):
    __tablename__ = "scores"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False)
    year: Mapped[int] = mapped_column(nullable=False)
    zscore: Mapped[float] = mapped_column(nullable=False)

    company: Mapped["Company"] = relationship(back_populates="scores")

    def __repr__(self):
        return f"Score(id={self.id}, company_id={self.company_id}, year={self.year}, zscore={self.zscore})"
