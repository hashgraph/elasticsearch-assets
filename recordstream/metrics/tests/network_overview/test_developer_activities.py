import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from network_overview.developer_activities import DeveloperActivities

# Sample data for testing
sample_records = [
    {"status": '22', "txn_type": 'CONTRACTCREATEINSTANCE', "consensusTimestamp": pd.Timestamp("2024-01-01 00:00:00"), "transaction_hash": "hash1", "payer": "payer1"},
    {"status": '22', "txn_type": 'CONTRACTUPDATEINSTANCE', "consensusTimestamp": pd.Timestamp("2024-01-01 00:01:00"), "transaction_hash": "hash2", "payer": "payer2"},
    {"status": '21', "txn_type": 'CONTRACTCREATEINSTANCE', "consensusTimestamp": pd.Timestamp("2024-01-01 00:02:00"), "transaction_hash": "hash3", "payer": "payer3"},
]

@pytest.fixture
def developer_activities():
    with patch('network_overview.developer_activities.BaseScript.__init__', return_value=None):
        developer_activities_instance = DeveloperActivities()
        developer_activities_instance.options = MagicMock()
        developer_activities_instance.options.input_file = 'input.json'
        developer_activities_instance.options.output_folder = 'output'
        developer_activities_instance.options.output_format = 'json'
        developer_activities_instance.options.log_level = 'INFO'
        developer_activities_instance.logger = MagicMock()
        return developer_activities_instance

def test_filter_records(developer_activities):
    result = developer_activities.filter_records(sample_records)
    expected = [
        {"status": '22', "txn_type": 'CONTRACTCREATEINSTANCE', "consensusTimestamp": pd.Timestamp("2024-01-01 00:00:00"), "transaction_hash": "hash1", "payer": "payer1"},
        {"status": '22', "txn_type": 'CONTRACTUPDATEINSTANCE', "consensusTimestamp": pd.Timestamp("2024-01-01 00:01:00"), "transaction_hash": "hash2", "payer": "payer2"}
    ]
    assert result == expected

def test_clean_records_df(developer_activities):
    df = pd.DataFrame([
        {"consensusTimestamp": pd.Timestamp("2024-01-01 00:00:00"), "txn_type": 'CONTRACTCREATEINSTANCE', "transaction_hash": "hash1", "payer": "payer1"},
        {"consensusTimestamp": pd.Timestamp("2024-01-01 00:01:45"), "txn_type": 'CONTRACTUPDATEINSTANCE', "transaction_hash": "hash2", "payer": "payer2"}
    ])
    result = developer_activities.clean_records_df(df)
    expected = df.copy()
    expected["rounded_timestamp"] = [pd.Timestamp("2024-01-01 00:00:00"), pd.Timestamp("2024-01-01 00:01:00")]
    expected["service"] = ['HSCS', 'HSCS']
    pd.testing.assert_frame_equal(result, expected)

def test_aggregated_by_service(developer_activities):
    df = pd.DataFrame([
        {"consensusTimestamp": pd.Timestamp("2024-01-01 00:00:00"), "rounded_timestamp": pd.Timestamp("2024-01-01 00:00:00"), "txn_type": 'CONTRACTCREATEINSTANCE', "transaction_hash": "hash1", "payer": "payer1", "service": "HSCS"},
        {"consensusTimestamp": pd.Timestamp("2024-01-01 00:01:00"), "rounded_timestamp": pd.Timestamp("2024-01-01 00:01:00"), "txn_type": 'CONTRACTUPDATEINSTANCE', "transaction_hash": "hash2", "payer": "payer2", "service": "HSCS"}
    ])
    result = developer_activities.aggregated_by_service(df)
    expected = pd.DataFrame([
        {"rounded_timestamp": pd.Timestamp("2024-01-01 00:00:00"), "service": "HSCS", "transaction_count": 1, "dev_count": 1},
        {"rounded_timestamp": pd.Timestamp("2024-01-01 00:01:00"), "service": "HSCS", "transaction_count": 1, "dev_count": 1}
    ])
    pd.testing.assert_frame_equal(result, expected)

def test_aggregated_by_network(developer_activities):
    df = pd.DataFrame([
        {"consensusTimestamp": pd.Timestamp("2024-01-01 00:00:00"), "rounded_timestamp": pd.Timestamp("2024-01-01 00:00:00"), "txn_type": 'CONTRACTCREATEINSTANCE', "transaction_hash": "hash1", "payer": "payer1", "service": "HSCS"},
        {"consensusTimestamp": pd.Timestamp("2024-01-01 00:01:00"), "rounded_timestamp": pd.Timestamp("2024-01-01 00:01:00"), "txn_type": 'CONTRACTUPDATEINSTANCE', "transaction_hash": "hash2", "payer": "payer2", "service": "HSCS"}
    ])
    result = developer_activities.aggregated_by_network(df)
    expected = pd.DataFrame([
        {"rounded_timestamp": pd.Timestamp("2024-01-01 00:00:00"), "transaction_count": 1, "dev_count": 1},
        {"rounded_timestamp": pd.Timestamp("2024-01-01 00:01:00"), "transaction_count": 1, "dev_count": 1}
    ])
    pd.testing.assert_frame_equal(result, expected)

def test_run(developer_activities):
    with patch.object(developer_activities, 'read_data', return_value=sample_records):
        with patch.object(developer_activities, 'write_df_to_file') as mock_write_df_to_file:
            developer_activities.run()
            assert mock_write_df_to_file.call_count == 2
