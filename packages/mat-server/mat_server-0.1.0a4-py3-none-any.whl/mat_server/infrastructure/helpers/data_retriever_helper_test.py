import pytest

from mat_server.domain import exceptions
from mat_server.infrastructure.helpers import DataRetrieverHelper


def test_get_value_with_error_syntax():
    data_retriever_helper = DataRetrieverHelper()
    with pytest.raises(exceptions.ValidationError, match='path 文法錯誤'):
        assert data_retriever_helper.get_value({}, '')
    with pytest.raises(exceptions.ValidationError, match='path 文法錯誤'):
        assert data_retriever_helper.get_value({}, '..')


def test_get_value_with_empty_data():
    data_retriever_helper = DataRetrieverHelper()
    assert data_retriever_helper.get_value({}, '.a') is None
    assert data_retriever_helper.get_value({}, '.a.b') is None
    assert data_retriever_helper.get_value({}, '.a.[2]') is None
    assert data_retriever_helper.get_value({}, '.a.[4].b') is None
    assert data_retriever_helper.get_value({}, '.[3]') is None
    assert data_retriever_helper.get_value([], '.[3]') is None


def test_get_value():
    data_retriever_helper = DataRetrieverHelper()
    assert data_retriever_helper.get_value({}, '.') == {}
    assert data_retriever_helper.get_value(None, '.') is None
    assert data_retriever_helper.get_value({'a': {'b': 3}}, '.a.b') == 3
    assert data_retriever_helper.get_value({'a': [0, 1, 2]}, '.a.[2]') == 2
    assert data_retriever_helper.get_value({'a': [0, 1, 2, 3, {'b': 5}]}, '.a.[4].b') == 5
    assert data_retriever_helper.get_value([0, 1, 2, 3], '.[3]') == 3
