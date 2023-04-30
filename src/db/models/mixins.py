from datetime import datetime

from sqlalchemy import Column, DateTime
from sqlalchemy.orm import declarative_mixin, Mapped, mapped_column


@declarative_mixin
class Timestamp:
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now(), nullable=False)