import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from consensus_services.hcs_stats import HCSServices

# Sample data for testing
sample_records = [
    {"status": '22', "txn_type": 'CONSENSUSCREATE', "consensusTimestamp": pd.Timestamp("2024-01-01 00:00:00")},
    {"status": '22', "txn_type": 'CONSENSUSSUBMITMESSAGE', "consensusTimestamp": pd.Timestamp("2024-01-01 00:01:00")},
    {"status": '21', "txn_type": 'CONSENSUSCREATE', "consensusTimestamp": pd.Timestamp("2024-01-01 00:02:00")},
]

@pytest.fixture
def hcs_services():
    with patch('consensus_services.hcs_stats.BaseScript.__init__', return_value=None):
        hcs_services_instance = HCSServices()
        hcs_services_instance.options = MagicMock()
        hcs_services_instance.options.input_file = 'input.json'
        hcs_services_instance.options.output_folder = 'output'
        hcs_services_instance.options.output_format = 'json'
        hcs_services_instance.options.log_level = 'INFO'
        hcs_services_instance.logger = MagicMock()
        return hcs_services_instance

def test_transform_data(hcs_services):
    result = hcs_services.transform_data(sample_records)
    expected = [
        {"status": '22', "txn_type": 'CONSENSUSCREATE', "consensusTimestamp": pd.Timestamp("2024-01-01 00:00:00")},
        {"status": '22', "txn_type": 'CONSENSUSSUBMITMESSAGE', "consensusTimestamp": pd.Timestamp("2024-01-01 00:01:00")}
    ]
    assert result == expected

def test_clean_records_df(hcs_services):
    df = pd.DataFrame([
        {"consensusTimestamp": pd.Timestamp("2024-01-01 00:00:00"), "txn_type": 'CONSENSUSCREATE'},
        {"consensusTimestamp": pd.Timestamp("2024-01-01 00:01:45"), "txn_type": 'CONSENSUSSUBMITMESSAGE'}
    ])
    result = hcs_services.clean_records_df(df)
    expected = df.copy()
    expected["rounded_timestamp"] = [pd.Timestamp("2024-01-01 00:00:00"), pd.Timestamp("2024-01-01 00:01:00")]
    pd.testing.assert_frame_equal(result, expected)

def test_aggregate_recordstreams_by_type(hcs_services):
    df = pd.DataFrame([
        {"consensusTimestamp": pd.Timestamp("2024-01-01 00:00:00"), "rounded_timestamp": pd.Timestamp("2024-01-01 00:00:00"), "txn_type": 'CONSENSUSCREATE', "transaction_hash": "hash1", "consensus_submit_message_bytes": 100, "consensus_create_topicID": 1, "consensus_submit_topicID": 1, "consensus_update_topicID": 1, "consensus_delete_topicID": 1},
        {"consensusTimestamp": pd.Timestamp("2024-01-01 00:01:00"), "rounded_timestamp": pd.Timestamp("2024-01-01 00:01:00"), "txn_type": 'CONSENSUSSUBMITMESSAGE', "transaction_hash": "hash2", "consensus_submit_message_bytes": 200, "consensus_create_topicID": 2, "consensus_submit_topicID": 2, "consensus_update_topicID": 2, "consensus_delete_topicID": 2}
    ])
    result = hcs_services.aggregate_recordstreams_by_type(df)
    expected = pd.DataFrame([
        {"rounded_timestamp": pd.Timestamp("2024-01-01 00:00:00"), "txn_type": 'CONSENSUSCREATE', "transaction_count": 1, "consensus_bytes": 100, "consensus_create_topicID": 1, "consensus_submit_topicID": 1, "consensus_update_topicID": 1, "consensus_delete_topicID": 1, "tps": 1/60},
        {"rounded_timestamp": pd.Timestamp("2024-01-01 00:01:00"), "txn_type": 'CONSENSUSSUBMITMESSAGE', "transaction_count": 1, "consensus_bytes": 200, "consensus_create_topicID": 1, "consensus_submit_topicID": 1, "consensus_update_topicID": 1, "consensus_delete_topicID": 1, "tps": 1/60}
    ])
    pd.testing.assert_frame_equal(result, expected)

def test_aggregate_recordstreams_submitted_topics(hcs_services):
    df = pd.DataFrame([
        {"consensusTimestamp": pd.Timestamp("2024-01-01 00:00:00"), "rounded_timestamp": pd.Timestamp("2024-01-01 00:00:00"), "txn_type": 'CONSENSUSCREATE', "transaction_hash": "hash1", "consensus_submit_message_bytes": 100, "consensus_submit_topicID": 1},
        {"consensusTimestamp": pd.Timestamp("2024-01-01 00:01:00"), "rounded_timestamp": pd.Timestamp("2024-01-01 00:01:00"), "txn_type": 'CONSENSUSSUBMITMESSAGE', "transaction_hash": "hash2", "consensus_submit_message_bytes": 200, "consensus_submit_topicID": 2}
    ])
    result = hcs_services.aggregate_recordstreams_submitted_topics(df)
    expected = pd.DataFrame([
        {"rounded_timestamp": pd.Timestamp("2024-01-01 00:00:00"), "consensus_submit_topicID": 1, "transaction_count": 1, "consensus_bytes": 100, "tps": 1/60},
        {"rounded_timestamp": pd.Timestamp("2024-01-01 00:01:00"), "consensus_submit_topicID": 2, "transaction_count": 1, "consensus_bytes": 200, "tps": 1/60}
    ])
    pd.testing.assert_frame_equal(result, expected)
