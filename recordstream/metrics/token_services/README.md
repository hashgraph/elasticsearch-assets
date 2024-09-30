## Table of Contents

- [Usage](#usage)
  - [Fungible Token](#fungible-token)
  - [Non Fungible Token](#non-fungible-token)
- [Example](#example)
- [Output](#output)
- [Contributing](#contributing)
- [License](#license)

## Usage

### Fungible Token

#### Overview

The `fungible_token_stats` script processes transaction records from the Hedera Token Service (HTS), specifically for fungible tokens. It reads raw data, filters and transforms it, and performs various aggregations to extract meaningful statistics such as transaction counts, send/receive amounts, and distinct users per token.

#### Key Features

- Filters and transforms raw HTS transaction records.
- Cleans and removes duplicates from the data.
- Aggregates data by transaction type and token.
- Outputs the processed data in JSON format.

#### Usage

1. Prepare an input file containing network transaction data.
2. Run the script using the command:
   ```bash
   python fungible_token_stats.py -i path_to_input_file -o path_to_output_folder
   ```

#### Command-Line Arguments

- `-i`: Path to the input file with network transaction data.
- `-o`: Path to the output folder where results will be saved.

#### Output

- **Input**: 
  - A raw data file containing HTS transaction records (specified via the script's options).
  
- **Output**: 
  - JSON files containing synthetic data and aggregated results by transaction type and by token.

#### Example Output
##### Synthetic Data 
```json
[
  {
    "txn_type": "TOKEN_TRANSFER",
    "transaction_hash": "abcd1234",
    "consensusTimestamp": "2023-09-30T12:00:00Z",
    "token_number": 12345,
    "internal_token_number": 12345,
    "payer": [123],
    "sender": [456],
    "receiver": [789],
    "send_amount": -1000,
    "receive_amount": 1000
  }
]
```

##### Aggregated Data by Transaction Type
```json
[
  {
    "rounded_timestamp": "2023-09-30T12:00:00Z",
    "txn_type": "TOKEN_TRANSFER",
    "transaction_count": 2,
    "send_amount": -1500,
    "receive_amount": 1500,
    "tps": 0.033
  }
]
```

##### Aggregated Data by Token
```json
[
  {
    "rounded_timestamp": "2023-09-30T12:00:00Z",
    "internal_token_number": 12345,
    "transaction_count": 1,
    "send_amount": -1000,
    "receive_amount": 1000,
    "distinct_payers": 1,
    "distinct_senders": 1,
    "distinct_receivers": 1
  }
]
```

These outputs are examples of how the HTS script processes and aggregates transaction data. They show key information like transaction type, amounts sent/received, distinct users, and transaction counts over time.
The script produces two output files in JSON format:
1. `synthetic_data.json` - Simplified HTS transaction data.
2. `fungible_token_stats_by_type.json` - Aggregated data by transaction type.
3. `fungible_token_stats_by_token.json` - Aggregated data by token.


### Non Fungible Token

The `non_fungible_token_stats` script processes transaction records from the Hedera Token Service (HTS), specifically for non-fungible tokens. It reads raw data, filters and transforms it, and performs various aggregations to extract meaningful statistics such as transaction counts, send/receive amounts, and distinct users per token.

#### Key Features

- Transforms and filters NFT records.
- Cleans and aggregates data by transaction type, token, and account.
- Outputs synthetic data and aggregated statistics to JSON files.

#### Usage

Run the script using the command line:

```bash
python nfts.py --input_file <path_to_input_file> --output_folder <path_to_output_folder>
```
#### Command-Line Arguments

- `-i`: Path to the input file with network transaction data.
- `-o`: Path to the output folder where results will be saved.


#### Example Output
##### Synthetic Data 
```json
[
    {
        "txn_type": "NFT_TRANSFER",
        "transaction_hash": "0x123abc456def",
        "consensusTimestamp": "2024-09-30T12:00:00Z",
        "token_number": "1234",
        "internal_token_number": "1234",
        "payer": ["1001"],
        "sender": ["1002"],
        "receiver": ["1003"],
        "series": ["1"]
    }
]
```

###### Aggregated Data by Transaction Type
```json
[
    {
        "txn_type": "NFT_TRANSFER",
        "transaction_count": 150
    },
    {
        "txn_type": "NFT_MINT",
        "transaction_count": 75
    },
    {
        "txn_type": "total",
        "transaction_count": 225
    }
]
```

##### Aggregated Data by Token
```json
[
    {
        "internal_token_number": "1234",
        "txn_type": "NFT_TRANSFER",
        "transaction_count": 100
    },
    {
        "internal_token_number": "5678",
        "txn_type": "NFT_MINT",
        "transaction_count": 50
    }
]
```
##### Aggregated Data by Account
```json
[
    {
        "accountNum": "1001",
        "transaction_count": 50,
        "data_type": "payer"
    },
    {
        "accountNum": "1002",
        "transaction_count": 75,
        "data_type": "sender"
    }
]
```
## Output Files

The script generates the following output files in the defined output folder:

- `non_fungible_token_stats_synthetic_data.json`
- `non_fungible_token_stats_by_type.json`
- `non_fungible_token_stats_by_token.json`
- `non_fungible_token_stats_by_account.json`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.