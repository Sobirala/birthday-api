from typing import Any, Optional

from sqlalchemy import BinaryExpression, ColumnOperators, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CongratulationModel
from app.repositories.base import BaseRepository


class CongratulationRepository(BaseRepository[CongratulationModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(CongratulationModel, session)

    async def random(self, *expressions: BinaryExpression[Any] | ColumnOperators) -> Optional[CongratulationModel]:
        query = select(self.__model__).order_by(func.random())

        query = self._set_filter(query, expressions)

        return (await self._session.scalars(query)).first()
