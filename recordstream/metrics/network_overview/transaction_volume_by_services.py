import os
import sys
import pandas as pd


# Add the path to the utils module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from metrics.utils.common import BaseScript
from network_overview.model import Txn

class NetworkOverview(BaseScript):
    def __init__(self):
        super().__init__(log_filename="network_overview")
        # Your HTS-specific initialization code here
        self.script_name = os.path.basename(__file__[:-3])

    def clean_records_df(self, records_df):
        """
        Cleans the records DataFrame by performing the following operations:
        - Removes duplicate rows.
        - Adds a rounded timestamp column to the DataFrame by rounding the 'consensusTimestamp' column to the nearest minute.
        - Adds a high level transaction type column based on the 'txn_type' column.

        Args:
            records_df (pandas.DataFrame): The DataFrame containing the records.

        Returns:
            pandas.DataFrame: The cleaned records DataFrame.
        """
        records_df.drop_duplicates(inplace=True)
        records_df['rounded_timestamp'] = records_df['consensusTimestamp'].dt.floor('min')

        # Add high level transaction type based on txn_type

        return records_df

    def aggregate_recordstreams(self, records_df):
        """
        Aggregate the record streams DataFrame to get the total number of transactions by transaction type per minute.

        Args:
            records_df (DataFrame): The input DataFrame containing the records.

        Returns:
            DataFrame: The aggregated DataFrame with columns for rounded timestamp, transaction type, transaction count, and data type.
        """
        # Filter out status != 22
        records_df = records_df[records_df['status'] == '22']
        # Aggregate record streams DataFrame 
        # Get the total number of transactions by transaction type per minute
        group_txn = records_df.groupby(['rounded_timestamp', 'txn_type'])['transaction_hash'].count().reset_index()
        # rename the column
        group_txn.rename(columns={
            'txn_type': 'transaction_type',
            'transaction_hash': 'transaction_count'
        }, inplace=True)
        group_txn['data_type'] = 'detail'
        return group_txn

    def aggregate_recordstreams_overall(self, records_df):
        """
        Aggregates the record streams DataFrame and calculates the transaction volume by services.

        Args:
            records_df (DataFrame): The input DataFrame containing the records.

        Returns:
            DataFrame: The aggregated DataFrame with transaction volume by services.

        """
        # Aggregate record streams DataFrame
        # Filter out status != 22
        records_df = records_df[records_df['status'] == '22']
        # Get the total number of transactions by transaction type per minute
        group_txn = records_df.groupby('rounded_timestamp').apply(
            lambda x: pd.Series({
                'crypto_total': x[(x['txn_type'].str.contains('CRYPTO')) & (x['txn_type'] != 'CRYPTOCREATEACCOUNT')]['transaction_hash'].count(),
                'create_account_total': x[x['txn_type'] == 'CRYPTOCREATEACCOUNT']['transaction_hash'].count(),
                'hcs_total': x[x['txn_type'].str.contains('CONSENSUS')]['transaction_hash'].count(),
                'hts_fungible_total': x[x['txn_type'].str.contains('TOKEN')]['transaction_hash'].count(),
                'hts_nft_total': x[x['txn_type'].str.contains('NFT')]['transaction_hash'].count(),
                'smart_contract_total': x[x['txn_type'].str.contains('CONTRACT')]['transaction_hash'].count(),
                'file_total': x[x['txn_type'].str.contains('FILE')]['transaction_hash'].count(),
                'ethereum_total': x[x['txn_type'].str.contains('ETHEREUM')]['transaction_hash'].count(),
                'staking_total': x[x['txn_type'].str.contains('NODESTAKE')]['transaction_hash'].count(),
                'total': x['transaction_hash'].count()
            })).reset_index()
        # Transform the group_txn DataFrame to a long format
        network_overview = group_txn.melt(id_vars=['rounded_timestamp'], var_name='transaction_type', value_name='transaction_count')
        # transaction per second 
        network_overview['transaction_per_second'] = network_overview['transaction_count'] / 60
        network_overview['data_type'] = 'overall'
        return network_overview

    def run(self):
        """
        Executes the main logic of the Network Overall script.
        
        Reads data from the input file, performs data cleaning and aggregation,
        and writes the aggregated output to a file.
        
        Raises:
            Exception: If any fatal error occurs during the execution.
        """
        self.logger.info("Run method started ...")
        try:
            self.logger.info(f"Reading data from {self.options.input_file}...")
            records = self.read_data(self.options.input_file, Txn)
            records_df = self.rcdstreams_to_pd_df(records)
            cleaned_records = self.clean_records_df(records_df)
            aggregated_records_txn = self.aggregate_recordstreams(cleaned_records)
            aggregated_records_overall = self.aggregate_recordstreams_overall(cleaned_records)
            # merge the two dataframes
            aggregated_records = pd.concat([aggregated_records_txn, aggregated_records_overall])
            output_filename = f"{self.options.output_folder}/{self.script_name}"
            self.logger.info(f"Writing aggregated output to {output_filename} ...")
            self.write_df_to_file(output_filename, aggregated_records)
        except Exception as e:
            self.logger.exception("Fatal Error!")
            self.logger.info(e)
            exit(1)

if __name__ == "__main__":
    myObject = NetworkOverview()
    myObject.run()
