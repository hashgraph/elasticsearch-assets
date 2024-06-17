import os
import sys

import pandas as pd

# Add the path to the utils module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from metrics.utils.common import BaseScript
from model import Txn


class HTS(BaseScript):
    def __init__(self):
        super().__init__(log_filename="fungible_token_stats")
        # Your HTS-specific initialization code here
        self.script_name = os.path.basename(__file__[:-3])
    
    def transform_data(self, records):
        # Extract only timestamp and unnested accountNum from the transfer_list column
        simplified_records = []
        for record in records:
            if record['status'] == '22' and ('TOKEN' in record['txn_type']):
                flat_records = {
                    'txn_type': record['txn_type'],
                    'transaction_hash' : record['transaction_hash'],
                    'consensusTimestamp': record['consensusTimestamp'],
                    'token_number': record['token_number'],
                    'internal_token_number': record['token_number']
                }

                if record['transfer_list'] is not None:
                    flat_records['payer'] = [transfer['accountID']['accountNum'] for transfer in record['transfer_list'] if transfer['amount'] < 0]

                if record['token_transfer_list'] is not None:
                    token_list = record['token_transfer_list']

                    # list of token sender/receiver
                    for token in token_list:
                        # filter out nft token
                        if token['nftTransfers'] is not None:
                            continue
                        # overwrite internal_token_number when token_number is present
                        flat_records['internal_token_number'] = token['token']['tokenNum']
                        # list sender/receiver
                        if token['transfers'] is None:
                            simplified_records.append(flat_records)
                            continue
                        flat_records['sender'] = [transfer['accountID']['accountNum'] for transfer in token['transfers']  if transfer['amount'] < 0]
                        flat_records['receiver'] = [transfer['accountID']['accountNum'] for transfer in token['transfers'] if transfer['amount'] >= 0]
                        # token burn/mint/transfer amount
                        flat_records['send_amount'] = sum([transfer['amount'] for transfer in token['transfers'] if transfer['amount'] < 0])
                        flat_records['receive_amount'] = sum([transfer['amount'] for transfer in token['transfers'] if transfer['amount'] >= 0])

                        simplified_records.append(flat_records)
        return simplified_records

    def rcdstreams_to_pd_df(self, records):
        # Convert records to Pandas DataFrame
        records_df = pd.DataFrame(records)
        return records_df

    def clean_records_df(self, records_df):
        # Clean records DataFrame
        records_df.drop_duplicates(inplace=True, ignore_index=True, subset=['transaction_hash', 'token_number', 'internal_token_number'])
        # add rounded timestamp to a minute
        records_df['rounded_timestamp'] = records_df['consensusTimestamp'].dt.floor('min')
        # add high level transaction type based on txn_type

        return records_df

    def aggregate_recordstreams_by_type(self, records_df):
        # Aggregate record streams DataFrame
        # Count the number of transactions per minute per txn_type
        group_txn = records_df.groupby(['rounded_timestamp', 'txn_type']).agg(
            transaction_count=pd.NamedAgg(column="transaction_hash", aggfunc="count"),
            send_amount=pd.NamedAgg(column="send_amount", aggfunc="sum"),
            receive_amount=pd.NamedAgg(column="receive_amount", aggfunc="sum")
        ).reset_index()
        group_txn['tps'] = group_txn['transaction_count'] / 60
          
        return group_txn

    def aggregate_recordstreams_by_token(self, records_df):
        # Aggregate data by internal_token_number
        group_txn = records_df.groupby(['rounded_timestamp', 'internal_token_number']).agg(
            transaction_count=pd.NamedAgg(column="transaction_hash", aggfunc="count"),
            send_amount=pd.NamedAgg(column="send_amount", aggfunc="sum"),
            receive_amount=pd.NamedAgg(column="receive_amount", aggfunc="sum")
        ).reset_index()

        # caculate distinct payer, sender and receiver
        exploded_df = records_df.explode('payer').explode('sender').explode('receiver')
        group_user_df = exploded_df.groupby(['rounded_timestamp', 'internal_token_number']).agg(
            distinct_payers=pd.NamedAgg(column='payer', aggfunc=pd.Series.nunique),
            distinct_receivers=pd.NamedAgg(column='receiver', aggfunc=pd.Series.nunique),
            distinct_senders=pd.NamedAgg(column='sender', aggfunc=pd.Series.nunique)
        ).reset_index()

        # merge group_txn and group_user_df
        group_txn = pd.merge(group_txn, group_user_df, on=['rounded_timestamp', 'internal_token_number'], how='left')

        return group_txn

    def run(self):
        self.logger.info("Run method started ...")
        try:
            self.logger.info(f"Reading data from {self.options.input_file} ...")
            records = self.read_data(self.options.input_file, Txn)
            simplified_records = self.transform_data(records)
            records_df = self.rcdstreams_to_pd_df(simplified_records)
            # write synthetic data to a file
            output_filename = f"{self.options.output_folder}/{self.script_name}_synthetic_data"
            self.logger.info(f"Writing synthetic data to {output_filename} ...")
            self.write_df_to_file(output_filename, records_df)
            cleaned_records = self.clean_records_df(records_df)
            # Count unique number of account per minute
            aggregate_recordstreams_by_type = self.aggregate_recordstreams_by_type(cleaned_records)
            aggregate_recordstreams_by_token = self.aggregate_recordstreams_by_token(cleaned_records)
            # Write the aggregated output to a JSON file
            output_filename_type = f"{self.options.output_folder}/{self.script_name}_by_type"
            self.logger.info(f"Writing aggregated output to {output_filename_type} ...")
            self.write_df_to_file(output_filename_type, aggregate_recordstreams_by_type)
            output_filename_topics = f"{self.options.output_folder}/{self.script_name}_by_token"
            self.logger.info(f"Writing aggregated output to {output_filename_topics} ...")
            self.write_df_to_file(output_filename_topics, aggregate_recordstreams_by_token)
            self.logger.info("Run method completed ...")
        except Exception as e:
            self.logger.exception("Fatal Error!")
            self.logger.info(e)
            exit(1)

if __name__ == "__main__":
    myObject = HTS()
    myObject.run()
