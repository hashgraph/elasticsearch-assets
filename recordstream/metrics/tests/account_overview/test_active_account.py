import json
import pytest
import pandas as pd
from unittest.mock import mock_open, patch, MagicMock
from account_overview.active_account import Account
from account_overview.model import Txn
from utils.common import BaseScript

sample_records = [
    {"transaction_hash": "hash1", "consensusTimestamp": pd.Timestamp("2024-01-01 00:00:00"), "payer": 1, "txn_sign_keys": ["key1"], "transfer_list": None},
    {"transaction_hash": "hash2", "consensusTimestamp": pd.Timestamp("2024-01-01 00:01:00"), "payer": 2, "txn_sign_keys": ["key2"], "transfer_list": [
        {"accountID": {"accountNum": 2}},
        {"accountID": {"accountNum": 3}},
        {"accountID": {"accountNum": 4}}
    ]}
]

@pytest.fixture
def account():
    with patch('account_overview.active_account.BaseScript.__init__', return_value=None):
        account_instance = Account()
        account_instance.options = MagicMock()
        account_instance.options.input_file = 'input.json'
        account_instance.options.output_folder = 'output'
        account_instance.options.output_format = 'json'
        account_instance.options.log_level = 'INFO'
        account_instance.logger = MagicMock()
        return account_instance

def test_transform_data(account):
    result = account.transform_data(sample_records)
    expected = [
        {"consensusTimestamp": pd.Timestamp("2024-01-01 00:00:00"), "accountNum": 1},
        {"consensusTimestamp": pd.Timestamp("2024-01-01 00:01:00"), "accountNum": 2},
        {"consensusTimestamp": pd.Timestamp("2024-01-01 00:01:00"), "accountNum": 3},
        {"consensusTimestamp": pd.Timestamp("2024-01-01 00:01:00"), "accountNum": 4}
    ]
    assert result == expected

def test_transform_data_payer_ec_key(account):
    result = account.transform_data_payer_ec_key(sample_records)
    expected = [
        {"transaction_hash": "hash1", "consensusTimestamp": pd.Timestamp("2024-01-01 00:00:00"), "accountNum": 1, "key_type": ["key1"]},
        {"transaction_hash": "hash2", "consensusTimestamp": pd.Timestamp("2024-01-01 00:01:00"), "accountNum": 2, "key_type": ["key2"]},
        {"transaction_hash": "hash2", "consensusTimestamp": pd.Timestamp("2024-01-01 00:01:00"), "accountNum": 3, "key_type": ["key2"]},
        {"transaction_hash": "hash2", "consensusTimestamp": pd.Timestamp("2024-01-01 00:01:00"), "accountNum": 4, "key_type": ["key2"]}
    ]
    assert result == expected

def test_clean_records_df(account):
    df = pd.DataFrame([
        {"consensusTimestamp": pd.Timestamp("2024-01-01 00:00:00"), "accountNum": 1},
        {"consensusTimestamp": pd.Timestamp("2024-01-01 00:01:45"), "accountNum": 2}
    ])
    result = account.clean_records_df(df)
    expected = df.copy()
    expected["rounded_timestamp"] = [pd.Timestamp("2024-01-01 00:00:00"), pd.Timestamp("2024-01-01 00:01:00")]
    pd.testing.assert_frame_equal(result, expected)

def test_aggregate_recordstreams(account):
    df = pd.DataFrame([
        {"consensusTimestamp": pd.Timestamp("2024-01-01 00:00:00"), "rounded_timestamp": pd.Timestamp("2024-01-01 00:00:00"), "accountNum": 1},
        {"consensusTimestamp": pd.Timestamp("2024-01-01 00:01:00"), "rounded_timestamp": pd.Timestamp("2024-01-01 00:01:00"), "accountNum": 2},
        {"consensusTimestamp": pd.Timestamp("2024-01-01 00:01:00"), "rounded_timestamp": pd.Timestamp("2024-01-01 00:01:00"), "accountNum": 3}
    ])
    result = account.aggregate_recordstreams(df)
    expected = pd.DataFrame([
        {"rounded_timestamp": pd.Timestamp("2024-01-01 00:00:00"), "accountNum": 1},
        {"rounded_timestamp": pd.Timestamp("2024-01-01 00:01:00"), "accountNum": 2}
    ])
    pd.testing.assert_frame_equal(result, expected)

