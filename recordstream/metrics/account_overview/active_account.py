import json
import os
import sys

import pandas as pd
# Add the path to the utils module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from metrics.utils.common import BaseScript
from account_overview.model import Txn


class Account(BaseScript):
    """
    This class represents the active account metrics script.
    It inherits from the BaseScript class and provides methods to transform and aggregate data related to active accounts.
    """

    def __init__(self):
        super().__init__(log_filename="active_account")
        # Your HTS-specific initialization code here
        self.script_name = os.path.basename(__file__[:-3])
    
    def transform_data(self, records):
        """
        Transform the input records by extracting the timestamp and unnested accountNum from the transfer_list column.

        Args:
            records (list): List of input records.

        Returns:
            list: List of transformed records.
        """
        simplified_records = []
        for record in records:
            if record['transfer_list'] is None:
                simplified_records.append({
                    'consensusTimestamp': record['consensusTimestamp'],
                    'accountNum': record["payer"]
                })
            else:
                for transfer in record['transfer_list']:
                    simplified_records.append({
                        'consensusTimestamp': record['consensusTimestamp'],
                        'accountNum': transfer['accountID']['accountNum']
                    })
        return simplified_records

    def transform_data_payer_ec_key(self, records):
        """
        Transform the input records by extracting the timestamp, unnested accountNum, and key_type from the transfer_list column.

        Args:
            records (list): List of input records.

        Returns:
            list: List of transformed records.
        """
        simplified_records = []
        for record in records:
            if record['transfer_list'] is None:
                simplified_records.append({
                    'transaction_hash': record['transaction_hash'],
                    'consensusTimestamp': record['consensusTimestamp'],
                    'accountNum': record["payer"],
                    'key_type': record["txn_sign_keys"]
                })
            else:
                for transfer in record['transfer_list']:
                    simplified_records.append({
                        'transaction_hash': record['transaction_hash'],
                        'consensusTimestamp': record['consensusTimestamp'],
                        'key_type': record["txn_sign_keys"],
                        'accountNum': transfer['accountID']['accountNum']
                    })
        return simplified_records

    def clean_records_df(self, records_df):
        """
        Clean the records DataFrame by adding a rounded timestamp to a minute and a high-level transaction type based on txn_type.

        Args:
            records_df (DataFrame): Input records DataFrame.

        Returns:
            DataFrame: Cleaned records DataFrame.
        """
        # add rounded timestamp to a minute
        records_df['rounded_timestamp'] = records_df['consensusTimestamp'].dt.floor('min')
        # add high level transaction type based on txn_type
        return records_df

    def aggregate_recordstreams(self, records_df):
        """
        Aggregate the record streams DataFrame by counting the distinct accountNums per minute.

        Args:
            records_df (DataFrame): Input records DataFrame.

        Returns:
            DataFrame: Aggregated records DataFrame.
        """
        # Aggregate record streams DataFrame
        # Count distinct accountNums per minute
        active_account = records_df.groupby(['rounded_timestamp'])['accountNum'].nunique().reset_index()
        return active_account
    
    def unique_account(self, records_df):
        """
        Extract the unique accountNums from the records DataFrame.

        Args:
            records_df (DataFrame): Input records DataFrame.

        Returns:
            ndarray: Array of unique accountNums.
        """
        # extract unique accountNums
        unique_account = records_df['accountNum'].unique()
        return unique_account
    
    def aggregated_recordstreams_payer_ec_key(self, records_df):
        """
        Aggregate the record streams DataFrame by counting the distinct accountNums and transaction hashes per key_type.

        Args:
            records_df (DataFrame): Input records DataFrame.

        Returns:
            DataFrame: Aggregated records DataFrame.
        """
        # Aggregate record streams DataFrame
        # Count distinct accountNums per minute
        records_df = records_df.explode('key_type')
        filter_df = records_df[records_df['key_type'].notna()]
        active_account = filter_df.groupby(['key_type']).agg(
            transaction_count=pd.NamedAgg(column="transaction_hash", aggfunc="nunique"),
            account_count=pd.NamedAgg(column="accountNum", aggfunc="nunique")
        ).reset_index()
        return active_account

    def run(self):
        """
        Run the active account metrics script.
        """
        self.logger.info("Run method started ...")
        try:
            self.logger.info(f"Reading data from {self.options.input_file} ...")
            records = self.read_data(self.options.input_file, Txn)
            simplified_records = self.transform_data(records)
            records_df = self.rcdstreams_to_pd_df(simplified_records)
            cleaned_records = self.clean_records_df(records_df)
            # Count unique number of account per minute
            aggregated_records = self.aggregate_recordstreams(cleaned_records)
            output_filename = f"{self.options.output_folder}/{self.script_name}_active_account"
            self.logger.info(f"Writing aggregated output to {output_filename} ...")
            self.write_df_to_file(output_filename, aggregated_records)
            # Aggegate EC account
            simplified_records_payer_ec_key = self.transform_data_payer_ec_key(records)
            records_df_payer_ec_key = self.rcdstreams_to_pd_df(simplified_records_payer_ec_key)
            cleaned_records_payer_ec_key = self.clean_records_df(records_df_payer_ec_key)
            aggregated_records_payer_ec_key = self.aggregated_recordstreams_payer_ec_key(cleaned_records_payer_ec_key)
            output_filename = f"{self.options.output_folder}/{self.script_name}_ec_account"
            self.logger.info(f"Writing aggregated output to {output_filename} ...")
            self.write_df_to_file(output_filename, aggregated_records_payer_ec_key)
            # Get list of unique accountNums in the records
            unique_account = self.unique_account(cleaned_records)
            output_filename = f"{self.options.output_folder}/unique_active_accounts.json"
            self.logger.info(f"Writing unique accountNums to {output_filename} ...")
            with open(output_filename, 'w') as f:
                json.dump(unique_account.tolist(), f)
        except Exception as e:
            self.logger.exception("Fatal Error!")
            self.logger.info(e)
            exit(1)

if __name__ == "__main__":
    myObject = Account()
    myObject.run()
