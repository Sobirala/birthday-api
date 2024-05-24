from typing import Any, Optional

from sqlalchemy import BinaryExpression, ColumnOperators, func, select

from app.models import Congratulation
from app.repositories.base import BaseRepository


class CongratulationRepository(BaseRepository[Congratulation]):
    __model__ = Congratulation

    async def random(self, *expressions: BinaryExpression[Any] | ColumnOperators) -> Optional[Congratulation]:
        query = select(self.__model__).order_by(func.random())

        query = self._set_filter(query, expressions)

        return (await self._session.scalars(query)).first()
