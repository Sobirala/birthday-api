from uuid import uuid4

import pytest

from app.models import GroupModel
from app.repositories import GroupRepository


@pytest.fixture
def repository(session_mock):
    return GroupRepository(session=session_mock)


@pytest.fixture
def sample_group():
    return GroupModel(id=1, title="Test Group")


@pytest.mark.asyncio
async def test_create_group(repository, session_mock, sample_group):
    result = await repository.create(sample_group)
    session_mock.add.assert_called_once_with(sample_group)
    assert result == sample_group


@pytest.mark.asyncio
async def test_merge_group(repository, session_mock, sample_group):
    session_mock.merge.return_value = sample_group
    result = await repository.merge(sample_group)
    session_mock.merge.assert_called_once_with(sample_group)
    assert result == sample_group


@pytest.mark.asyncio
async def test_get_group(repository, session_mock, sample_group):
    pk = uuid4()
    session_mock.get.return_value = sample_group
    result = await repository.get(pk)
    session_mock.get.assert_called_once_with(GroupModel, pk, options=None)
    assert result == sample_group


@pytest.mark.asyncio
async def test_delete_group(repository, session_mock):
    await repository.delete(GroupModel.title == "Test Group")
    session_mock.execute.assert_called_once()


@pytest.mark.asyncio
async def test_get_count(repository, session_mock):
    session_mock.scalar.return_value = 10
    result = await repository.get_count(GroupModel.title == "Test Group")
    session_mock.scalar.assert_called_once()
    assert result == 10


@pytest.mark.asyncio
async def test_check_exists(repository, session_mock):
    session_mock.scalar.return_value = True
    result = await repository.check_exists(GroupModel.title == "Test Group")
    session_mock.scalar.assert_called_once()
    assert result is True
