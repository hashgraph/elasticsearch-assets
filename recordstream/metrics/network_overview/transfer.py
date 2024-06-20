import os
import sys
import pandas as pd


# Add the path to the utils module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from metrics.utils.common import BaseScript
from model import TxnWithTransfer

class NetworkOverview(BaseScript):
    def __init__(self):
        super().__init__(log_filename="network_overview_transfer")
        # Your HTS-specific initialization code here
        self.script_name = os.path.basename(__file__[:-3])
    
    def map_txn_type(self, txn_type):
        """
        Maps a transaction type to a specific category.

        Args:
            txn_type (str): The transaction type to be mapped.

        Returns:
            str: The mapped category for the transaction type.
        """
        if 'CRYPTO' in txn_type:
            return 'CRYPTO'
        elif 'CONSENSUS' in txn_type:
            return 'CONSENSUS'
        elif 'TOKEN' in txn_type:
            return 'TOKEN'
        elif 'NFT' in txn_type:
            return 'NFT'
        elif 'CONTRACT' in txn_type:
            return 'CONTRACT'
        elif 'FILE' in txn_type:
            return 'FILE'
        elif 'ETHEREUM' in txn_type:
            return 'ETHEREUM'
        elif 'NODESTAKE' in txn_type:
            return 'NODESTAKE'
        else:
            return 'OTHER'
    
    def classify_transfer_type(self, transfer_amount):
        """
        Classifies the transfer type based on the transfer amount.

        Args:
            transfer_amount (int): The amount of the transfer.

        Returns:
            str: The classification of the transfer type.

        """
        if transfer_amount > 1_000_000_000:
            return 'gigantic_txn'
        
        if transfer_amount > 10_000_000:
            return 'huge_txns'
        
        if transfer_amount > 10_000:
            return 'large_txn'
        
        if transfer_amount > 1_000:
            return 'medium_txn'
        
        if transfer_amount > 10:
            return 'small_txn'
        
        if transfer_amount <= 10:
            return 'micro_txn'
        
    def transform_data(self, records):
        """
        Transforms the given records into a simplified format.

        Args:
            records (list): A list of records to be transformed.

        Returns:
            list: A list of simplified records.

        """
        simplified_records = []
        for record in records:
            if record['status'] == '22':
                flat_record = {
                    'txn_type': record['txn_type'],
                    'group_txn_type': self.map_txn_type(record['txn_type']),
                    'transaction_hash' : record['transaction_hash'],
                    'consensusTimestamp': record['consensusTimestamp'],
                    'node_id': record['node_id'] if 'node_id' in record else 0,
                    'payer': record['payer'],
                    'sender': [],
                    'receiver': [],
                    'transaction_fee': record['transaction_fee']/100_000_000,
                    'total_transfer': 0,
                    'network_fee': 0,
                    'node_fee': 0,
                    'send_amount': [],
                    'receive_amount': []
                }
                if record['transfer_list'] is None:
                    simplified_records.append(flat_record)
                    continue
                transfer_list = record.get('transfer_list', [])
                total_transfer = 0
                for transfer in transfer_list:
                    account_id = transfer['accountID']['accountNum']
                    amount = transfer['amount']/100_000_000
                    if amount < 0:
                        flat_record['sender'].append({
                            'sender_id': account_id,
                            'amount': amount
                        })
                        total_transfer += abs(amount)
                    else:
                        if account_id == 98:
                            flat_record['network_fee'] = amount
                        elif account_id in range(1, 35):
                            flat_record['node_fee'] = amount
                        else:
                            flat_record['receiver'].append({
                                'receiver_id': account_id,
                                'amount': amount
                            })
                flat_record['total_transfer'] = total_transfer
                flat_record['transfer_type'] = self.classify_transfer_type(flat_record['total_transfer'])
                simplified_records.append(flat_record)
        return simplified_records

    def clean_records_df(self, records_df):
        """
        Clean the records DataFrame by performing the following operations:
        - Remove duplicate records based on the 'transaction_hash' column.
        - Add a new column 'rounded_timestamp' that contains the rounded timestamp to the nearest minute.
        - Add a high-level transaction type based on the 'txn_type' column.

        Args:
            records_df (pandas.DataFrame): The DataFrame containing the records.

        Returns:
            pandas.DataFrame: The cleaned records DataFrame.
        """
        records_df.drop_duplicates(inplace=True, ignore_index=True, subset=['transaction_hash'])
        records_df['rounded_timestamp'] = records_df['consensusTimestamp'].dt.floor('min')

        # Add high level transaction type based on txn_type

        return records_df

    def overall_transfer(self, records_df):
        """
        Calculate the overall transfer metrics based on the provided records DataFrame.

        Parameters:
            records_df (pandas.DataFrame): The DataFrame containing the records.

        Returns:
            pandas.DataFrame: The aggregated records DataFrame with total transfer, network fee, node fee,
                              send amount, and receive amount.

        """
        # Aggregate records to calculate total transfer, network fee, node fee, send amount, receive amount
        aggregated_records = records_df.groupby(['rounded_timestamp']).agg(
            total_transfer=('total_transfer', 'sum'),
            network_fee=('network_fee', 'sum'),
            node_fee=('node_fee', 'sum'),
            txn_count=('transaction_hash', 'count'),
        ).reset_index()
        return aggregated_records

    def transfer_by_type(self, records_df):
        """
        Aggregate records by transfer type to calculate total transfer.

        Args:
            records_df (pandas.DataFrame): The input DataFrame containing records.

        Returns:
            pandas.DataFrame: The aggregated DataFrame with columns for rounded timestamp, transfer type,
            transaction count, and total transfer.
        """
        # Aggregate records to calculate total transfer, network fee, node fee, send amount, receive amount
        aggregated_records = records_df.groupby(['rounded_timestamp', 'transfer_type']).agg(
            txn_count=('transaction_hash', 'count'),
            total_transfer=('total_transfer', 'sum'),
        ).reset_index()
        return aggregated_records

    def aggregate_by_payer(self, records_df):
        """
        Aggregate records by payer to calculate various metrics.

        Parameters:
        - records_df (pandas.DataFrame): DataFrame containing the records to be aggregated.

        Returns:
        - pandas.DataFrame: DataFrame with aggregated metrics for each payer.
        """
        # Aggregate records to calculate total transfer, network fee, node fee, send amount, receive amount
        payer_transfer = records_df.groupby(['rounded_timestamp', 'payer']).apply(
            lambda x: pd.Series({
                'total_transfer': x['total_transfer'].sum(),
                'network_fee': x['network_fee'].sum(),
                'node_fee': x['node_fee'].sum(),
                'txn_count': x['transaction_hash'].count(),
                'crypto_txn_count': x[x['group_txn_type'].str.contains('CRYPTO')]['transaction_hash'].count(),
                'consensus_txn_count': x[x['group_txn_type'].str.contains('CONSENSUS')]['transaction_hash'].count(),
                'token_txn_count': x[x['group_txn_type'].str.contains('TOKEN')]['transaction_hash'].count(),
                'nft_txn_count': x[x['group_txn_type'].str.contains('NFT')]['transaction_hash'].count(),
                'contract_txn_count': x[x['group_txn_type'].str.contains('CONTRACT')]['transaction_hash'].count(),
                'file_txn_count': x[x['group_txn_type'].str.contains('FILE')]['transaction_hash'].count(),
                'ethereum_txn_count': x[x['group_txn_type'].str.contains('ETHEREUM')]['transaction_hash'].count(),
                'staking_txn_count': x[x['group_txn_type'].str.contains('NODESTAKE')]['transaction_hash'].count(),
                'other_txn_count': x[~x['group_txn_type'].str.contains('CRYPTO|CONSENSUS|TOKEN|NFT|CONTRACT|FILE|ETHEREUM|NODESTAKE')]['transaction_hash'].count()
            })).reset_index()
        return payer_transfer

    def aggregate_by_sender(self, records_df):
        """
        Aggregate records by sender to calculate total transfer, network fee, node fee, send amount, and receive amount.

        Args:
            records_df (pandas.DataFrame): The DataFrame containing the records.

        Returns:
            pandas.DataFrame: The aggregated DataFrame with calculated metrics for each receiver.
                The DataFrame contains the following columns:
                - rounded_timestamp: The rounded timestamp of the record.
                - sender_id: The ID of the receiver.
                - txn_count: The number of transactions received by the receiver.
                - sender_transfer: The total amount received by the receiver.
                - crypto_txn_count: The number of cryptocurrency transactions received by the receiver.
                - token_txn_count: The number of token transactions received by the receiver.
        """
        # Aggregate records to calculate total transfer, network fee, node fee, send amount, receive amount
        # Normalize and explode the sender column
        sender_df = records_df.explode('sender').reset_index(drop=True)
        sender_normalized = pd.json_normalize(sender_df['sender'])

        # Combine the exploded sender DataFrame with the original DataFrame
        df = pd.concat([sender_df.drop(columns='sender'), sender_normalized], axis=1)

        sender_transfer = df.groupby(['rounded_timestamp', 'sender_id']).apply(
            lambda x: pd.Series({
                'txn_count': x['transaction_hash'].count(),
                'send_transfer': x['amount'].sum(),
                'crypto_txn_count': x[x['group_txn_type'].str.contains('CRYPTO')]['transaction_hash'].nunique(),
                'token_txn_count': x[x['group_txn_type'].str.contains('TOKEN')]['transaction_hash'].nunique(),
            })).reset_index()
        return sender_transfer
    
    def aggregate_by_receiver(self, records_df):
        """
        Aggregate records by receiver.

        Args:
            records_df (pandas.DataFrame): The DataFrame containing the records.

        Returns:
            pandas.DataFrame: The aggregated DataFrame with calculated metrics for each receiver.
                The DataFrame contains the following columns:
                - rounded_timestamp: The rounded timestamp of the record.
                - receiver_id: The ID of the receiver.
                - txn_count: The number of transactions received by the receiver.
                - receive_transfer: The total amount received by the receiver.
                - crypto_txn_count: The number of cryptocurrency transactions received by the receiver.
                - token_txn_count: The number of token transactions received by the receiver.
        """
        # Aggregate records to calculate total transfer, network fee, node fee, send amount, receive amount
        # Normalize and explode the receiver column
        receiver_df = records_df.explode('receiver').reset_index(drop=True)
        receiver_normalized = pd.json_normalize(receiver_df['receiver'])

        # Combine the exploded receiver DataFrame with the original DataFrame
        df = pd.concat([receiver_df.drop(columns='receiver'), receiver_normalized], axis=1)

        receiver_transfer = df.groupby(['rounded_timestamp', 'receiver_id']).apply(
            lambda x: pd.Series({
                'txn_count': x['transaction_hash'].count(),
                'receive_transfer': x['amount'].sum(),
                'crypto_txn_count': x[x['group_txn_type'].str.contains('CRYPTO')]['transaction_hash'].nunique(),
                'token_txn_count': x[x['group_txn_type'].str.contains('TOKEN')]['transaction_hash'].nunique(),
            })).reset_index()
        return receiver_transfer

    def run(self):
        """
        Executes the main logic of the transfer script.

        This method reads data from an input file, performs data transformation and cleaning,
        aggregates the records based on different criteria, and writes the aggregated data to output files.

        Raises:
            Exception: If any error occurs during the execution of the script.

        Returns:
            None
        """
        self.logger.info("Run method started ...")
        try:
            self.logger.info(f"Reading data from {self.options.input_file}...")
            records = self.read_data(self.options.input_file, TxnWithTransfer)
            simplified_records = self.transform_data(records)
            records_df = self.rcdstreams_to_pd_df(simplified_records)
            cleaned_records = self.clean_records_df(records_df)
            # Aggregate records to calculate total transfer, network fee, node fee & transaction count
            overall_transfer = self.overall_transfer(cleaned_records)
            output_name = f"{self.options.output_folder}/{self.script_name}_overall"
            self.logger.info(f"Writing output to {output_name}...")
            self.write_df_to_file(output_name, overall_transfer)
            # Aggregate records to classify transfer type
            transfer_by_type = self.transfer_by_type(cleaned_records)
            output_name = f"{self.options.output_folder}/{self.script_name}_by_type"
            self.logger.info(f"Writing output to {output_name}...")
            self.write_df_to_file(output_name, transfer_by_type)
            # Aggregate records by payer
            payer_transfer = self.aggregate_by_payer(cleaned_records)
            output_name = f"{self.options.output_folder}/{self.script_name}_by_payer"
            self.logger.info(f"Writing output to {output_name}...")
            self.write_df_to_file(output_name, payer_transfer)
            # Aggregate records by sender
            sender_transfer = self.aggregate_by_sender(cleaned_records)
            output_name = f"{self.options.output_folder}/{self.script_name}_by_sender"
            self.logger.info(f"Writing output to {output_name}...")
            self.write_df_to_file(output_name, sender_transfer)
            # Aggregate records by receiver
            receiver_transfer = self.aggregate_by_receiver(cleaned_records)
            output_name = f"{self.options.output_folder}/{self.script_name}_by_receiver"
            self.logger.info(f"Writing output to {output_name}...")
            self.write_df_to_file(output_name, receiver_transfer)
        except Exception as e:
            self.logger.exception("Fatal Error!")
            self.logger.info(e)
            exit(1)

if __name__ == "__main__":
    myObject = NetworkOverview()
    myObject.run()
