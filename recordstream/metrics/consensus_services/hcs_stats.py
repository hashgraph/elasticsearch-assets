import os
import sys

import pandas as pd

# Add the path to the utils module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from metrics.utils.common import BaseScript
from model import Txn


class NetworkOverview(BaseScript):
    def __init__(self):
        super().__init__(log_filename="consensus_services")
        # Your HTS-specific initialization code here
        self.script_name = os.path.basename(__file__[:-3])
    
    def transform_data(self, records):
        # Extract only timestamp and unnested accountNum from the transfer_list column
        simplified_records = [
            record 
            for record in records 
            if record['status'] == '22'
            and ('CONSENSUS' in record['txn_type'])
        ]
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

    # Define a custom function to count distinct non-zero values
    def count_distinct_non_zero(self, series):
        return series[series != 0].nunique()

    def aggregate_recordstreams_by_type(self, records_df):
        # Aggregate record streams DataFrame
        # Count the number of transactions per minute per txn_type
        group_txn = records_df.groupby(['rounded_timestamp', 'txn_type']).agg(
            transaction_count=pd.NamedAgg(column="transaction_hash", aggfunc="count"),
            consensus_bytes=pd.NamedAgg(column="consensus_submit_message_bytes", aggfunc="sum"),
            consensus_create_topicID=pd.NamedAgg(column="consensus_create_topicID", aggfunc=self.count_distinct_non_zero),
            consensus_submit_topicID=pd.NamedAgg(column="consensus_submit_topicID", aggfunc=self.count_distinct_non_zero),
            consensus_update_topicID=pd.NamedAgg(column="consensus_update_topicID", aggfunc=self.count_distinct_non_zero),
            consensus_delete_topicID=pd.NamedAgg(column="consensus_delete_topicID", aggfunc=self.count_distinct_non_zero)
        ).reset_index()
        group_txn['tps'] = group_txn['transaction_count'] / 60
        return group_txn
    
    def aggregate_recordstreams_submitted_topics(self, records_df):
        # Aggregate record streams DataFrame for CONSENSUSSUBMITMESSAGE
        group_txn = records_df.groupby(['rounded_timestamp', 'consensus_submit_topicID']).agg(
            transaction_count=pd.NamedAgg(column="transaction_hash", aggfunc="count"),
            consensus_bytes=pd.NamedAgg(column="consensus_submit_message_bytes", aggfunc="sum")
        ).reset_index()
        group_txn['tps'] = group_txn['transaction_count'] / 60
        return group_txn

    def run(self):
        self.logger.info("Run method started ...")
        try:
            self.logger.info(f"Reading data from {self.options.input_file} ...")
            records = self.read_data(self.options.input_file, Txn)
            simplified_records = self.transform_data(records)
            records_df = self.rcdstreams_to_pd_df(simplified_records)
            cleaned_records = self.clean_records_df(records_df)
            # Count unique number of account per minute
            aggregate_recordstreams_by_type = self.aggregate_recordstreams_by_type(cleaned_records)
            aggregate_recordstreams_by_submitted_topics = self.aggregate_recordstreams_submitted_topics(cleaned_records)
            # Write the aggregated output to a JSON file
            output_filename_type = f"{self.options.output_folder}/{self.script_name}_hcs_by_type"
            self.logger.info(f"Writing aggregated output to {output_filename_type} ...")
            self.write_df_to_file(output_filename_type, aggregate_recordstreams_by_type)
            output_filename_topics = f"{self.options.output_folder}/{self.script_name}_hcs_by_submitted_topics"
            self.logger.info(f"Writing aggregated output to {output_filename_topics} ...")
            self.write_df_to_file(output_filename_topics, aggregate_recordstreams_by_submitted_topics)
            self.logger.info("Run method completed ...")
        except Exception as e:
            self.logger.exception("Fatal Error!")
            self.logger.info(e)
            exit(1)

if __name__ == "__main__":
    myObject = NetworkOverview()
    myObject.run()
