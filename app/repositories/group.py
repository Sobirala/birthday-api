from sqlalchemy.ext.asyncio import AsyncSession

from app.models import GroupModel
from app.repositories.base import BaseRepository


class GroupRepository(BaseRepository[GroupModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(GroupModel, session)
