# Transaction Analysis Tool

This repository contains a set of tools for analyzing transaction data. The tools include models for representing transactions, scripts for processing transaction data, and utility functions for common operations.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
  - [Model](#model)
  - [Transaction Volume by Node](#transaction-volume-by-node)
- [Example](#example)
- [Output](#output)
- [Contributing](#contributing)
- [License](#license)

## Installation

To use the tools in this repository, you need to have Python installed on your system. Additionally, you need to install the required packages. You can install them using poetry:

```bash
poetry install
```

## Usage

### Model

The `Txn` model is defined in `model.py` and represents a transaction with various fields.

```python
from model import Txn
import datetime

# Example data
data = {
    "status": "completed",
    "record.transactionHash": "0x12345abcde",
    "@processed": "2023-06-18T12:34:56",
    "body.nodeAccountID.accountNum": "789",
    "txn_type": "transfer",
    "consensusTimestamp": "2023-06-18T12:35:00"
}

# Creating an instance of Txn
transaction = Txn(**data)

# Accessing fields
print(transaction.status)
print(transaction.transaction_hash)
print(transaction.txn_type)
print(transaction.processed_timestamp)
print(transaction.consensusTimestamp)
print(transaction.node_id)
```

### Transaction Volume by Node

The `transaction_volume_by_node.py` script processes transaction records to calculate the transaction volume by node. It uses the `Txn` model and various utility functions defined in `common.py`.

To run this script, you need to have your data in the appropriate format and provide the necessary environment variables.


#### Running the Script

```bash
python transaction_volume_by_node.py --input_file path_to_input_file --output_folder path_to_output_folder
```

### Example

Here's an example of how to use the tools provided in this repository.

```python
# Example data
data = {
    "status": "completed",
    "record.transactionHash": "0x12345abcde",
    "@processed": "2023-06-18T12:34:56",
    "body.nodeAccountID.accountNum": "789",
    "txn_type": "transfer",
    "consensusTimestamp": "2023-06-18T12:35:00"
}

# Creating an instance of Txn
transaction = Txn(**data)

# Outputting the transaction details
print("Transaction Details:")
print(f"Status: {transaction.status}")
print(f"Transaction Hash: {transaction.transaction_hash}")
print(f"Transaction Type: {transaction.txn_type}")
print(f"Processed Timestamp: {transaction.processed_timestamp}")
print(f"Consensus Timestamp: {transaction.consensusTimestamp}")
print(f"Node ID: {transaction.node_id}")

# Running the transaction volume script
import os
from transaction_volume_by_node import NetworkOverview

# Set up environment variables (this is only setup for example, normally it should be set in .env file)
os.environ['HEDERA_METRIC_CONFIG_PATH'] = 'config/path'
os.environ['HEDERA_DEV_ENV'] = 'True'
os.environ['LOG_DIR'] = 'log/directory'
os.environ['PARSER_OUTPUT_DIR'] = 'output/directory'
os.environ['LOG_LEVEL'] = 'INFO'
os.environ['HEDERA_NETWORK'] = 'testnet'

# Initialize and run the script
network_overview = NetworkOverview()
network_overview.run()
```

## Output

The output of running the `transaction_volume_by_node.py` script will be a file containing the aggregated transaction volumes by node and timestamp. The file will be saved in the specified output directory.

The output will have the following format:

```
rounded_timestamp,node_id,transaction_hash
2023-06-18 12:34:00,789,10
2023-06-18 12:35:00,789,15
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

---

If you have any additional information or specific requirements, please let me know so I can refine the README further.