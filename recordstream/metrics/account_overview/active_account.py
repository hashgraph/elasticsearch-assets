import json
import os
import sys

import pandas as pd
# Add the path to the utils module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from metrics.utils.common import BaseScript
from model import Txn


class NetworkOverview(BaseScript):
    def __init__(self):
        super().__init__(log_filename="active_account")
        # Your HTS-specific initialization code here
        self.script_name = os.path.basename(__file__[:-3])
    
    def transform_data(self, records):
        # Extract only timestamp and unnested accountNum from the transfer_list column
        simplified_records = []
        for record in records:
            if record['transfer_list'] is None:
                simplified_records.append({
                    'consensusTimestamp': record['consensusTimestamp'],
                    'accountNum': record["payer"]
                })
            for transfer in record['transfer_list']:
                simplified_records.append({
                    'consensusTimestamp': record['consensusTimestamp'],
                    'key_type': record["txn_sign_keys"]
                })
        return simplified_records

    def transform_data_payer_ec_key(self, records):
        # Extract only timestamp and unnested accountNum from the transfer_list column
        simplified_records = []
        for record in records:
            if record['transfer_list'] is None:
                simplified_records.append({
                    'consensusTimestamp': record['consensusTimestamp'],
                    'accountNum': record["payer"],
                    'key_type': record["txn_sign_keys"]
                })
            for transfer in record['transfer_list']:
                if transfer['accountID']['accountNum'] < 0:
                    simplified_records.append({
                        'consensusTimestamp': record['consensusTimestamp'],
                        'key_type': record["txn_sign_keys"],
                        'accountNum': transfer['accountID']['accountNum']
                    })
        return simplified_records

    def rcdstreams_to_pd_df(self, records):
        # Convert records to Pandas DataFrame
        records_df = pd.DataFrame(records)
        return records_df

    def clean_records_df(self, records_df):
        # Clean records DataFrame
        records_df.drop_duplicates(inplace=True)
        # add rounded timestamp to a minute
        records_df['rounded_timestamp'] = records_df['consensusTimestamp'].dt.floor('min')
        # add high level transaction type based on txn_type

        return records_df

    def aggregate_recordstreams(self, records_df):
        # Aggregate record streams DataFrame
        # Count distinct accountNums per minute
        active_account = records_df.groupby(['rounded_timestamp'])['accountNum'].nunique().reset_index()
        return active_account
    
    def unique_account(self, records_df):
        # extract unique accountNums
        unique_account = records_df['accountNum'].unique()
        return unique_account
    
    def aggregated_recordstreams_payer_ec_key(self, records_df):
        # Aggregate record streams DataFrame
        # Count distinct accountNums per minute
        active_account = records_df.groupby(['key_type']).agg(
            transaction_count=pd.NamedAgg(column="transaction_hash", aggfunc="count"),
            account_count=pd.NamedAgg(column="accountNum", aggfunc="nunique")
        ).reset_index()
        return active_account

    def run(self):
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
    myObject = NetworkOverview()
    myObject.run()
