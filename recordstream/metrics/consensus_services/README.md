# Hedera Consensus Service (HCS) Metrics Script

This script processes Hedera Consensus Service (HCS) transaction data, transforming and aggregating it to provide insights on the network's consensus activities. It computes transaction metrics by transaction type and topic, as well as the number of transactions per second (TPS).

## Key Features
- **Transformation**: Extracts relevant data from HCS transactions, focusing on consensus-related messages and topics.
- **Aggregation**:
  - Aggregates transaction data by type and consensus topic ID.
  - Calculates TPS and aggregates transaction counts and consensus message sizes.
- **Metrics**:
  - Aggregates the number of distinct topic IDs for different consensus operations (create, submit, update, delete).
  - Counts the number of transactions per minute and calculates TPS.
- **Output**: Generates JSON files with aggregated results by transaction type and submitted topics.

## Usage

1. Set up the input file with the necessary Hedera Consensus Service (HCS) transaction data.
2. Run the script using:
   ```bash
   python consensus_services.py -i path_to_input_file -o path_to_output_folder
   ```

## Command-Line Arguments

- `-i`: Path to the input file containing HCS transaction data.
- `-o`: Path to the folder where output files will be stored.

## Example Output

### Aggregated HCS Metrics by Transaction Type
```json
[
  {
    "rounded_timestamp": "2023-09-25T12:00:00",
    "txn_type": "CONSENSUSSUBMITMESSAGE",
    "transaction_count": 150,
    "consensus_bytes": 50000,
    "consensus_create_topicID": 5,
    "consensus_submit_topicID": 10,
    "consensus_update_topicID": 2,
    "consensus_delete_topicID": 1,
    "tps": 2.5
  }
]
```

### Aggregated HCS Metrics by Submitted Topics
```json
[
  {
    "rounded_timestamp": "2023-09-25T12:00:00",
    "consensus_submit_topicID": 12345,
    "transaction_count": 50,
    "consensus_bytes": 20000,
    "tps": 0.83
  }
]
```

## Additional Notes
- Ensure that the input file is in the correct format and contains all required fields for HCS transaction data.
- The script will generate multiple output files in the specified output folder:
  - Aggregated HCS metrics by transaction type.
  - Aggregated HCS metrics by submitted topics.
- The output files will be in JSON format and will contain the aggregated metrics for the specified time intervals.