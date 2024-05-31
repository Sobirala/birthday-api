from typing import Optional, Sequence

from sqlalchemy import ColumnElement, Interval, and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.base import ExecutableOption
from sqlalchemy.sql.functions import concat

from app.models import GroupModel, UserModel
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[UserModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(UserModel, session)

    async def get_user_in_group(self, user_id: int, chat_id: int, options: Optional[Sequence[ExecutableOption]] = None) -> Optional[UserModel]:
        query = select(self.__model__) \
            .join(UserModel.groups) \
            .filter(GroupModel.id == chat_id) \
            .filter(UserModel.id == user_id) \
            .limit(1)

        if options is not None:
            query = query.options(*options)

        return (await self._session.scalars(query)).first()

    async def get_birthday_group_users(self, birthday_id: int, group_id: int) -> Sequence[UserModel]:
        query = select(UserModel) \
                .select_from(GroupModel) \
                .join(GroupModel.users) \
                .filter(GroupModel.id == group_id) \
                .filter(UserModel.id != birthday_id)

        return (await self._session.scalars(query)).all()
