# Active Account Metrics Script

This script calculates and aggregates active account metrics from Hedera network data. It processes transaction records to extract unique accounts, account activity, and transaction details per key type.

## Key Features
- **Transformation**: Converts and processes records to extract account numbers and transaction details.
- **Aggregation**: Aggregates data on active accounts by rounding timestamps and grouping by transaction types.
- **Metrics**:
  - Counts distinct active accounts per minute.
  - Aggregates accounts and transactions by key type.
- **Output**: Generates JSON files with aggregated results and a list of unique accounts.

## Usage

1. Set up the input file with the necessary Hedera transaction data.
2. Run the script using:
   ```bash
   python active_account.py -i path_to_input_file -o path_to_output_folder
   ```

## Command-Line Arguments

- `-i`: Path to the input file containing Hedera transaction data.
- `-o`: Path to the folder where output files will be stored.

## Example Output

### Aggregated Active Accounts
```json
[
  {
    "rounded_timestamp": "2023-09-25T12:00:00",
    "accountNum": 100
  },
  {
    "rounded_timestamp": "2023-09-25T12:01:00",
    "accountNum": 95
  }
]
```

### EC Key Type Aggregated Transactions
```json
[
  {
    "key_type": "ED25519",
    "transaction_count": 50,
    "account_count": 30
  },
  {
    "key_type": "ECDSA",
    "transaction_count": 40,
    "account_count": 25
  }
]
```

### Unique Active Accounts
```json
[
  12345,
  67890,
  54321
]
```

## Additional Notes
- Ensure that the input file is in the correct format and contains all required fields.
- The script will generate multiple output files in the specified output folder:
  - Aggregated account metrics per minute.
  - Aggregated metrics based on EC key types.
  - A list of unique active accounts.
