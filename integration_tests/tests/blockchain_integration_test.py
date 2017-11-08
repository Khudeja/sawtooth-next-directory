# Copyright 2017 Intel Corporation
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

from base64 import b64decode
import logging
import time
import unittest
from uuid import uuid4
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError

from sawtooth_cli.rest_client import RestClient

import sawtooth_signing as signing

from rbac_addressing import addresser
from rbac_transaction_creation.protobuf import user_state_pb2
from rbac_transaction_creation.common import Key
from rbac_transaction_creation.user_transaction_creation import create_user


LOGGER = logging.getLogger(__name__)


BATCHER_PRIVATE_KEY = signing.generate_privkey()
BATCHER_PUBLIC_KEY = signing.generate_pubkey(BATCHER_PRIVATE_KEY)

BATCHER_KEY = Key(public_key=BATCHER_PUBLIC_KEY,
                  private_key=BATCHER_PRIVATE_KEY)


def wait_until_status(url, status_code=200, tries=5):
    """Pause the program until the given url returns the required status.
    Args:
        url (str): The url to query.
        status_code (int, optional): The required status code. Defaults to 200.
        tries (int, optional): The number of attempts to request the url for
            the given status. Defaults to 5.
    Raises:
        AssertionError: If the status is not received in the given number of
            tries.
    """
    attempts = tries
    while attempts > 0:
        try:
            response = urlopen(url)
            if response.getcode() == status_code:
                return

        except HTTPError as err:
            if err.code == status_code:
                return

            LOGGER.debug('failed to read url: %s', str(err))
        except URLError as err:
            LOGGER.debug('failed to read url: %s', str(err))

        sleep_time = (tries - attempts + 1) * 2
        LOGGER.debug('Retrying in %s secs', sleep_time)
        time.sleep(sleep_time)

        attempts -= 1

    raise AssertionError(
        "{} is not available within {} attempts".format(url, tries))


def wait_for_rest_apis(endpoints, tries=5):
    """Pause the program until all the given REST API endpoints are available.
    Args:
        endpoints (list of str): A list of host:port strings.
        tries (int, optional): The number of attempts to request the url for
            availability.
    """

    for endpoint in endpoints:
        wait_until_status(
            'http://{}/blocks'.format(endpoint),
            status_code=200,
            tries=tries)


class TestBlockchain(unittest.TestCase):

    def test_blockchain(self):
        """Tests that the validation rules within the transaction processor
        are applied correctly.

        Notes:
            1. User
                CreateUser Validation rules:
                - Public key given for manager must be in state as a User.
                - User must not already exist.
                - The signing public key must belong to the user or manager.
                - The User must have a name longer than 4 characters.
                Create 5 Users,
                                user1
                                / \
                               /   \
                         user2a    user2b
                         /              \
                        /                \
                      user3a              user3b

                UpdateUserManager Validation rules:

        """

        wait_for_rest_apis(['rest-api:8080'])

        key1, user1 = make_key_and_user_name()

        client = RBACClient('http://rest-api:8080')
        self.assertEqual(
            client.create_user(
                key=key1,
                user_name=user1,
                user_id=key1.public_key)[0]['status'],
            'COMMITTED')

        key2a, user2a = make_key_and_user_name()

        self.assertEqual(
            client.create_user(
                key=key1,
                user_name=user2a,
                user_id=key2a.public_key,
                manager_ids=[key1.public_key])[0]['status'],
            'COMMITTED')

        key3a, user3a = make_key_and_user_name()

        key2b, user2b = make_key_and_user_name()

        self.assertEqual(
            client.create_user(
                key=key3a,
                user_name=user2b,
                user_id=key2b.public_key,
                manager_ids=[key3a.public_key])[0]['status'],
            'INVALID',
            "The transaction is invalid because the public key given for "
            "the manager does not exist in state.")

        self.assertEqual(
            client.create_user(
                key=key2a,
                user_name=user1,
                user_id=key1.public_key,
                manager_ids=[key2a.public_key, key1.public_key])[0]['status'],
            'INVALID',
            "The transaction is invalid because the User already exists.")

        self.assertEqual(
            client.create_user(
                key=key2a,
                user_name=user2b,
                user_id=key2b.public_key,
                manager_ids=[key3a.public_key])[0]['status'],
            'INVALID',
            "The signing key does not belong to the user or manager.")

        key_invalid, user_invalid = make_key_and_user_name()

        self.assertEqual(
            client.create_user(
                key=key_invalid,
                user_name=user_invalid[:4],
                user_id=key_invalid.public_key,
                manager_ids=None)[0]['status'],
            'INVALID',
            "The User's name must be at least 5 characters long.")

        self.assertEqual(
            client.create_user(
                key=key2a,
                user_name=user3a,
                user_id=key3a.public_key,
                manager_ids=[key2a.public_key, key1.public_key])[0]['status'],
            'COMMITTED')

        self.assertEqual(
            client.create_user(
                key=key1,
                user_name=user2b,
                user_id=key2b.public_key,
                manager_ids=[key1.public_key])[0]['status'],
            'COMMITTED')

        key3b, user3b = make_key_and_user_name()

        self.assertEqual(
            client.create_user(
                key=key3b,
                user_name=user3b,
                user_id=key3b.public_key,
                manager_ids=[key2b.public_key, key1.public_key])[0]['status'],
            'COMMITTED')

        state_items = client.return_state()
        self.assertEqual(len(state_items), 5, "There are 5 users in state.")


class RBACClient(object):

    def __init__(self, url):
        self._client = RestClient(base_url=url)

    def return_state(self):
        items = []
        for item in self._client.list_state(subtree=addresser.NS)['data']:
            if addresser.address_is(item['address']) == addresser.AddressSpace.USER:
                user_container = user_state_pb2.UserContainer()
                user_container.ParseFromString(b64decode(item['data']))
                items.append((user_container, addresser.AddressSpace.USER))
        return items

    def create_user(self, key, user_name, user_id, manager_ids=None):
        batch_list, signature = create_user(key,
                                            BATCHER_KEY,
                                            user_name,
                                            user_id,
                                            uuid4().hex,
                                            manager_ids)
        self._client.send_batches(batch_list)
        return self._client.get_statuses([signature], wait=10)


def make_key_and_user_name():
    private_key = signing.generate_privkey()
    pubkey = signing.generate_pubkey(private_key)

    key = Key(public_key=pubkey, private_key=private_key)
    return key, uuid4().hex