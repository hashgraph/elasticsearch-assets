import pytest
from unittest.mock import MagicMock, patch
from token_services.token_list import TokenList  # Replace 'your_module_path' with the actual path
import pandas as pd

@pytest.fixture
def token_list_instance():
    with patch('token_services.token_list.BaseScript.__init__', return_value=None):
        token_list = TokenList()
        token_list.logger = MagicMock()
        token_list.options = MagicMock()
        token_list.options.output_folder = "dummy_output_folder"
        return token_list

def test_get_token_list_success(token_list_instance, mocker):
    # Mock the mirrornode_helper.get_mirrornode_token_list method
    mock_tokens = [{'token_id': '0.0.1', 'name': 'Token1'}, {'token_id': '0.0.2', 'name': 'Token2'}]
    mocker.patch('metrics.utils.mirrornode_helper.get_mirrornode_token_list', return_value=mock_tokens)

    tokens = token_list_instance.get_token_list()
    assert tokens == mock_tokens
    token_list_instance.logger.info.assert_called_with("Getting token list")

def test_get_token_list_exception(token_list_instance, mocker):
    # Mock the mirrornode_helper.get_mirrornode_token_list method to raise an exception
    mocker.patch('metrics.utils.mirrornode_helper.get_mirrornode_token_list', side_effect=Exception("Test Exception"))

    tokens = token_list_instance.get_token_list()
    assert tokens is None
    token_list_instance.logger.error.assert_called_with("Exception: Test Exception")


def test_run_failure(token_list_instance, mocker):
    # Mock the get_token_list to return None
    mocker.patch.object(token_list_instance, 'get_token_list', return_value=None)

    token_list_instance.run()

    token_list_instance.logger.info.assert_called_with("Getting token list")
    token_list_instance.logger.error.assert_called_with("Failed to get token list")
