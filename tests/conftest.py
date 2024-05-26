from unittest.mock import AsyncMock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.fixture
def session_mock():
    return AsyncMock(spec=AsyncSession)

