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
        super().__init__(log_filename="network_overview")
        # Your HTS-specific initialization code here
        self.script_name = os.path.basename(__file__[:-3])

    def clean_records_df(self, records_df):
        # Clean records DataFrame
        records_df.drop_duplicates(inplace=True)
        # add rounded timestamp to a minute
        records_df['rounded_timestamp'] = records_df['consensusTimestamp'].dt.floor('min')
        # add high level transaction type based on txn_type

        return records_df

    def aggregate_recordstreams(self, records_df):
        # Aggregate record streams DataFrame
        # Filter out status != 22
        records_df = records_df[records_df['status'] == '22']
        # Get the total number of transactions by transaction type per minute
        network_overview = records_df.groupby(['rounded_timestamp', 'node_id'])['transaction_hash'].count().reset_index()
        return network_overview

    def run(self):
        self.logger.info("Run method started ...")
        try:
            self.logger.info(f"Reading data from {self.options.input_file}...")
            records = self.read_data(self.options.input_file, Txn)
            records_df = self.rcdstreams_to_pd_df(records)
            cleaned_records = self.clean_records_df(records_df)
            aggregated_records = self.aggregate_recordstreams(cleaned_records)
            output_name = f"{self.options.output_folder}/{self.script_name}"
            self.logger.info(f"Writing output to {output_name}...")
            self.write_df_to_file(output_name, aggregated_records)
        except Exception as e:
            self.logger.exception("Fatal Error!")
            self.logger.info(e)
            exit(1)

if __name__ == "__main__":
    myObject = NetworkOverview()
    myObject.run()
