from typing import Optional, Set

from sqlalchemy import String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.db.db_setup import Base
from src.db.models.mixins import Timestamp


class Country(Timestamp, Base):
    __tablename__ = "countries"

    alpha_2_iso_code: Mapped[str] = mapped_column(String(2), primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    company_number_regex: Mapped[str] = mapped_column(default="^.*$", nullable=False)

    company: Mapped[Optional[Set["Company"]]] = relationship()
