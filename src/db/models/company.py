from typing import List, Optional

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.db.db_setup import Base
from src.db.models.mixins import Timestamp


class Company(Timestamp, Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    company_number: Mapped[str] = mapped_column(String(100), nullable=False)
    country_alpha_2_iso_code: Mapped[str] = \
        mapped_column(String(2), ForeignKey("countries.alpha_2_iso_code"), nullable=False)
    name: Mapped[str] = mapped_column(String, default="Unknown")

    scores: Mapped[Optional[List["Score"]]] = relationship(back_populates="company")
