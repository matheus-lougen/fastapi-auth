from __future__ import annotations

from datetime import datetime

from sqlalchemy import exists, func, select
from sqlalchemy.orm import Mapped, Session, mapped_column, registry

table_registry = registry()


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now(), onupdate=func.now())

    @classmethod
    def fetch_by_id(cls, id: int, session: Session) -> User:
        return session.scalar(select(User).where(User.id == id))

    def exists(self, session: Session) -> bool:
        return session.scalar(exists().where((User.username == self.username) | (User.email == self.email)).select())
