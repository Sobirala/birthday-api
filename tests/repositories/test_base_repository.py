from uuid import uuid4

import pytest
from sqlalchemy import select
from sqlalchemy import BinaryExpression
from sqlalchemy.orm import selectinload

from tests.conftest import MockModel


@pytest.mark.asyncio
async def test_get_count(base_repository, mock_session):
    mock_session.scalar.return_value = 1
    result = await base_repository.get_count()
    assert result == 1
    mock_session.scalar.assert_called_once()

@pytest.mark.asyncio
async def test_create(base_repository, mock_session):
    mock_model = MockModel()
    result = await base_repository.create(mock_model)
    assert result == mock_model
    mock_session.add.assert_called_once_with(mock_model)

@pytest.mark.asyncio
async def test_merge(base_repository, mock_session):
    mock_model = MockModel()
    result = await base_repository.merge(mock_model)
    assert result == mock_model
    mock_session.merge.assert_called_once_with(mock_model)

@pytest.mark.asyncio
async def test_get(base_repository, mock_session):
    mock_model = MockModel()
    mock_session.get.return_value = mock_model
    pk = uuid4()
    result = await base_repository.get(pk)
    assert result == mock_model
    mock_session.get.assert_called_once_with(MockModel, pk, options=None)

@pytest.mark.asyncio
async def test_update(base_repository, mock_session):
    mock_session.scalars.return_value.all.return_value = [MockModel()]
    expressions = [MockModel.id == uuid4()]
    kwargs = {'name': 'new name'}
    result = await base_repository.update(*expressions, **kwargs)
    assert len(result) == 1
    mock_session.scalars.assert_called_once()

@pytest.mark.asyncio
async def test_delete(base_repository, mock_session):
    expressions = [MockModel.id == uuid4()]
    await base_repository.delete(*expressions)
    mock_session.execute.assert_called_once()

@pytest.mark.asyncio
async def test_find(base_repository, mock_session):
    mock_session.scalars.return_value.all.return_value = [MockModel()]
    expressions = [MockModel.id == uuid4()]
    result = await base_repository.find(*expressions)
    assert len(result) == 1
    mock_session.scalars.assert_called_once()

@pytest.mark.asyncio
async def test_find_one(base_repository, mock_session):
    mock_session.scalars.return_value.first.return_value = MockModel()
    expressions = [MockModel.id == uuid4()]
    result = await base_repository.find_one(*expressions)
    assert result is not None
    mock_session.scalars.assert_called_once()

@pytest.mark.asyncio
async def test_check_exists(base_repository, mock_session):
    mock_session.scalar.return_value = True
    expressions = [MockModel.id == uuid4()]
    result = await base_repository.check_exists(*expressions)
    assert result is True
    mock_session.scalar.assert_called_once()

@pytest.mark.asyncio
async def test_check_exists_false(base_repository, mock_session):
    mock_session.scalar.return_value = None
    expressions = [MockModel.id == uuid4()]
    result = await base_repository.check_exists(*expressions)
    assert result is False
    mock_session.scalar.assert_called_once()

def test_set_filter(base_repository):
    query = select(MockModel)
    expressions = [MockModel.id == 1]
    filtered_query = base_repository._set_filter(query, expressions)
    assert filtered_query.whereclause is not None

def test_set_filter_no_expressions(base_repository):
    query = select(MockModel)
    expressions = []
    filtered_query = base_repository._set_filter(query, expressions)
    assert filtered_query.whereclause is None

def test_set_additions(base_repository):
    query = select(MockModel)
    limit = 10
    offset = 5
    options = [selectinload(MockModel.id)]
    order = [MockModel.id]
    additions_query = base_repository._set_additions(query, limit, offset, options, order)
    assert additions_query._limit == limit
    assert additions_query._offset == offset
    assert additions_query._order_by_clauses is not None
    assert additions_query._with_options is not None

def test_set_additions_none(base_repository):
    query = select(MockModel)
    additions_query = base_repository._set_additions(query)
    assert additions_query._limit is None
    assert additions_query._offset is None
    assert additions_query._order_by_clauses == ()
    assert additions_query._with_options == ()

def test_set_filter_with_additions(base_repository):
    query = select(MockModel)
    expressions = [MockModel.id == 1]
    limit = 10
    offset = 5
    options = [selectinload(MockModel.id)]
    order = [MockModel.id]
    final_query = base_repository._set_filter_with_additions(query, expressions, limit, offset, options, order)
    assert final_query.whereclause is not None
    assert final_query._limit == limit
    assert final_query._offset == offset
    assert final_query._order_by_clauses is not None
    assert final_query._with_options is not None

def test_set_filter_with_additions_no_expressions(base_repository):
    query = select(MockModel)
    expressions = []
    limit = 10
    offset = 5
    options = [selectinload(MockModel.id)]
    order = [MockModel.id]
    final_query = base_repository._set_filter_with_additions(query, expressions, limit, offset, options, order)
    assert final_query.whereclause is None
    assert final_query._limit == limit
    assert final_query._offset == offset
    assert final_query._order_by_clauses is not None
    assert final_query._with_options is not None