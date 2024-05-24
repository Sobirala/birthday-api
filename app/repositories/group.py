from typing import Optional

from app.models import Group
from app.repositories.base import BaseRepository


class GroupRepository(BaseRepository[Group]):
    __model__ = Group
