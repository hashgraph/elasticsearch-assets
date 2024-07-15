import os
import sys

import pandas as pd

# Add the path to the utils module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from metrics.utils.common import BaseScript
from token_services.model import Txn


class NFTS(BaseScript):
    def __init__(self):
        super().__init__(log_filename="non_fungible_token_stats")
        # Your HTS-specific initialization code here
        self.script_name = os.path.basename(__file__[:-3])
    
    def transform_data(self, records):
        """
        Transforms the given records by extracting relevant information and returning a simplified list of records.
        Filter for TOKEN transaction and remove records with status != 22

        Args:
            records (list): A list of records to be transformed.

        Returns:
            list: A simplified list of records containing the extracted information.

        """
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

    def clean_records_df(self, records_df):
        """
        Clean the records DataFrame by performing the following operations:
        1. Remove duplicate rows based on 'transaction_hash', 'token_number', and 'internal_token_number' columns.
        2. Add a new column 'rounded_timestamp' that contains the rounded timestamp to the nearest minute.
        3. Add a new column 'high_level_transaction_type' based on the 'txn_type' column.

        Args:
            records_df (pandas.DataFrame): The DataFrame containing the records.

        Returns:
            pandas.DataFrame: The cleaned records DataFrame.
        """
        records_df.drop_duplicates(inplace=True, ignore_index=True, subset=['transaction_hash', 'token_number', 'internal_token_number'])
        records_df['rounded_timestamp'] = records_df['consensusTimestamp'].dt.floor('min')
        # add high level transaction type based on txn_type

        return records_df

    def aggregate_recordstreams_by_type(self, records_df):
        """
        Aggregate the record streams DataFrame by transaction type.

        Args:
            records_df (pandas.DataFrame): The DataFrame containing the record streams.

        Returns:
            pandas.DataFrame: The aggregated DataFrame with the count of transactions per transaction type.
        """
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
        """
        Aggregates the given records DataFrame by internal_token_number and txn_type.

        Args:
            records_df (pandas.DataFrame): The DataFrame containing the records.

        Returns:
            pandas.DataFrame: The aggregated DataFrame with columns internal_token_number, txn_type, and transaction_count.
        """
        # Aggregate data by internal_token_number
        group_txn = records_df.groupby(['internal_token_number', 'txn_type']).agg(
            transaction_count=pd.NamedAgg(column="transaction_hash", aggfunc="count")
        ).reset_index()

        return group_txn
    
    def aggregate_recordstreams_by_account(self, records_df):
        """
        Aggregates record streams by account.

        Args:
            records_df (DataFrame): The input DataFrame containing the records.

        Returns:
            DataFrame: The aggregated data grouped by account.

        """
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

    def run(self):
        """
        Executes the main logic of the NFT script.
        
        Reads data from the input file, processes and aggregates the records,
        and writes the output to separate files.
        """
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
