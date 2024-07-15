import pytest
import pandas as pd
from unittest.mock import patch, MagicMock

from smart_contract_services.sc_stats import SmartContract

@pytest.fixture
def smart_contract():
    with patch('smart_contract_services.sc_stats.BaseScript.__init__', return_value=None):
        smart_contract = SmartContract()
        smart_contract.options = MagicMock()
        smart_contract.logger = MagicMock()
        return smart_contract

@pytest.fixture
def sample_records():
    return [
        {
            'txn_type': 'CONTRACTCALL',
            'transaction_hash': 'hash1',
            'consensusTimestamp': pd.Timestamp('2024-01-01 00:00:00'),
            'contractNum': 123,
            'gasUsed': 21000,
            'payer': 123,
            'transfer_list': [
                {'accountID': {'accountNum': 123}, 'amount': -100000000},
                {'accountID': {'accountNum': 456}, 'amount': 100000000}
            ],
            'status': '22',
            'contract_call_result': {
                'contractID': {'contractNum': 123},
                'gasUsed': 21000,
                'logInfo': [],
                'createdContractIDs': [456]
            },
            'contract_create_result': None
        },
        {
            'txn_type': 'ETHEREUMTRANSACTION',
            'transaction_hash': 'hash2',
            'consensusTimestamp': pd.Timestamp('2024-01-01 00:01:00'),
            'contractNum': 789,
            'gasUsed': 30000,
            'payer': 789,
            'transfer_list': [
                {'accountID': {'accountNum': 789}, 'amount': -200000000},
                {'accountID': {'accountNum': 123}, 'amount': 200000000}
            ],
            'status': '22',
            'contract_call_result': None,
            'contract_create_result': {
                'contractID': {'contractNum': 789},
                'gasUsed': 30000,
                'logInfo': [],
                'createdContractIDs': [123]
            }
        }
    ]

def test_transform_data(smart_contract, sample_records):
    transformed_data = smart_contract.transform_data(sample_records)
    assert len(transformed_data) == 2

    # Check first record
    record1 = transformed_data[0]
    assert record1['txn_type'] == 'CONTRACTCALL'
    assert record1['transaction_hash'] == 'hash1'
    assert record1['contract_number'] == 123
    assert record1['gasUsed'] == 21000
    assert record1['payer'] == [123]
    assert record1['other_associated_account'] == [456]
    assert record1['internal_contract_number'] == [123]
    assert record1['created_contract_id'] == [456]

    # Check second record
    record2 = transformed_data[1]
    assert record2['txn_type'] == 'ETHEREUMTRANSACTION'
    assert record2['transaction_hash'] == 'hash2'
    assert record2['contract_number'] == 789
    assert record2['gasUsed'] == 30000
    assert record2['payer'] == [789]
    assert record2['other_associated_account'] == [123]
    assert record2['internal_contract_number'] == [789]

def test_clean_records_df(smart_contract, sample_records):
    transformed_data = smart_contract.transform_data(sample_records)
    records_df = pd.DataFrame(transformed_data)
    records_df['consensusTimestamp'] = pd.to_datetime(records_df['consensusTimestamp'])
    cleaned_df = smart_contract.clean_records_df(records_df)
    assert 'rounded_timestamp' in cleaned_df.columns
    assert cleaned_df['rounded_timestamp'].iloc[0] == pd.Timestamp('2024-01-01 00:00:00')

def test_aggregate_recordstreams_by_type(smart_contract, sample_records):
    transformed_data = smart_contract.transform_data(sample_records)
    records_df = pd.DataFrame(transformed_data)
    records_df['consensusTimestamp'] = pd.to_datetime(records_df['consensusTimestamp'])
    cleaned_df = smart_contract.clean_records_df(records_df)
    type_df = smart_contract.aggregate_recordstreams_by_type(cleaned_df)
    assert 'transaction_count' in type_df.columns
    assert type_df['transaction_count'].sum() == 2

def test_aggregate_recordstreams_by_contract(smart_contract, sample_records):
    transformed_data = smart_contract.transform_data(sample_records)
    records_df = pd.DataFrame(transformed_data)
    records_df['consensusTimestamp'] = pd.to_datetime(records_df['consensusTimestamp'])
    cleaned_df = smart_contract.clean_records_df(records_df)
    contract_df = smart_contract.aggregate_recordstreams_by_contract(cleaned_df)
    assert 'transaction_count' in contract_df.columns
    assert contract_df['transaction_count'].sum() == 2

def test_aggregate_recordstreams_by_account_contract(smart_contract, sample_records):
    transformed_data = smart_contract.transform_data(sample_records)
    records_df = pd.DataFrame(transformed_data)
    records_df['consensusTimestamp'] = pd.to_datetime(records_df['consensusTimestamp'])
    cleaned_df = smart_contract.clean_records_df(records_df)
    account_contract_df = smart_contract.aggregate_recordstreams_by_account_contract(cleaned_df)
    assert 'transaction_count' in account_contract_df.columns
    assert account_contract_df['transaction_count'].sum() == 2

def test_aggregate_recordstreams_by_account(smart_contract, sample_records):
    transformed_data = smart_contract.transform_data(sample_records)
    records_df = pd.DataFrame(transformed_data)
    records_df['consensusTimestamp'] = pd.to_datetime(records_df['consensusTimestamp'])
    cleaned_df = smart_contract.clean_records_df(records_df)
    account_df = smart_contract.aggregate_recordstreams_by_account(cleaned_df)
    assert 'transaction_count' in account_df.columns
    assert account_df['transaction_count'].sum() == 2

def test_run(smart_contract, sample_records):
    with patch.object(smart_contract, 'read_data', return_value=sample_records):
        with patch.object(smart_contract, 'write_df_to_file') as mock_write_df_to_file:
            smart_contract.run()
            assert mock_write_df_to_file.call_count == 5
