from unittest import mock

import pytest

from cicd.core.client import Client


class DummyModel(dict):
    pass


@pytest.fixture
def response_json():
    return {'one': 1, 'two': 2}


@pytest.fixture
def sut(bag, response_json):
    with mock.patch('requests.request', return_value=bag.response):
        bag.response.json.return_value = response_json
        yield Client().config(base_url='base_url', token='token')


def test_client_instance(sut: Client):
    assert sut == Client.instance
    assert sut == Client()


def test_client_config(sut: Client):
    assert sut.BASE_URL == 'base_url'
    assert sut.token == 'token'

    sut.config(base_url='new_base_url')
    assert sut.BASE_URL == 'new_base_url'
    assert sut.token == 'token'

    sut.config(token='new_token')
    assert sut.BASE_URL == 'new_base_url'
    assert sut.token == 'new_token'


def test_client_headers(sut: Client):
    assert sut.make_headers() == {'Authorization': 'Bearer token'}


def test_client_paging_params(sut: Client):
    assert sut.make_paging_params(10) == {'page': 1, 'per_page': 10}
    assert sut.make_paging_params((2, 10)) == {'page': 2, 'per_page': 10}


def test_client_request(sut: Client, bag):
    result = sut.request(endpoint='dummy')
    assert result == {'one': 1, 'two': 2}
    bag.response.raise_for_status.assert_called()
    bag.response.json.assert_called()


def test_client_request_model(sut: Client, bag):
    result = sut.request(endpoint='dummy', as_type=DummyModel)
    assert isinstance(result, DummyModel)


@pytest.mark.parametrize('response_json', [([{'one': 1}, {'two': 2}])])
def test_client_request_model_list(sut: Client, bag):
    result = sut.request(endpoint='dummy', as_type=DummyModel, to_list=True)
    assert isinstance(result, list)
    assert all(isinstance(x, DummyModel) for x in result)
