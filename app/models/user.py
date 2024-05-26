import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.enums import Gender
from app.models.base import BaseModel, TimestampMixin

if TYPE_CHECKING:
    from app.models.group import GroupModel


class UserModel(TimestampMixin, BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    fullname: Mapped[str]
    gender: Mapped[Gender]
    timezone: Mapped[str]
    birthday: Mapped[datetime.date]
    groups: Mapped[List["GroupModel"]] = relationship(secondary="usergrouplink", back_populates="users")