def test_unique_account(account):
    df = pd.DataFrame([
        {"accountNum": 1},
        {"accountNum": 2},
        {"accountNum": 2},
        {"accountNum": 3}
    ])
    result = account.unique_account(df)
    expected = [1, 2, 3]
    assert sorted(result) == sorted(expected)

def test_aggregated_recordstreams_payer_ec_key(account):
    df = pd.DataFrame([
        {"transaction_hash": "hash1", "accountNum": 1, "key_type": ["key1"]},
        {"transaction_hash": "hash2", "accountNum": 2, "key_type": ["key2"]},
        {"transaction_hash": "hash3", "accountNum": 3, "key_type": ["key2"]}
    ])
    result = account.aggregated_recordstreams_payer_ec_key(df)
    expected = pd.DataFrame([
        {"key_type": "key1", "transaction_count": 1, "account_count": 1},
        {"key_type": "key2", "transaction_count": 2, "account_count": 2}
    ])
    pd.testing.assert_frame_equal(result, expected)


def test_run(account):
    # Create a mock DataFrame that matches the expected structure
    records_df_mock = pd.DataFrame([
        {"transaction_hash": "hash1", "consensusTimestamp": pd.Timestamp("2024-01-01 00:00:00"), "accountNum": 1, "txn_sign_keys": ["key1"]},
        {"transaction_hash": "hash2", "consensusTimestamp": pd.Timestamp("2024-01-01 00:01:00"), "accountNum": 2, "txn_sign_keys": ["key2"]},
        {"transaction_hash": "hash2", "consensusTimestamp": pd.Timestamp("2024-01-01 00:01:00"), "accountNum": 3, "txn_sign_keys": ["key2"]},
        {"transaction_hash": "hash2", "consensusTimestamp": pd.Timestamp("2024-01-01 00:01:00"), "accountNum": 4, "txn_sign_keys": ["key2"]}
    ])

    # Mock the methods that will be called in the run method
    with patch.object(Account, 'read_data', return_value=sample_records) as mock_read_data, \
         patch.object(Account, 'rcdstreams_to_pd_df', return_value=records_df_mock) as mock_rcdstreams_to_pd_df, \
         patch.object(Account, 'clean_records_df', side_effect=lambda x: x) as mock_clean_records_df, \
         patch.object(Account, 'aggregate_recordstreams', return_value=pd.DataFrame({"rounded_timestamp": [pd.Timestamp("2024-01-01 00:00:00")], "accountNum": [1]})) as mock_aggregate_recordstreams, \
         patch.object(Account, 'aggregated_recordstreams_payer_ec_key', return_value=pd.DataFrame({"key_type": ["key1"], "transaction_count": [1], "account_count": [1]})) as mock_aggregated_recordstreams_payer_ec_key, \
         patch.object(Account, 'write_df_to_file') as mock_write_df_to_file, \
         patch('account_overview.active_account.open', mock_open()) as mock_file:

        account.run()

        # Check that read_data was called with the correct arguments
        mock_read_data.assert_called_once_with('input.json', Txn)

        # Check that the transformation methods were called with correct DataFrames
        mock_rcdstreams_to_pd_df.assert_called()
        mock_clean_records_df.assert_called()
        mock_aggregate_recordstreams.assert_called()
        mock_aggregated_recordstreams_payer_ec_key.assert_called()

        # Check that write_df_to_file was called with the correct arguments
        mock_write_df_to_file.assert_any_call('output/active_account_active_account', mock_aggregate_recordstreams.return_value)
        mock_write_df_to_file.assert_any_call('output/active_account_ec_account', mock_aggregated_recordstreams_payer_ec_key.return_value)

        # Check that the file for unique accounts was opened and written to
        mock_file.assert_called_with('output/unique_active_accounts.json', 'w')
        mock_file().write.assert_called()

        # Ensure logger methods were called
        account.logger.info.assert_called()