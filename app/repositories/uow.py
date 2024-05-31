from types import TracebackType
from typing import Self, Type

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import BaseModel
from app.repositories.congratulation import CongratulationRepository
from app.repositories.group import GroupRepository
from app.repositories.user import UserRepository


class UnitOfWork:
    _session: AsyncSession

    users: UserRepository
    groups: GroupRepository
    congratulations: CongratulationRepository

    def __init__(self, session: AsyncSession):
        self._session = session
        self.users = UserRepository(self._session)
        self.groups = GroupRepository(self._session)
        self.congratulations = CongratulationRepository(self._session)

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type: Type[BaseException], exc_val: BaseException, exc_tb: TracebackType) -> None:
        await self.commit()

    async def commit(self) -> None:
        await self._session.commit()

    async def delete(self, model: BaseModel) -> None:
        await self._session.delete(model)

    async def rollback(self) -> None:
        await self._session.rollback()
