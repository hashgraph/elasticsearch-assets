import os
import sys
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock

from network_overview.transfer import NetworkOverview

# Sample data for testing
sample_records = [
    {
        'txn_type': 'CRYPTO_TRANSFER',
        'transaction_hash': 'hash1',
        'consensusTimestamp': pd.Timestamp('2024-01-01 00:00:00'),
        'payer': 'payer1',
        'transfer_list': [
            {'accountID': {'accountNum': 123}, 'amount': -100000000},
            {'accountID': {'accountNum': 456}, 'amount': 80000000},
            {'accountID': {'accountNum': 98}, 'amount': 10000000},  # network_fee
            {'accountID': {'accountNum': 5}, 'amount': 10000000},   # node_fee
        ],
        'transaction_fee': 1000000,
        'status': '22'
    },
    {
        'txn_type': 'TOKEN_TRANSFER',
        'transaction_hash': 'hash2',
        'consensusTimestamp': pd.Timestamp('2024-01-01 00:01:00'),
        'payer': 'payer2',
        'transfer_list': [
            {'accountID': {'accountNum': 123}, 'amount': -200000000},
            {'accountID': {'accountNum': 789}, 'amount': 170000000},
            {'accountID': {'accountNum': 98}, 'amount': 20000000},  # network_fee
            {'accountID': {'accountNum': 6}, 'amount': 10000000},   # node_fee
        ],
        'transaction_fee': 2000000,
        'status': '22'
    }
]


@pytest.fixture
def network_overview():
    with patch('network_overview.transfer.BaseScript.__init__', return_value=None):
        network_overview = NetworkOverview()
        network_overview.options = MagicMock()
        network_overview.logger = MagicMock()
        return network_overview

def test_map_txn_type(network_overview):
    assert network_overview.map_txn_type('CRYPTO_TRANSFER') == 'CRYPTO'
    assert network_overview.map_txn_type('CONSENSUS_SUBMIT_MESSAGE') == 'CONSENSUS'
    assert network_overview.map_txn_type('TOKEN_MINT') == 'TOKEN'
    assert network_overview.map_txn_type('NFT_CREATE') == 'NFT'
    assert network_overview.map_txn_type('CONTRACT_CALL') == 'CONTRACT'
    assert network_overview.map_txn_type('FILE_CREATE') == 'FILE'
    assert network_overview.map_txn_type('ETHEREUM_TRANSACTION') == 'ETHEREUM'
    assert network_overview.map_txn_type('NODESTAKE_UPDATE') == 'NODESTAKE'
    assert network_overview.map_txn_type('UNKNOWN_TYPE') == 'OTHER'

def test_classify_transfer_type(network_overview):
    assert network_overview.classify_transfer_type(1_500_000_000) == 'gigantic_txn'
    assert network_overview.classify_transfer_type(20_000_000) == 'huge_txns'
    assert network_overview.classify_transfer_type(20_000) == 'large_txn'
    assert network_overview.classify_transfer_type(1_500) == 'medium_txn'
    assert network_overview.classify_transfer_type(50) == 'small_txn'
    assert network_overview.classify_transfer_type(5) == 'micro_txn'


def test_transform_data(network_overview):
    transformed_data = network_overview.transform_data(sample_records)
    assert len(transformed_data) == 2
    
    # Check first record
    assert transformed_data[0]['txn_type'] == 'CRYPTO_TRANSFER'
    assert transformed_data[0]['group_txn_type'] == 'CRYPTO'
    assert transformed_data[0]['transaction_hash'] == 'hash1'
    assert transformed_data[0]['total_transfer'] == 1.0
    assert transformed_data[0]['transfer_type'] == 'micro_txn'
    assert transformed_data[0]['network_fee'] == 0.1
    assert transformed_data[0]['node_fee'] == 0.1
    assert transformed_data[0]['transaction_fee'] == 0.01

    # Check second record
    assert transformed_data[1]['txn_type'] == 'TOKEN_TRANSFER'
    assert transformed_data[1]['group_txn_type'] == 'TOKEN'
    assert transformed_data[1]['transaction_hash'] == 'hash2'
    assert transformed_data[1]['total_transfer'] == 2.0
    assert transformed_data[1]['transfer_type'] == 'micro_txn'
    assert transformed_data[1]['network_fee'] == 0.2
    assert transformed_data[1]['node_fee'] == 0.1
    assert transformed_data[1]['transaction_fee'] == 0.02

def test_clean_records_df(network_overview):
    transformed_data = network_overview.transform_data(sample_records)
    df = pd.DataFrame(transformed_data)
    df['consensusTimestamp'] = pd.to_datetime(df['consensusTimestamp'])
    cleaned_df = network_overview.clean_records_df(df)
    assert 'rounded_timestamp' in cleaned_df.columns
    assert cleaned_df['rounded_timestamp'].iloc[0] == pd.Timestamp('2024-01-01 00:00:00')

def test_overall_transfer(network_overview):
    transformed_data = network_overview.transform_data(sample_records)
    df = pd.DataFrame(transformed_data)
    df['consensusTimestamp'] = pd.to_datetime(df['consensusTimestamp'])
    cleaned_df = network_overview.clean_records_df(df)
    overall_df = network_overview.overall_transfer(cleaned_df)
    assert 'total_transfer' in overall_df.columns
    assert overall_df['total_transfer'].sum() == 3.0

def test_transfer_by_type(network_overview):
    transformed_data = network_overview.transform_data(sample_records)
    df = pd.DataFrame(transformed_data)
    df['consensusTimestamp'] = pd.to_datetime(df['consensusTimestamp'])
    cleaned_df = network_overview.clean_records_df(df)
    type_df = network_overview.transfer_by_type(cleaned_df)
    assert 'total_transfer' in type_df.columns
    assert type_df['total_transfer'].sum() == 3.0

def test_aggregate_by_payer(network_overview):
    transformed_data = network_overview.transform_data(sample_records)
    df = pd.DataFrame(transformed_data)
    df['consensusTimestamp'] = pd.to_datetime(df['consensusTimestamp'])
    cleaned_df = network_overview.clean_records_df(df)
    payer_df = network_overview.aggregate_by_payer(cleaned_df)
    assert 'total_transfer' in payer_df.columns
    assert payer_df['total_transfer'].sum() == 3.0

def test_aggregate_by_sender(network_overview):
    transformed_data = network_overview.transform_data(sample_records)
    df = pd.DataFrame(transformed_data)
    df['consensusTimestamp'] = pd.to_datetime(df['consensusTimestamp'])
    cleaned_df = network_overview.clean_records_df(df)
    sender_df = network_overview.aggregate_by_sender(cleaned_df)
    assert 'send_transfer' in sender_df.columns
    assert sender_df['send_transfer'].sum() == -3.0

def test_aggregate_by_receiver(network_overview):
    transformed_data = network_overview.transform_data(sample_records)
    df = pd.DataFrame(transformed_data)
    df['consensusTimestamp'] = pd.to_datetime(df['consensusTimestamp'])
    cleaned_df = network_overview.clean_records_df(df)
    receiver_df = network_overview.aggregate_by_receiver(cleaned_df)
    assert 'receive_transfer' in receiver_df.columns
    assert receiver_df['receive_transfer'].sum() == 2.5

def test_run(network_overview):
    with patch.object(network_overview, 'read_data', return_value=sample_records):
        with patch.object(network_overview, 'write_df_to_file') as mock_write_df_to_file:
            network_overview.run()
            assert mock_write_df_to_file.call_count == 5