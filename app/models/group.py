from typing import TYPE_CHECKING, List

from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.enums import Language
from app.models.base import BaseModel, TimestampMixin

if TYPE_CHECKING:
    from app.models.user import UserModel


class GroupModel(TimestampMixin, BaseModel):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    title: Mapped[str]
    language: Mapped[Language] = mapped_column(default=Language.UK)
    collect: Mapped[bool] = mapped_column(default=False)
    users: Mapped[List["UserModel"]] = relationship(
        secondary="usergrouplink",
        back_populates="groups"
    )
