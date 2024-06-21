import pytest
import pandas as pd
from unittest.mock import MagicMock, patch
from datetime import datetime
from token_services.non_fungible_token_stats import NFTS  # Replace 'your_module_path' with the actual path

@pytest.fixture
def sample_records():
    return [
        {
            'status': '22',
            'txn_type': 'NFT_TRANSFER',
            'transaction_hash': 'abc123',
            'consensusTimestamp': datetime(2023, 6, 20, 12, 30),
            'token_number': 1001,
            'transfer_list': [{'accountID': {'accountNum': 1}, 'amount': -100}],
            'token_transfer_list': [
                {
                    'nftTransfers': [
                        {'senderAccountID': {'accountNum': 1}, 'receiverAccountID': {'accountNum': 2}, 'serialNumber': 1}
                    ],
                    'token': {'tokenNum': 2001},
                    'transfers': []
                }
            ]
        },
        {
            'status': '21',
            'txn_type': 'NFT_TRANSFER',
            'transaction_hash': 'def456',
            'consensusTimestamp': datetime(2023, 6, 20, 12, 31),
            'token_number': 1002,
            'transfer_list': None,
            'token_transfer_list': None
        }
    ]

@pytest.fixture
def nfts_instance():
        with patch('token_services.non_fungible_token_stats.BaseScript.__init__', return_value=None):
            nfts = NFTS()
            nfts.logger = MagicMock()
            nfts.options = MagicMock()
            nfts.options.input_file = "dummy_input_file"
            nfts.options.output_folder = "dummy_output_folder"
            return nfts

def test_transform_data(nfts_instance, sample_records):
    simplified_records = nfts_instance.transform_data(sample_records)
    expected_records = [
        {
            'txn_type': 'NFT_TRANSFER',
            'transaction_hash': 'abc123',
            'consensusTimestamp': datetime(2023, 6, 20, 12, 30),
            'token_number': 1001,
            'internal_token_number': 2001,
            'payer': [1],
            'sender': [1],
            'receiver': [2],
            'series': [1]
        }
    ]
    assert simplified_records == expected_records

def test_clean_records_df(nfts_instance):
    sample_df = pd.DataFrame([
        {
            'txn_type': 'NFT_TRANSFER',
            'transaction_hash': 'abc123',
            'consensusTimestamp': datetime(2023, 6, 20, 12, 30),
            'token_number': 1001,
            'internal_token_number': 2001,
            'payer': [1],
            'sender': [1],
            'receiver': [2],
            'series': [1]
        },
        {
            'txn_type': 'NFT_TRANSFER',
            'transaction_hash': 'abc123',
            'consensusTimestamp': datetime(2023, 6, 20, 12, 30),
            'token_number': 1001,
            'internal_token_number': 2001,
            'payer': [1],
            'sender': [1],
            'receiver': [2],
            'series': [1]
        }
    ])
    cleaned_df = nfts_instance.clean_records_df(sample_df)
    assert len(cleaned_df) == 1
    assert 'rounded_timestamp' in cleaned_df.columns

def test_aggregate_recordstreams_by_type(nfts_instance):
    sample_df = pd.DataFrame([
        {
            'txn_type': 'NFT_TRANSFER',
            'transaction_hash': 'abc123',
            'consensusTimestamp': datetime(2023, 6, 20, 12, 30),
            'token_number': 1001,
            'internal_token_number': 2001,
            'rounded_timestamp': datetime(2023, 6, 20, 12, 30)
        }
    ])
    aggregated_df = nfts_instance.aggregate_recordstreams_by_type(sample_df)
    expected_columns = ['txn_type', 'transaction_count']
    assert all(column in aggregated_df.columns for column in expected_columns)

def test_aggregate_recordstreams_by_token(nfts_instance):
    sample_df = pd.DataFrame([
        {
            'txn_type': 'NFT_TRANSFER',
            'transaction_hash': 'abc123',
            'consensusTimestamp': datetime(2023, 6, 20, 12, 30),
            'token_number': 1001,
            'internal_token_number': 2001,
            'rounded_timestamp': datetime(2023, 6, 20, 12, 30)
        }
    ])
    aggregated_df = nfts_instance.aggregate_recordstreams_by_token(sample_df)
    expected_columns = ['internal_token_number', 'txn_type', 'transaction_count']
    assert all(column in aggregated_df.columns for column in expected_columns)

def test_aggregate_recordstreams_by_account(nfts_instance):
    sample_df = pd.DataFrame([
        {
            'txn_type': 'NFT_TRANSFER',
            'transaction_hash': 'abc123',
            'consensusTimestamp': datetime(2023, 6, 20, 12, 30),
            'token_number': 1001,
            'internal_token_number': 2001,
            'payer': [1],
            'sender': [1],
            'receiver': [2],
            'series': [1],
            'rounded_timestamp': datetime(2023, 6, 20, 12, 30)
        }
    ])
    aggregated_df = nfts_instance.aggregate_recordstreams_by_account(sample_df)
    expected_columns = ['accountNum', 'transaction_count', 'data_type']
    assert all(column in aggregated_df.columns for column in expected_columns)

def test_run_method(nfts_instance, sample_records, mocker):
    # Mock the methods used in run
    with patch.object(nfts_instance, 'read_data', return_value=sample_records):
        with patch.object(nfts_instance, 'write_df_to_file') as mock_write_df_to_file:
            nfts_instance.run()
            assert nfts_instance.write_df_to_file.call_count == 4  # One for synthetic data, three for aggregated data
