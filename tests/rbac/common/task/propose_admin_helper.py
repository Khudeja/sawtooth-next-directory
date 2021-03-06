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
"""Propose Task Admin Test Helper"""
# pylint: disable=no-member

import logging
import random

from rbac.common import rbac
from rbac.common import protobuf
from tests.rbac.common.assertions import TestAssertions
from tests.rbac.common.user.create_user_helper import CreateUserTestHelper
from tests.rbac.common.task.create_task_helper import CreateTaskTestHelper

LOGGER = logging.getLogger(__name__)


class TestHelper(TestAssertions):
    """A minimal test helper required by this test helper"""

    def __init__(self, *args, **kwargs):
        TestAssertions.__init__(self, *args, **kwargs)
        self.user = CreateUserTestHelper()
        self.task = CreateTaskTestHelper()


# pylint: disable=invalid-name
helper = TestHelper()


class ProposeTaskAdminTestHelper(TestAssertions):
    """Propose Task Admin Test Helper"""

    def id(self):
        return rbac.addresser.proposal.unique_id()

    def reason(self):
        """Get a random reason"""
        return "Because" + str(random.randint(10000, 100000))

    def create(self):
        """A user creates an add task admin proposal
        to add themselves as an admin to a task"""
        task, task_owner, task_owner_key = helper.task.create()
        user, user_key = helper.user.create()
        proposal_id = self.id()
        reason = self.reason()
        message = rbac.task.admin.propose.make(
            proposal_id=proposal_id,
            task_id=task.task_id,
            user_id=user.user_id,
            reason=reason,
            metadata=None,
        )
        proposal, status = rbac.task.admin.propose.create(
            signer_keypair=user_key,
            message=message,
            object_id=task.task_id,
            related_id=user.user_id,
        )
        self.assertStatusSuccess(status)
        self.assertIsInstance(proposal, protobuf.proposal_state_pb2.Proposal)
        self.assertEqual(
            proposal.proposal_type, protobuf.proposal_state_pb2.Proposal.ADD_TASK_ADMIN
        )
        self.assertEqual(proposal.proposal_id, proposal_id)
        self.assertEqual(proposal.object_id, task.task_id)
        self.assertEqual(proposal.related_id, user.user_id)
        self.assertEqual(proposal.opener, user.user_id)
        self.assertEqual(proposal.open_reason, reason)
        return proposal, task, task_owner, task_owner_key, user, user_key
