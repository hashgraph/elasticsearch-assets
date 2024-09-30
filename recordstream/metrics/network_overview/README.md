# Transaction Analysis Tool

This repository contains a set of tools for analyzing transaction data. The tools include models for representing transactions, scripts for processing transaction data, and utility functions for common operations.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
  - [Model](#model)
  - [Transaction Volume by Node](#transaction-volume-by-node)
  - [Transaction Volume by Services](#transaction-volume-by-services)
  - [Developer Activites](#developer-activities)
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

#### Network Overview Metrics Script

The `NetworkOverview` script processes Hedera network transaction data, focusing on node-specific metrics. It performs data cleaning, filters records based on status, and aggregates transaction counts by node per minute.

#### Key Features

- **Data Cleaning**:
  - Removes duplicate records.
  - Adds a rounded timestamp column for aggregation (by minute).
  - Classifies transactions into high-level types based on `txn_type`.

- **Aggregation**:
  - Filters out records with status `!= 22`.
  - Aggregates transaction counts per node for each minute.
  
- **Output**:
  - Provides transaction counts grouped by node and minute.

#### Usage

1. Prepare an input file containing network transaction data.
2. Run the script using the command:
   ```bash
   python network_overview.py -i path_to_input_file -o path_to_output_folder
   ```

#### Command-Line Arguments

- `-i`: Path to the input file with network transaction data.
- `-o`: Path to the output folder where results will be saved.

#### Example Output

The script generates an output file that contains aggregated transaction data by node and minute:

```json
[
  {
    "rounded_timestamp": "2023-09-25T12:00:00",
    "node_id": "1",
    "transaction_count": 150
  },
  {
    "rounded_timestamp": "2023-09-25T12:01:00",
    "node_id": "2",
    "transaction_count": 200
  }
]
```

##### Output Structure

- `rounded_timestamp`: The timestamp rounded to the nearest minute.
- `node_id`: The ID of the network node.
- `transaction_count`: The number of transactions recorded for that node in that minute.

#### Additional Notes

- Ensure the input data is correctly formatted and contains all required fields (e.g., `txn_type`, `consensusTimestamp`, `status`, `transaction_hash`, `node_id`).
- The script outputs a JSON file to the specified output folder with aggregated transaction data by node and timestamp.

### Transaction Volume by Services

This script processes Hedera network transaction data to provide insights into the volume and distribution of various types of network services. It calculates detailed transaction counts and aggregates them into high-level categories, offering an overview of network activity across services such as Crypto, Consensus, Token, Smart Contracts, and more.

#### Key Features

- **Data Cleaning**:
  - Removes duplicate records.
  - Adds a timestamp rounded to the nearest minute.
  - Classifies transactions into high-level categories.
  
- **Aggregation**:
  - Aggregates transaction counts by type (e.g., Crypto, Token, Consensus).
  - Calculates total transaction volumes for various services and the network overall.
  - Computes transactions per second (TPS) for detailed and overall metrics.
  
- **Output**:
  - Provides detailed metrics per minute by transaction type.
  - Summarizes overall network transaction volumes by service.
#### Usage

1. Prepare an input file with the network transaction data.
2. Run the script using:
   ```bash
   python network_overview.py -i path_to_input_file -o path_to_output_folder
   ```

#### Command-Line Arguments

- `-i`: Path to the input file containing network transaction data.
- `-o`: Path to the folder where output files will be stored.

#### Example Output

##### Detailed Transaction Metrics by Type
```json
[
  {
    "rounded_timestamp": "2023-09-25T12:00:00",
    "transaction_type": "CONSENSUSSUBMITMESSAGE",
    "transaction_count": 150,
    "data_type": "detail"
  }
]
```

##### Aggregated Network Overview by Service
```json
[
  {
    "rounded_timestamp": "2023-09-25T12:00:00",
    "transaction_type": "crypto_total",
    "transaction_count": 500,
    "transaction_per_second": 8.33,
    "data_type": "overall"
  },
  {
    "rounded_timestamp": "2023-09-25T12:00:00",
    "transaction_type": "hcs_total",
    "transaction_count": 300,
    "transaction_per_second": 5,
    "data_type": "overall"
  }
]
```

#### Overall Metrics
The script outputs two main types of aggregated metrics:
- **Detailed**: Transactions aggregated by specific transaction type per minute.
- **Overall**: Network-level transactions aggregated into service categories like Crypto, Token, Consensus, and more.

#### Additional Notes

- Ensure the input file is properly formatted and contains all the necessary fields for network transactions.
- The output will be written to multiple files in the specified output folder:
  - Detailed transaction counts per type.
  - Overall transaction counts for different services.


### Developer Activities

The `DeveloperActivities` script processes Hedera network transaction data, focusing on developer-specific activities such as contract creation, token creation, and topic updates. The script filters, cleans, aggregates, and outputs developer-related metrics grouped by service and network.

#### Key Features

- **Record Filtering**:
  - Filters records where the transaction type involves developer activities (e.g., contract and token creation).
  - Only processes records with a status of `22` (successful transactions).

- **Data Cleaning**:
  - Removes duplicate records.
  - Adds a rounded timestamp column based on the `consensusTimestamp` (floored to the nearest minute).
  - Maps transaction types to higher-level services (e.g., `HTS`, `HSCS`).

- **Aggregation**:
  - Aggregates records by service and network to provide transaction counts and unique developer counts.
  - Generates separate outputs for service-level and network-level aggregations.

- **Output**:
  - Saves aggregated metrics as JSON files in the specified output folder.

#### Usage

1. Prepare an input file containing network transaction data.
2. Run the script using the command:
   ```bash
   python developer_activities.py -i path_to_input_file -o path_to_output_folder
   ```

##### Command-Line Arguments

- `-i`: Path to the input file with network transaction data.
- `-o`: Path to the output folder where results will be saved.

#### Example Output

The script generates two output files:
1. **Aggregated by Service**:
   ```json
   [
     {
       "rounded_timestamp": "2023-09-25T12:00:00",
       "service": "HTS",
       "transaction_count": 150,
       "dev_count": 50
     },
     {
       "rounded_timestamp": "2023-09-25T12:01:00",
       "service": "HSCS",
       "transaction_count": 200,
       "dev_count": 60
     }
   ]
   ```

2. **Aggregated by Network**:
   ```json
   [
     {
       "rounded_timestamp": "2023-09-25T12:00:00",
       "transaction_count": 350,
       "dev_count": 100
     },
     {
       "rounded_timestamp": "2023-09-25T12:01:00",
       "transaction_count": 400,
       "dev_count": 120
     }
   ]
   ```

#### Output Structure

- **Aggregated by Service**:
  - `rounded_timestamp`: The timestamp rounded to the nearest minute.
  - `service`: The high-level service associated with the transaction (e.g., `HTS`, `HSCS`).
  - `transaction_count`: The total number of transactions for that service in that minute.
  - `dev_count`: The number of unique developers who initiated the transactions.

- **Aggregated by Network**:
  - `rounded_timestamp`: The timestamp rounded to the nearest minute.
  - `transaction_count`: The total number of transactions across all services for that minute.
  - `dev_count`: The number of unique developers across all transactions for that minute.

#### Developer Activity Types

The script focuses on the following developer activities:

- **HTS (Hedera Token Service)**:
  - `TOKENCREATION`
  - `NFTCREATION`

- **HSCS (Hedera Smart Contract Service)**:
  - `CONTRACTCREATEINSTANCE`
  - `CONTRACTUPDATEINSTANCE`

- **HCS (Hedera Consensus Service)**:
  - `CONSENSUSCREATETOPIC`
  - `CONSENSUSUPDATETOPIC`

## Additional Notes

- Ensure the input data is correctly formatted and contains all required fields (e.g., `txn_type`, `consensusTimestamp`, `status`, `transaction_hash`, `payer`).
- The script outputs two separate JSON files for service-level and network-level aggregations.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

---

If you have any additional information or specific requirements, please let me know so I can refine the README further.