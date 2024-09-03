import os
import sys
import pandas as pd


# Add the path to the utils module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from metrics.utils.common import BaseScript
from network_overview.model import Txn

service_mapping = {
    "CONTRACTCREATEINSTANCE": "HSCS",
    "CONTRACTUPDATEINSTANCE": "HSCS",
    "NFTCREATION": "HTS",
    "TOKENCREATION": "HTS",
    "CONSENSUSCREATETOPIC": "HCS",
    "CONSENSUSUPDATETOPIC": "HCS",
}

class DeveloperActivities(BaseScript):
    def __init__(self):
        super().__init__(log_filename="developer_activities")
        # Your HTS-specific initialization code here
        self.script_name = os.path.basename(__file__[:-3])

    def filter_records(self, records):
        """
        Filters the given records based on the status and txn_type.

        Args:
            records (list): A list of records to be filtered.

        Returns:
            list: A filtered list of records with status == '22' and txn_type in developer_activities.
        """
        developer_activities = ["CONTRACTCREATEINSTANCE", "CONTRACTUPDATEINSTANCE", "TOKENCREATION", "NFTCREATION", "CONSENSUSCREATETOPIC", "CONSENSUSUPDATETOPIC"]
        filter_records = [record for record in records if (record['status'] == '22') and record['txn_type'] in developer_activities]
        return filter_records
    
    def clean_records_df(self, records_df):
        """
        Clean the records DataFrame by performing the following operations:
        1. Remove duplicate rows.
        2. Add a rounded timestamp to the nearest minute based on the 'consensusTimestamp' column.
        3. Add a high-level transaction type based on the 'txn_type' column.

        Args:
            records_df (pandas.DataFrame): The DataFrame containing the records.

        Returns:
            pandas.DataFrame: The cleaned records DataFrame.
        """
        # Clean records DataFrame
        records_df.drop_duplicates(inplace=True)
        records_df['rounded_timestamp'] = records_df['consensusTimestamp'].dt.floor('min')
        records_df['service'] = records_df['txn_type'].map(service_mapping)
        return records_df

    def aggregated_by_service(self, records_df):
        """
        Aggregate the record streams DataFrame by rounded timestamp and service.

        Args:
            records_df (DataFrame): The input DataFrame containing the records.

        Returns:
            DataFrame: The aggregated DataFrame with the total number of transactions and unique developers per minute, 
                       grouped by rounded timestamp and service.
        """
        # Aggregate record streams DataFrame
        # Get the total number of transactions by transaction type per minute
        group_txn = records_df.groupby(['rounded_timestamp', 'service']).agg(
            transaction_count=pd.NamedAgg(column='transaction_hash', aggfunc='count'),
            dev_count=pd.NamedAgg(column="payer", aggfunc="nunique")
        ).reset_index()
        return group_txn
    
    def aggregated_by_network(self, records_df):
        """
        Aggregate the record streams DataFrame by network.

        Args:
            records_df (DataFrame): The DataFrame containing the records.

        Returns:
            DataFrame: The aggregated DataFrame with the total number of transactions
                       by transaction type per minute and the number of unique developers.
        """
        # Aggregate record streams DataFrame
        # Get the total number of transactions by transaction type per minute
        group_txn = records_df.groupby(['rounded_timestamp']).agg(
            transaction_count=pd.NamedAgg(column='transaction_hash', aggfunc='count'),
            dev_count=pd.NamedAgg(column="payer", aggfunc="nunique")
        ).reset_index()
        return group_txn

    def run(self):
        """
        Executes the main logic of the developer activities script.

        This method reads data from an input file, filters the records, cleans the data,
        aggregates it by service and network, and writes the aggregated output to JSON files.

        Raises:
            Exception: If any fatal error occurs during the execution.

        Returns:
            None
        """
        self.logger.info("Run method started ...")
        try:
            self.logger.info(f"Reading data from {self.options.input_file}...")
            records = self.read_data(self.options.input_file, Txn)
            filtered_records = self.filter_records(records)
            if len(filtered_records) == 0:
                self.logger.info("No Developer Activities found")
                return
            records_df = self.rcdstreams_to_pd_df(filtered_records)
            cleaned_records = self.clean_records_df(records_df)
            # aggregated by service
            aggregated_by_service = self.aggregated_by_service(cleaned_records)
            # Write the aggregated output to a JSON file
            output_name = f"{self.options.output_folder}/{self.script_name}_aggregated_by_service"
            self.logger.info(f"Writing output to {output_name}...")
            self.write_df_to_file(output_name, aggregated_by_service)
            # aggregated by network
            aggregated_by_network = self.aggregated_by_network(cleaned_records)
            # Write the aggregated output to a JSON file
            output_name = f"{self.options.output_folder}/{self.script_name}_aggregated_by_network"
            self.logger.info(f"Writing output to {output_name}...")
            self.write_df_to_file(output_name, aggregated_by_network)
        except Exception as e:
            self.logger.exception("Fatal Error!")
            self.logger.info(e)
            exit(1)

if __name__ == "__main__":
    myObject = DeveloperActivities()
    myObject.run()
