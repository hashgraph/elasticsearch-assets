import os
import sys
import pandas as pd

# Add the path to the utils module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from metrics.utils.common import BaseScript
from model import Txn

class SmartContract(BaseScript):
    def __init__(self):
        super().__init__(log_filename="smart_contract_services")
        # Your HTS-specific initialization code here
        self.script_name = os.path.basename(__file__[:-3])
    
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
            if record['status'] == '22' and ('CONTRACT' in record['txn_type'] or 'ETHEREUM' in record['txn_type']):
                base_flat_record = {
                    'txn_type': record['txn_type'],
                    'transaction_hash': record['transaction_hash'],
                    'consensusTimestamp': record['consensusTimestamp'],
                    'contract_number': record['contractNum'],
                    'internal_contract_number': [record['contractNum']],
                    'gasUsed': record['gasUsed'],
                    'payer': [],
                    'other_associated_account': []
                }

                if record['transfer_list']:
                    base_flat_record['payer'] = [
                        transfer['accountID']['accountNum']
                        for transfer in record['transfer_list']
                        if transfer['amount'] < 0
                    ]
                    base_flat_record['other_associated_account'] = [
                        transfer['accountID']['accountNum']
                        for transfer in record['transfer_list']
                        if transfer['amount'] > 0
                    ]

                if record['contract_call_result'] or record['contract_create_result']:
                    base_flat_record['contract_number'] = record['contract_call_result']['contractID']['contractNum']
                    base_flat_record['gasUsed'] = record['contract_call_result']['gasUsed']
                    if record['contract_call_result']['logInfo']:
                        base_flat_record['internal_contract_number'] = [
                            record['contractID']['contractNum']
                            for record in record['contract_call_result']['logInfo']
                        ]
                    base_flat_record['created_contract_id'] = record['contract_call_result']['createdContractIDs']
                
                simplified_records.append(base_flat_record)
        return simplified_records

    def clean_records_df(self, records_df):
        """
        Clean the records DataFrame by performing the following operations:
        1. Remove duplicate rows based on 'transaction_hash' and 'contract_number' columns.
        2. Add a new column 'rounded_timestamp' which contains the rounded timestamp to the nearest minute.
        3. Add a new column 'high_level_txn_type' based on the 'txn_type' column.

        Args:
            records_df (pandas.DataFrame): The DataFrame containing the records.

        Returns:
            pandas.DataFrame: The cleaned records DataFrame.
        """
        # Clean records DataFrame
        records_df.drop_duplicates(inplace=True, ignore_index=True, subset=['transaction_hash', 'contract_number'])
        records_df['rounded_timestamp'] = records_df['consensusTimestamp'].dt.floor('min')
        # add high level transaction type based on txn_type

        return records_df

    def aggregate_recordstreams_by_type(self, records_df):
        """
        Aggregate record streams DataFrame by contract number, transaction type, and rounded timestamp.

        Args:
            records_df (DataFrame): The input DataFrame containing the records.

        Returns:
            DataFrame: The aggregated DataFrame with the following columns:
                - contract_number: The contract number.
                - txn_type: The transaction type.
                - rounded_timestamp: The rounded timestamp.
                - transaction_count: The number of transactions per minute per txn_type.
                - gas_used_total: The total gas used per minute per txn_type.
                - gas_used_max: The maximum gas used per minute per txn_type.
                - gas_used_min: The minimum gas used per minute per txn_type.
        """
        # Aggregate record streams DataFrame
        # Count the number of transactions per minute per txn_type
        group_txn = records_df.groupby(['contract_number', 'txn_type', 'rounded_timestamp']).agg(
            transaction_count=pd.NamedAgg(column="transaction_hash", aggfunc="count"),
            gas_used_total=pd.NamedAgg(column="gasUsed", aggfunc="sum"),
            gas_used_max=pd.NamedAgg(column="gasUsed", aggfunc="max"),
            gas_used_min=pd.NamedAgg(column="gasUsed", aggfunc="min"),
        ).reset_index()

        return group_txn

    def aggregate_recordstreams_by_contract(self, records_df):
        """
        Aggregate record streams by contract.

        Args:
            records_df (pandas.DataFrame): The DataFrame containing the records.

        Returns:
            DataFrame: The aggregated DataFrame with the following columns:
                - contract_number: The contract number.
                - transaction_count: The number of transactions.
                - gas_used_total: The total gas used.
                - gas_used_max: The maximum gas used.
                - gas_used_min: The minimum gas used.
        """
        # Aggregate data by internal_token_number
        group_txn = records_df.groupby(['contract_number']).agg(
            transaction_count=pd.NamedAgg(column="transaction_hash", aggfunc="count"),
            gas_used_total=pd.NamedAgg(column="gasUsed", aggfunc="sum"),
            gas_used_max=pd.NamedAgg(column="gasUsed", aggfunc="max"),
            gas_used_min=pd.NamedAgg(column="gasUsed", aggfunc="min"),
        ).reset_index()

        return group_txn
    
    def aggregate_recordstreams_by_account_contract(self, records_df):
        """
        Aggregates record streams by account and contract.

        Args:
            records_df (pandas.DataFrame): The input DataFrame containing the records.

        Returns:
            DataFrame: The aggregated DataFrame with the following columns:
                - contract_number: The contract number.
                - payer: The account number.
                - transaction_count: The number of transactions.
                - gas_used_total: The total gas used.

        """
        # Explode the payer column
        records_df = records_df.explode('payer')
        # Aggregate data by internal_token_number
        group_txn = records_df.groupby(['contract_number', 'payer']).agg(
            transaction_count=pd.NamedAgg(column="transaction_hash", aggfunc="count"),
            gas_used_total=pd.NamedAgg(column="gasUsed", aggfunc="sum")
        ).reset_index()

        return group_txn
    
    def aggregate_recordstreams_by_account(self, records_df):
        """
        Aggregates record streams by account.

        Args:
            records_df (pandas.DataFrame): The DataFrame containing the records.

        Returns:
            DataFrame: The aggregated data by payer and transaction type, including transaction count and total gas used.
        """
        # Explode the payer column
        records_df = records_df.explode('payer')
        # Aggregate data by internal_token_number
        group_txn = records_df.groupby(['payer', 'txn_type']).agg(
            transaction_count=pd.NamedAgg(column="transaction_hash", aggfunc="count"),
            gas_used_total=pd.NamedAgg(column="gasUsed", aggfunc="sum")
        ).reset_index()

        return group_txn

    def run(self):
            """
            Executes the main logic of the smart contract script.
            
            Reads data from an input file, performs data transformation and aggregation,
            and writes the results to output files.
            """
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
                # Aggreate data
                aggregate_recordstreams_by_type = self.aggregate_recordstreams_by_type(cleaned_records)
                aggregate_recordstreams_by_contract = self.aggregate_recordstreams_by_contract(cleaned_records)
                aggregate_recordstreams_by_account_contract = self.aggregate_recordstreams_by_account_contract(cleaned_records)
                aggregate_recordstreams_by_account = self.aggregate_recordstreams_by_account(cleaned_records)
                # Write the aggregated output to a JSON file
                output_filename_type = f"{self.options.output_folder}/{self.script_name}_by_type"
                self.logger.info(f"Writing aggregated output to {output_filename_type} ...")
                self.write_df_to_file(output_filename_type, aggregate_recordstreams_by_type)
                output_filename_contract = f"{self.options.output_folder}/{self.script_name}_by_contract"
                self.logger.info(f"Writing aggregated output to {output_filename_contract} ...")
                self.write_df_to_file(output_filename_contract, aggregate_recordstreams_by_contract)
                output_filename_account_contract = f"{self.options.output_folder}/{self.script_name}_by_account_contract"
                self.logger.info(f"Writing aggregated output to {output_filename_account_contract} ...")
                self.write_df_to_file(output_filename_account_contract, aggregate_recordstreams_by_account_contract)
                output_filename_account = f"{self.options.output_folder}/{self.script_name}_by_account"
                self.logger.info(f"Writing aggregated output to {output_filename_account} ...")
                self.write_df_to_file(output_filename_account, aggregate_recordstreams_by_account)
                self.logger.info("Run method completed ...")
            except Exception as e:
                self.logger.exception("Fatal Error!")
                self.logger.info(e)
                exit(1)

if __name__ == "__main__":
    myObject = SmartContract()
    myObject.run()
