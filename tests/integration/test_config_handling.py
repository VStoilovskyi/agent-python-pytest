"""This module includes integration tests for configuration parameters."""
#  Copyright (c) 2022 https://reportportal.io .
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#  https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License
from delayed_assert import expect, assert_expectations
from six.moves import mock

from tests import REPORT_PORTAL_SERVICE
from tests.helpers import utils


@mock.patch(REPORT_PORTAL_SERVICE)
def test_rp_launch_id(mock_client_init):
    """Verify that RP plugin does not start/stop launch if 'rp_launch_id' set.

    :param mock_client_init: Pytest fixture
    """
    variables = dict()
    variables['rp_launch_id'] = "test_launch_id"
    variables.update(utils.DEFAULT_VARIABLES.items())
    result = utils.run_pytest_tests(tests=['examples/test_simple.py'],
                                    variables=variables)

    assert int(result) == 0, 'Exit code should be 0 (no errors)'

    mock_client = mock_client_init.return_value
    expect(mock_client.start_launch.call_count == 0,
           '"start_launch" method was called')
    expect(mock_client.finish_launch.call_count == 0,
           '"finish_launch" method was called')

    start_call_args = mock_client.start_test_item.call_args_list
    finish_call_args = mock_client.finish_test_item.call_args_list

    expect(len(start_call_args) == len(finish_call_args))
    assert_expectations()


@mock.patch(REPORT_PORTAL_SERVICE)
def test_rp_parent_item_id(mock_client_init):
    """Verify RP set Parent ID for root items if 'rp_parent_item_id' set.

    :param mock_client_init: Pytest fixture
    """
    parent_id = "parent_id"
    variables = dict()
    variables['rp_parent_item_id'] = parent_id
    variables.update(utils.DEFAULT_VARIABLES.items())
    result = utils.run_pytest_tests(tests=['examples/test_simple.py'],
                                    variables=variables)

    assert int(result) == 0, 'Exit code should be 0 (no errors)'

    mock_client = mock_client_init.return_value
    expect(mock_client.start_launch.call_count == 1,
           '"start_launch" method was not called')
    expect(mock_client.finish_launch.call_count == 1,
           '"finish_launch" method was not called')

    start_call_args = mock_client.start_test_item.call_args_list
    finish_call_args = mock_client.finish_test_item.call_args_list

    expect(len(start_call_args) == len(finish_call_args))
    expect(start_call_args[0][1]["parent_item_id"] == parent_id)
    assert_expectations()


@mock.patch(REPORT_PORTAL_SERVICE)
def test_rp_parent_item_id_and_rp_launch_id(mock_client_init):
    """Verify RP handles both conf props 'rp_parent_item_id' & 'rp_launch_id'.

    :param mock_client_init: Pytest fixture
    """
    parent_id = "parent_id"
    variables = dict()
    variables['rp_parent_item_id'] = parent_id
    variables['rp_launch_id'] = "test_launch_id"
    variables.update(utils.DEFAULT_VARIABLES.items())
    result = utils.run_pytest_tests(tests=['examples/test_simple.py'],
                                    variables=variables)

    assert int(result) == 0, 'Exit code should be 0 (no errors)'

    mock_client = mock_client_init.return_value
    expect(mock_client.start_launch.call_count == 0,
           '"start_launch" method was called')
    expect(mock_client.finish_launch.call_count == 0,
           '"finish_launch" method was called')

    start_call_args = mock_client.start_test_item.call_args_list
    finish_call_args = mock_client.finish_test_item.call_args_list

    expect(len(start_call_args) == len(finish_call_args))
    expect(start_call_args[0][1]["parent_item_id"] == parent_id)
    assert_expectations()
