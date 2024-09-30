
# Smart Contract Services Script

The `SmartContract` script processes transaction data from the Hedera network related to smart contracts and Ethereum transactions. It transforms raw records, cleans and aggregates them, and generates reports that summarize contract and gas usage across different metrics.

## Key Features

- **Data Transformation**:
  - Simplifies raw records, extracting relevant fields such as transaction type, contract number, gas usage, and accounts involved.
  - Supports both smart contract and Ethereum-based transactions.

- **Data Cleaning**:
  - Removes duplicate records based on transaction hash and contract number.
  - Adds a rounded timestamp column to group transactions by minute.

- **Data Aggregation**:
  - Aggregates records by contract number, transaction type, and account, computing metrics such as transaction count, total gas used, and max/min gas used.
  - Provides various aggregation levels, including by contract, by account, and by transaction type.

- **Output**:
  - Saves transformed and aggregated data as JSON files in the specified output folder.

## Usage

1. Prepare an input file containing smart contract transaction data.
2. Run the script using the following command:
   ```bash
   python smart_contract_services.py -i path_to_input_file -o path_to_output_folder
   ```

### Command-Line Arguments

- `-i`: Path to the input file containing the transaction data.
- `-o`: Path to the output folder where results will be saved.

## Example Output

The script generates several output files with aggregated metrics, including:

1. **Synthetic Data**:
   ```json
   [
     {
       "txn_type": "CONTRACTCALL",
       "transaction_hash": "0x123...",
       "consensusTimestamp": "2023-09-25T12:00:00",
       "contract_number": "1001",
       "gasUsed": 50000,
       "payer": [1005],
       "other_associated_account": [1006]
     }
   ]
   ```

2. **Aggregated by Type**:
   ```json
   [
     {
       "contract_number": "1001",
       "txn_type": "CONTRACTCALL",
       "rounded_timestamp": "2023-09-25T12:00:00",
       "transaction_count": 5,
       "gas_used_total": 200000,
       "gas_used_max": 50000,
       "gas_used_min": 20000
     }
   ]
   ```

3. **Aggregated by Contract**:
   ```json
   [
     {
       "contract_number": "1001",
       "transaction_count": 15,
       "gas_used_total": 700000,
       "gas_used_max": 50000,
       "gas_used_min": 10000
     }
   ]
   ```

4. **Aggregated by Account and Contract**:
   ```json
   [
     {
       "contract_number": "1001",
       "payer": "1005",
       "transaction_count": 7,
       "gas_used_total": 350000
     }
   ]
   ```

5. **Aggregated by Account**:
   ```json
   [
     {
       "payer": "1005",
       "txn_type": "CONTRACTCALL",
       "transaction_count": 10,
       "gas_used_total": 500000
     }
   ]
   ```

### Output Structure

- **Aggregated by Type**:
  - `contract_number`: The contract number.
  - `txn_type`: The transaction type (e.g., `CONTRACTCALL`, `ETHEREUMTRANSACTION`).
  - `rounded_timestamp`: The timestamp rounded to the nearest minute.
  - `transaction_count`: Number of transactions in that minute for that contract and type.
  - `gas_used_total`: Total gas used.
  - `gas_used_max`: Maximum gas used in a single transaction.
  - `gas_used_min`: Minimum gas used in a single transaction.

- **Aggregated by Contract**:
  - `contract_number`: The contract number.
  - `transaction_count`: Total number of transactions for the contract.
  - `gas_used_total`: Total gas used for the contract.
  - `gas_used_max`: Maximum gas used for the contract.
  - `gas_used_min`: Minimum gas used for the contract.

- **Aggregated by Account and Contract**:
  - `contract_number`: The contract number.
  - `payer`: The account number of the payer.
  - `transaction_count`: Number of transactions associated with the account for that contract.
  - `gas_used_total`: Total gas used by the account for the contract.

- **Aggregated by Account**:
  - `payer`: The account number.
  - `txn_type`: The transaction type.
  - `transaction_count`: Total number of transactions initiated by the account.
  - `gas_used_total`: Total gas used by the account.

## Notes

- Ensure the input data is correctly formatted and contains all required fields, such as `txn_type`, `consensusTimestamp`, `contractNum`, `gasUsed`, `transaction_hash`, and `payer`.
- The script outputs multiple JSON files, each reflecting a different level of data aggregation.
