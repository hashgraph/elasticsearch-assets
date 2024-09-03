import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from network_overview.transaction_volume_by_node import NetworkOverview

# Sample data for testing
sample_records = [
    {"status": '22', "txn_type": 'type1', "consensusTimestamp": pd.Timestamp("2024-01-01 00:00:00"), "transaction_hash": "hash1", "node_id": "node1"},
    {"status": '22', "txn_type": 'type2', "consensusTimestamp": pd.Timestamp("2024-01-01 00:01:00"), "transaction_hash": "hash2", "node_id": "node2"},
    {"status": '21', "txn_type": 'type1', "consensusTimestamp": pd.Timestamp("2024-01-01 00:02:00"), "transaction_hash": "hash3", "node_id": "node1"},
]

@pytest.fixture
def network_overview():
    with patch('network_overview.transaction_volume_by_node.BaseScript.__init__', return_value=None):
        network_overview_instance = NetworkOverview()
        network_overview_instance.options = MagicMock()
        network_overview_instance.options.input_file = 'input.json'
        network_overview_instance.options.output_folder = 'output'
        network_overview_instance.options.output_format = 'json'
        network_overview_instance.options.log_level = 'INFO'
        network_overview_instance.logger = MagicMock()
        return network_overview_instance

def test_clean_records_df(network_overview):
    df = pd.DataFrame([
        {"consensusTimestamp": pd.Timestamp("2024-01-01 00:00:00"), "txn_type": 'type1', "transaction_hash": "hash1", "node_id": "node1"},
        {"consensusTimestamp": pd.Timestamp("2024-01-01 00:01:45"), "txn_type": 'type2', "transaction_hash": "hash2", "node_id": "node2"}
    ])
    result = network_overview.clean_records_df(df)
    expected = df.copy()
    expected["rounded_timestamp"] = [pd.Timestamp("2024-01-01 00:00:00"), pd.Timestamp("2024-01-01 00:01:00")]
    pd.testing.assert_frame_equal(result, expected)

def test_aggregate_recordstreams(network_overview):
    df = pd.DataFrame([
        {"status": '22', "txn_type": 'type1', "consensusTimestamp": pd.Timestamp("2024-01-01 00:00:00"), "transaction_hash": "hash1", "node_id": "node1", "rounded_timestamp": pd.Timestamp("2024-01-01 00:00:00")},
        {"status": '22', "txn_type": 'type2', "consensusTimestamp": pd.Timestamp("2024-01-01 00:01:00"), "transaction_hash": "hash2", "node_id": "node2", "rounded_timestamp": pd.Timestamp("2024-01-01 00:01:00")},
        {"status": '21', "txn_type": 'type1', "consensusTimestamp": pd.Timestamp("2024-01-01 00:02:00"), "transaction_hash": "hash3", "node_id": "node1", "rounded_timestamp": pd.Timestamp("2024-01-01 00:02:00")}
    ])
    result = network_overview.aggregate_recordstreams(df)
    expected = pd.DataFrame([
        {"rounded_timestamp": pd.Timestamp("2024-01-01 00:00:00"), "node_id": "node1", "transaction_hash": 1},
        {"rounded_timestamp": pd.Timestamp("2024-01-01 00:01:00"), "node_id": "node2", "transaction_hash": 1}
    ])
    pd.testing.assert_frame_equal(result, expected)

def test_run(network_overview):
    with patch.object(network_overview, 'read_data', return_value=sample_records):
        with patch.object(network_overview, 'write_df_to_file') as mock_write_df_to_file:
            network_overview.run()
            assert mock_write_df_to_file.call_count == 1

