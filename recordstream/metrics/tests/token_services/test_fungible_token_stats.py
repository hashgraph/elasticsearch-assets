import pytest
import pandas as pd
from unittest.mock import MagicMock, patch
from datetime import datetime
from token_services.fungible_token_stats import HTS  # Make sure to replace 'your_module_path' with the actual path


@pytest.fixture
def sample_records():
    return [
        {
            'status': '22',
            'txn_type': 'TOKEN_TRANSFER',
            'transaction_hash': 'abc123',
            'consensusTimestamp': datetime(2023, 6, 20, 12, 30),
            'token_number': 1001,
            'transfer_list': [{'accountID': {'accountNum': 1}, 'amount': -100}],
            'token_transfer_list': [
                {
                    'nftTransfers': None,
                    'token': {'tokenNum': 2001},
                    'transfers': [
                        {'accountID': {'accountNum': 1}, 'amount': -100},
                        {'accountID': {'accountNum': 2}, 'amount': 100}
                    ]
                }
            ]
        },
        {
            'status': '21',
            'txn_type': 'TOKEN_TRANSFER',
            'transaction_hash': 'def456',
            'consensusTimestamp': datetime(2023, 6, 20, 12, 31),
            'token_number': 1002,
            'transfer_list': None,
            'token_transfer_list': None
        }
    ]

@pytest.fixture
def hts_instance():
    with patch('token_services.fungible_token_stats.BaseScript.__init__', return_value=None):
        hts = HTS()
        hts.logger = MagicMock()
        hts.options = MagicMock()
        hts.options.input_file = "dummy_input_file"
        hts.options.output_folder = "dummy_output_folder"
        return hts

def test_transform_data(sample_records, hts_instance):
    simplified_records = hts_instance.transform_data(sample_records)
    expected_records = [
        {
            'txn_type': 'TOKEN_TRANSFER',
            'transaction_hash': 'abc123',
            'consensusTimestamp': datetime(2023, 6, 20, 12, 30),
            'token_number': 1001,
            'internal_token_number': 2001,
            'payer': [1],
            'sender': [1],
            'receiver': [2],
            'send_amount': -100,
            'receive_amount': 100
        }
    ]
    assert simplified_records == expected_records

def test_clean_records_df(hts_instance):
    sample_df = pd.DataFrame([
        {
            'txn_type': 'TOKEN_TRANSFER',
            'transaction_hash': 'abc123',
            'consensusTimestamp': datetime(2023, 6, 20, 12, 30),
            'token_number': 1001,
            'internal_token_number': 2001,
            'payer': [1],
            'sender': [1],
            'receiver': [2],
            'send_amount': -100,
            'receive_amount': 100
        },
        {
            'txn_type': 'TOKEN_TRANSFER',
            'transaction_hash': 'abc123',
            'consensusTimestamp': datetime(2023, 6, 20, 12, 30),
            'token_number': 1001,
            'internal_token_number': 2001,
            'payer': [1],
            'sender': [1],
            'receiver': [2],
            'send_amount': -100,
            'receive_amount': 100
        }
    ])
    cleaned_df = hts_instance.clean_records_df(sample_df)
    assert len(cleaned_df) == 1
    assert 'rounded_timestamp' in cleaned_df.columns

def test_aggregate_recordstreams_by_type(hts_instance):
    sample_df = pd.DataFrame([
        {
            'txn_type': 'TOKEN_TRANSFER',
            'transaction_hash': 'abc123',
            'consensusTimestamp': datetime(2023, 6, 20, 12, 30),
            'token_number': 1001,
            'internal_token_number': 2001,
            'send_amount': -100,
            'receive_amount': 100,
            'rounded_timestamp': datetime(2023, 6, 20, 12, 30)
        }
    ])
    aggregated_df = hts_instance.aggregate_recordstreams_by_type(sample_df)
    assert len(aggregated_df) == 1
    assert 'transaction_count' in aggregated_df.columns
    assert 'tps' in aggregated_df.columns

def test_aggregate_recordstreams_by_token(hts_instance):
    sample_df = pd.DataFrame([
        {
            'txn_type': 'TOKEN_TRANSFER',
            'transaction_hash': 'abc123',
            'consensusTimestamp': datetime(2023, 6, 20, 12, 30),
            'token_number': 1001,
            'internal_token_number': 2001,
            'payer': [1],
            'sender': [1],
            'receiver': [2],
            'send_amount': -100,
            'receive_amount': 100,
            'rounded_timestamp': datetime(2023, 6, 20, 12, 30)
        }
    ])
    aggregated_df = hts_instance.aggregate_recordstreams_by_token(sample_df)
    assert len(aggregated_df) == 1
    assert 'distinct_payers' in aggregated_df.columns
    assert 'distinct_senders' in aggregated_df.columns
    assert 'distinct_receivers' in aggregated_df.columns

def test_run_method(hts_instance, sample_records):
    with patch.object(hts_instance, 'read_data', return_value=sample_records):
        with patch.object(hts_instance, 'write_df_to_file') as mock_write_df_to_file:
            hts_instance.run()
            assert mock_write_df_to_file.call_count == 3
