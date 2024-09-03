import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from account_overview.active_account import Account

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
