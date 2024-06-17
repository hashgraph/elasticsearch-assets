import os
import sys

import pandas as pd

# Add the path to the utils module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from metrics.utils.common import BaseScript
from model import Txn


class NFTS(BaseScript):
    def __init__(self):
        super().__init__(log_filename="non_fungible_token_stats")
        # Your HTS-specific initialization code here
        self.script_name = os.path.basename(__file__[:-3])
    
    def transform_data(self, records):
        # Extract only timestamp and unnested accountNum from the transfer_list column
        simplified_records = []
        for record in records:
            if record['status'] == '22' and ('NFT' in record['txn_type'] or 'TOKEN' in record['txn_type']):
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
                        # Filter out fungible token
                        if (token['nftTransfers'] is None) and ('TOKEN' in record['txn_type']):
                            continue
                        # overwrite internal_token_number when token_number is present
                        flat_records['internal_token_number'] = token['token']['tokenNum']
                        # initialize sender/receiver/series
                        flat_records['sender'] = []
                        flat_records['receiver'] = []
                        flat_records['series'] = []
                        if token['nftTransfers'] is not None:
                            # list sender/receiver
                            for transfer in token['nftTransfers']:
                                flat_records['sender'].append(transfer['senderAccountID']['accountNum'])
                                flat_records['receiver'].append(transfer['receiverAccountID']['accountNum'])
                                flat_records['series'].append(transfer['serialNumber'])
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
        # Count the number of transactions per txn_type
        group_txn = records_df.groupby(['txn_type']).agg(
            transaction_count=pd.NamedAgg(column="transaction_hash", aggfunc="count")
        ).reset_index()
        # Get total number of transactions
        total_txn = group_txn['transaction_count'].sum()
        total_df = pd.DataFrame({'txn_type': 'total', 'transaction_count': total_txn}, index=[0])
        # combine total_df with group_txn
        group_txn = pd.concat([group_txn, total_df], ignore_index=True)
          
        return group_txn

    def aggregate_recordstreams_by_token(self, records_df):
        # Aggregate data by internal_token_number
        group_txn = records_df.groupby(['internal_token_number', 'txn_type']).agg(
            transaction_count=pd.NamedAgg(column="transaction_hash", aggfunc="count")
        ).reset_index()

        return group_txn
    
    def aggregate_recordstreams_by_account(self, records_df):
        # explode payer column
        payer_df = records_df.explode('payer')
        # Aggregate data by account
        group_txn = payer_df.groupby(['payer']).agg(
            transaction_count=pd.NamedAgg(column="transaction_hash", aggfunc="count")
        ).reset_index()
        group_txn['data_type'] = 'payer'
        group_txn.rename(columns={'payer': 'accountNum'}, inplace=True)

        # explode sender column
        sender_df = records_df.explode('sender')
        # Aggregate data by account
        group_txn_sender = sender_df.groupby(['sender']).agg(
            transaction_count=pd.NamedAgg(column="transaction_hash", aggfunc="count")
        ).reset_index()
        group_txn_sender['data_type'] = 'sender'
        group_txn_sender.rename(columns={'sender': 'accountNum'}, inplace=True)

        # explode receiver column
        receiver_df = records_df.explode('receiver')
        # Aggregate data by account
        group_txn_receiver = receiver_df.groupby(['receiver']).agg(
            transaction_count=pd.NamedAgg(column="transaction_hash", aggfunc="count")
        ).reset_index()
        group_txn_receiver['data_type'] = 'receiver'
        group_txn_receiver.rename(columns={'receiver': 'accountNum'}, inplace=True)

        # Combine all data
        group_txn = pd.concat([group_txn, group_txn_sender, group_txn_receiver], ignore_index=True)

        return group_txn
    
    def write_df_to_file(self, output_filename, output_df):
        output_filename = f"{output_filename}_{self.starttime.strftime('%Y%m%d%H%M%S')}.{self.options.output_format}"
        if self.options.output_format == 'json':    
            # Write output to JSON file
            output_df.to_json(output_filename, orient='records', lines=True)
        elif self.options.output_format == 'csv':
            # Write output to CSV file
            output_df.to_csv(output_filename, index=False)
        else:
            raise Exception("Invalid output format")

    def run(self):
        self.logger.info("Run method started ...")
        try:
            self.logger.info(f"Reading data from {self.options.input_file} ...")
            records = self.read_data(self.options.input_file, Txn)
            simplified_records = self.transform_data(records)
            if len(simplified_records) == 0:
                self.logger.info("No NFT records to process ...")
                exit(0)
            records_df = self.rcdstreams_to_pd_df(simplified_records)
            # write synthetic data to a file
            output_filename = f"{self.options.output_folder}/{self.script_name}_synthetic_data"
            self.logger.info(f"Writing synthetic data to {output_filename} ...")
            self.write_df_to_file(output_filename, records_df)
            cleaned_records = self.clean_records_df(records_df)
            # Aggregated data by type
            aggregate_recordstreams_by_type = self.aggregate_recordstreams_by_type(cleaned_records)
            # Aggregated data by token
            aggregate_recordstreams_by_token = self.aggregate_recordstreams_by_token(cleaned_records)
            # Aggregated data by account
            aggregate_recordstreams_by_account = self.aggregate_recordstreams_by_account(cleaned_records)
            # Write the aggregated output to a JSON file
            output_filename_type = f"{self.options.output_folder}/{self.script_name}_by_type"
            self.logger.info(f"Writing aggregated output to {output_filename_type} ...")
            self.write_df_to_file(output_filename_type, aggregate_recordstreams_by_type)
            output_filename_topics = f"{self.options.output_folder}/{self.script_name}_by_token"
            self.logger.info(f"Writing aggregated output to {output_filename_topics} ...")
            self.write_df_to_file(output_filename_topics, aggregate_recordstreams_by_token)
            output_filename_account = f"{self.options.output_folder}/{self.script_name}_by_account"
            self.logger.info(f"Writing aggregated output to {output_filename_account} ...")
            self.write_df_to_file(output_filename_account, aggregate_recordstreams_by_account)
            self.logger.info("Run method completed ...")
        except Exception as e:
            self.logger.exception("Fatal Error!")
            self.logger.info(e)
            exit(1)

if __name__ == "__main__":
    myObject = NFTS()
    myObject.run()
