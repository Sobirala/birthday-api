from app.models import GroupModel
from app.repositories.base import BaseRepository


class GroupRepository(BaseRepository[GroupModel]):
    __model__ = GroupModel
