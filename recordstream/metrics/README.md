# Metrics

This folder contains the metrics module for the project. The metrics module is responsible for collecting, processing, and analyzing various metrics related to the application.

## Table of Contents

- [Installation](#installation)
- [Available Metrics](#available-metrics)
- [Contributing](#contributing)
- [License](#license)

## Installation


To run the Hedera repository locally, follow these steps:

1. **Clone the Hedera Repository**
   ```bash
   git clone https://github.com/hashgraph/elasticsearch-assets.git
   cd elasticsearch-assets/recordstream
   ```

2. **Ensure Python 3.9.x is Installed**
   ```bash
   python --version
   ```

3. **Ensure Poetry 1.2.x is Installed**
   ```bash
   poetry -v
   ```

4. **Install Packages with Poetry**
   ```bash
   cd metrics
   poetry install
   ```


5. **Run the Metrics Module**

    To run the metrics module using Poetry, execute the following command. 
    ```bash
    poetry run python path_to_metrics_module.py -i path_to_input_file -o path_to_output_file -l log_level -f output_format
    ```
    
    This command runs a Python script called `path_to_metrics_module.py` with several command-line arguments:

    - `-h, --help`: Helper.
    - `-i INPUT_FILE, --input_file=INPUT_FILE`: Specifies the path to the input file.
    - `-o OUTPUT_FOLDER, --output_folder=OUTPUT_FOLDER`: Specifies the path to the output file.
    - `-f OUTPUT_FORMAT, --output_format=OUTPUT_FORMAT`: Specifies the output format for the script (e.g., JSON, CSV).
    - `-l LOG_LEVEL, --level=LOG_LEVEL`: Specifies the log level for the script (e.g., DEBUG, INFO, WARNING, ERROR, CRITICAL).

    ##### Example usage:
    
    ```bash
    poetry run python network_overview/transaction_volume_by_node.py -i $HOME/recordstream.json -o $HOME/metrics_overview -l INFO -f csv
    ```

    This command runs the `transaction_volume_by_node.py` script with the following arguments:
    - `-i $HOME/recordstream.json`: Get the decoded records file from $HOME/recodstreams.json.
    - `-o $HOME/metrics_overview`: Save the output files to $HOME/metrics_overview.
    - `-l INFO`: Set the log level to INFO.
    - `-f csv`: Set the output format to CSV.


## Available Metrics

For detailed explanations of each metric, please refer to the respective files in the `metrics` folder.

| Folder               | File                              | Description                                                               |
|----------------------|-----------------------------------|---------------------------------------------------------------------------|
| `network_overview`   | `transaction_volume_by_node.py`   | Overall network activities split by node.                                 |
| `network_overview`   | `transaction_volume_by_services.py` | Overall network activities split by services.                             |
| `account_overview`   | `active_account.py`               | Overall account activities, including new accounts created and active accounts. |
| `consensus_services` | `hcs_stats.py`                    | Aggregated HCS activities by transaction type and submitted topics.       |
| `token_services`     | `fungible_token_stats.py`         | Synthetic and aggregated fungible token metrics by transaction type, token number, and account. |
| `token_services`     | `non_fungible_token_stats.py`     | Synthetic and aggregated non-fungible token metrics by transaction type, token number, and account. |
| `smart_contract_services` | `sc_stats.py`                | Synthetic and aggregated smart contract metrics by transaction type, smart contract number, and account. |

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
