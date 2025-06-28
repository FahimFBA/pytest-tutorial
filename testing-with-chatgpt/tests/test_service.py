import unittest.mock as mock

import pytest
import requests

import source.service as service


@mock.patch("source.service.get_user_from_db")
def test_get_user_from_db(mock_get_user_from_db):
    mock_get_user_from_db.return_value = "Mocked Alice"
    user_name = service.get_user_from_db(1)
    assert user_name == "Mocked Alice"
    pass


@mock.patch("requests.get")
def test_get_users(mock_get):
    mock_response = mock.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"id": 1,
                                       "name": "John Doe",
                                       "username": "JohnDoe",
                                       "email": "johndoe@gmail.com",
                                       "address": {
                                           "street": "street",
                                           "suite": "suite",
                                           "city": "city",
                                           "zipcode": "12345-9845",
                                           "geo": {
                                               "lat": "-65.1554",
                                               "lng": "42.1459"
                                           }
                                       }
                                       }
    mock_get.return_value = mock_response
    data = service.get_users()
    assert data == {"id": 1,
                    "name": "John Doe",
                    "username": "JohnDoe",
                    "email": "johndoe@gmail.com",
                    "address": {
                        "street": "street",
                        "suite": "suite",
                        "city": "city",
                        "zipcode": "12345-9845",
                        "geo": {
                            "lat": "-65.1554",
                            "lng": "42.1459"
                        }
                    }
                    }
    pass


@mock.patch("requests.get")
def test_get_users_error(mock_get):
    mock_response = mock.Mock()
    mock_response.status_code = 400
    mock_get.return_value = mock_response
    with pytest.raises(requests.HTTPError):
        service.get_users()