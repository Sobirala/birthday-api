import datetime
from typing import Optional, Sequence

from sqlalchemy import ColumnElement, Interval, and_, func, select
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.base import ExecutableOption
from sqlalchemy.sql.functions import concat

from app.enums import Gender
from app.models import Group, User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    __model__ = User

    async def get_user_in_group(self, user_id: int, chat_id: int, options: Optional[Sequence[ExecutableOption]] = None) -> Optional[User]:
        query = select(User) \
            .join(User.groups) \
            .filter(Group.id == chat_id) \
            .filter(User.id == user_id) \
            .limit(1)

        if options is not None:
            query = query.options(*options)

        return (await self._session.scalars(query)).first()

    async def get_birthday_persons(self, interval: int = 0) -> Sequence[User]:
        query = select(User).options(selectinload(User.groups)).filter(self._get_filter(interval))

        return (await self._session.scalars(query)).all()

    @staticmethod
    def _get_filter(interval: int = 0) -> ColumnElement[bool]:
        date = func.current_date()
        if interval != 0:
            date += func.cast(concat(interval, ' DAYS'), Interval)  # type: ignore[assignment]
        return and_(
            func.extract("MONTH", User.birthday) == func.extract("MONTH", date),
            func.extract("DAY", User.birthday) == func.extract("DAY", date),
            func.extract("HOUR", func.timezone(User.timezone, func.current_time())) == 9
        )

    async def get_birthday_group_users(self, birthday_id: int, group_id: int) -> Sequence[User]:
        query = select(User) \
                .select_from(Group) \
                .join(Group.users) \
                .filter(Group.id == group_id) \
                .filter(User.id != birthday_id)

        return (await self._session.scalars(query)).all()
