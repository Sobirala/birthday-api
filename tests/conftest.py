from unittest.mock import AsyncMock, MagicMock

import pytest
from sqlalchemy import ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped

from app.models import BaseModel
from app.repositories.base import BaseRepository
from app.settings import Settings


class MockModel(BaseModel):
    __tablename__ = "mock"
    id: Mapped[int]


@pytest.fixture
def mock_session():
    mock_session = AsyncMock(AsyncSession)
    mock_session.scalars.return_value = MagicMock(ScalarResult)
    return mock_session


@pytest.fixture
def base_repository(mock_session):
    return BaseRepository(MockModel, mock_session)


@pytest.fixture
def settings():
    return Settings(_env_file="test.env", _env_file_encoding="utf-8")
