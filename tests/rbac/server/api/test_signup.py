# Copyright 2018 Contributors to Hyperledger Sawtooth
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -----------------------------------------------------------------------------
"""Test the REST API endpoint"""
# pylint: disable=invalid-name,redefined-outer-name,unused-import

import requests
import pytest

from rbac.common.logs import getLogger
from tests.rbac.test.fixtures import url_base
from tests.rbac.test.fixtures import testdata
from tests.rbac.test.assertions import assert_api_error
from tests.rbac.test.assertions import assert_api_success

LOGGER = getLogger(__name__)


@pytest.mark.api
@pytest.mark.api_signup
@pytest.mark.parametrize(
    "data",
    [
        (
            {
                "name": testdata.name(),
                "username": testdata.username(),
                "email": testdata.email(),
                "password": testdata.password(),
            }
        )
    ],
)
def test_api_user_signup_good(url_base, data):
    """Test user signup with good data
    """
    url = url_base + "/api/users/"
    response = requests.post(url=url, headers=None, json=data)
    result = assert_api_success(response)
    assert result["data"]
    assert result["data"]["message"] == "Authorization successful"
    assert isinstance(result["data"]["user"], dict)
    assert result["data"]["user"]["email"] == data["email"]
    assert result["data"]["user"]["username"] == data["username"]
    assert result["data"]["user"]["name"] == data["name"]
    assert "password" not in result["data"]["user"]


@pytest.mark.api
@pytest.mark.api_signup
@pytest.mark.parametrize(
    "data, expected_error",
    [
        (
            {
                "username": testdata.username(),
                "email": testdata.email(),
                "password": testdata.password(),
            },
            "Bad Request: name field is required",
        ),
        (
            {
                "name": testdata.name(),
                "username": testdata.username(),
                "password": testdata.password(),
            },
            "Bad Request: email field is required",
        ),
        (
            {
                "name": testdata.name(),
                "username": testdata.username(),
                "email": testdata.email(),
            },
            "Bad Request: password field is required",
        ),
    ],
)
def test_api_user_signup_bad(url_base, data, expected_error):
    """Test user signup with bad data
    """
    url = url_base + "/api/users/"
    response = requests.post(url=url, headers=None, json=data)
    assert_api_error(response, expected_error)
