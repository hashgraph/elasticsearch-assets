import pytest
import requests
from unittest.mock import patch, MagicMock

from utils.mirrornode_helper import (  # Replace `utils.mirrornode_helper` with the actual module name
    http_get_with_retry,
    get_mirrornode,
    get_mirrornode_token_list,
    get_mirrornode_token_balance,
    parse_token,
    parse_token_balance,
)

# Example logger fixture using MagicMock
@pytest.fixture
def logger():
    return MagicMock()

# Test http_get_with_retry function
def test_http_get_with_retry_success():
    url = "https://example.com"
    
    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        response = http_get_with_retry(url)
        assert response == mock_response
        mock_get.assert_called_once_with(url, timeout=10)

def test_get_mirrornode_failure(logger):
    method = "/api/v1/token"
    
    with patch("requests.get", side_effect=requests.exceptions.Timeout):
        response = get_mirrornode(method, logger)
        assert response == {"status": 0}
        logger.warning.assert_called_once_with("Failed to retrieve a response from the MirrorNode API.")

# Test get_mirrornode function
def test_get_mirrornode_success(logger):
    method = "/api/v1/token"
    
    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "success"}
        mock_get.return_value = mock_response
        
        response = get_mirrornode(method, logger)
        assert response == {"status": "success"}
        mock_get.assert_called_once()

def test_get_mirrornode_failure(logger):
    method = "/api/v1/token"
    
    with patch("requests.get", side_effect=requests.exceptions.Timeout):
        response = get_mirrornode(method, logger)
        assert response == {"status": 0}
        logger.warning.assert_called_once_with("Failed to retrieve a response from the MirrorNode API.")

# Test get_mirrornode_token_list function
def test_get_mirrornode_token_list_success(logger):
    token_api_endpoint = "/api/v1/tokens"
    mock_response_data = {
        "tokens": [{"token_id": "0.0.1234"}],
        "links": {"next": None}
    }
    
    with patch("utils.mirrornode_helper.get_mirrornode", return_value=mock_response_data):
        token_list = get_mirrornode_token_list(logger, token_api_endpoint)
        assert token_list == [{"token_id": "0.0.1234"}]
        logger.info.assert_called()

def test_get_mirrornode_token_list_exception(logger):
    token_api_endpoint = "/api/v1/tokens"
    
    with patch("utils.mirrornode_helper.get_mirrornode", side_effect=Exception("Test Exception")):
        token_list = get_mirrornode_token_list(logger, token_api_endpoint)
        assert token_list == []
        logger.warning.assert_called()

# Test get_mirrornode_token_balance function
def test_get_mirrornode_token_balance_success(logger):
    token_id = "0.0.1234"
    mock_response_data = {
        "balances": [{"account": "0.0.5678", "balance": 1000}],
        "links": {"next": None}
    }
    
    with patch("utils.mirrornode_helper.get_mirrornode", return_value=mock_response_data):
        token_balance = get_mirrornode_token_balance(logger, token_id)
        assert token_balance == [{"account": "0.0.5678", "balance": 1000}]
        logger.info.assert_called()

def test_get_mirrornode_token_balance_exception(logger):
    token_id = "0.0.1234"
    
    with patch("utils.mirrornode_helper.get_mirrornode", side_effect=Exception("Test Exception")):
        token_balance = get_mirrornode_token_balance(logger, token_id)
        assert token_balance is None
        logger.warning.assert_called()

# Test parse_token function
def test_parse_token():
    mirror_token_list = []
    response = [{"token_id": "0.0.1234", "admin_key": "test_key"}]
    
    parsed_list = parse_token(mirror_token_list, response)
    assert parsed_list == [{"token_id": "0.0.1234"}]  # admin_key should be removed

# Test parse_token_balance function
def test_parse_token_balance():
    token_balances = []
    response = {"balances": [{"account": "0.0.5678", "balance": 1000}]}
    
    parsed_balances = parse_token_balance(token_balances, response)
    assert parsed_balances == [{"account": "0.0.5678", "balance": 1000}]
