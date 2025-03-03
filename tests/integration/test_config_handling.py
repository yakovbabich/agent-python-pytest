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

from examples.test_rp_logging import LOG_MESSAGE
from tests import REPORT_PORTAL_SERVICE
from tests.helpers import utils

TEST_LAUNCH_ID = 'test_launch_id'


@mock.patch(REPORT_PORTAL_SERVICE)
def test_rp_launch_id(mock_client_init):
    """Verify that RP plugin does not start/stop launch if 'rp_launch_id' set.

    :param mock_client_init: Pytest fixture
    """
    variables = dict()
    variables['rp_launch_id'] = TEST_LAUNCH_ID
    variables.update(utils.DEFAULT_VARIABLES.items())
    result = utils.run_pytest_tests(tests=['examples/test_simple.py'],
                                    variables=variables)

    assert int(result) == 0, 'Exit code should be 0 (no errors)'

    expect(
        mock_client_init.call_args_list[0][1]['launch_id'] == TEST_LAUNCH_ID)

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


@mock.patch(REPORT_PORTAL_SERVICE)
def test_rp_log_format(mock_client_init):
    log_format = '(%(name)s) %(message)s (%(filename)s:%(lineno)s)'
    variables = {'rp_log_format': log_format}
    variables.update(utils.DEFAULT_VARIABLES.items())

    mock_client = mock_client_init.return_value
    result = utils.run_tests_with_client(
        mock_client, ['examples/test_rp_logging.py'], variables=variables)

    assert int(result) == 0, 'Exit code should be 0 (no errors)'

    expect(mock_client.log.call_count == 1)
    message = mock_client.log.call_args_list[0][0][1]
    expect(len(message) > 0)
    expect(message == '(examples.test_rp_logging) ' + LOG_MESSAGE +
           ' (test_rp_logging.py:24)')
    assert_expectations()


@mock.patch(REPORT_PORTAL_SERVICE)
def test_rp_log_batch_payload_size(mock_client_init):
    log_size = 123456
    variables = {'rp_log_batch_payload_size': log_size}
    variables.update(utils.DEFAULT_VARIABLES.items())

    result = utils.run_pytest_tests(['examples/test_rp_logging.py'],
                                    variables=variables)
    assert int(result) == 0, 'Exit code should be 0 (no errors)'

    expect(mock_client_init.call_count == 1)

    constructor_args = mock_client_init.call_args_list[0][1]
    expect(constructor_args['log_batch_payload_size'] == log_size)
    assert_expectations()
