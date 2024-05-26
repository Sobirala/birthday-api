from typing import Any, Optional

from sqlalchemy import BinaryExpression, ColumnOperators, func, select

from app.models import CongratulationModel
from app.repositories.base import BaseRepository


class CongratulationRepository(BaseRepository[CongratulationModel]):
    __model__ = CongratulationModel

    async def random(self, *expressions: BinaryExpression[Any] | ColumnOperators) -> Optional[CongratulationModel]:
        query = select(self.__model__).order_by(func.random())

        query = self._set_filter(query, expressions)

        return (await self._session.scalars(query)).first()
