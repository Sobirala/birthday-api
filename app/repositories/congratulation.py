from typing import Optional, Any

from sqlalchemy import func, select, ColumnOperators, BinaryExpression

from app.enums import Language
from app.models import Congratulation
from app.repositories.base import BaseRepository


class CongratulationRepository(BaseRepository[Congratulation]):
    __model__ = Congratulation

    async def random(self, *expressions: BinaryExpression[Any] | ColumnOperators) -> Optional[Congratulation]:
        query = select(self.__model__).order_by(func.random())

        query = self._set_filter(query, expressions)

        return (await self._session.scalars(query)).first()
