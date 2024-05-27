import json
from optparse import OptionParser
import os
import logging
import logging.config
import datetime

from pydantic import BaseModel, Field
import pandas as pd


class Txn(BaseModel):
    status: str
    node_id: str = Field(alias="body.nodeAccountID.accountNum")
    transaction_hash: str = Field(alias="record.transactionHash")
    txn_type: str
    processed_timestamp:  datetime.datetime = Field(alias="@processed")
    consensusTimestamp: datetime.datetime
    consensus_create_topicID: int | None = None
    consensus_submit_topicID: int | None = None
    consensus_update_topicID: int | None = None
    consensus_delete_topicID: int | None = None
    consensus_submit_message_bytes: int | None = None


class NetworkOverview:
    def __init__(self):
        self.starttime = datetime.datetime.now()
        self.script_name = os.path.basename(__file__[:-3])

        # Initialize the parameters
        self.__init_params__()
        self.logger = self.init_log()
        self.__init_env_var__()

    def __init_env_var__(self):
        # Get the environment variables
        self.path = os.getenv("PATH")
        if self.path is None:
            raise Exception("Environment variable PATH is not set")
        else:
            self.logger.info("Environment variable PATH=%s", self.path)
    
    def __init_params__(self):
        # Initialize the parameters
        parser = OptionParser(usage="%prog [OPTIONS] ...")

        parser.add_option(
            "-i", "--input_file",
            action="store",
            type=str,
            dest="input_file",
            help="Path to the recordstream input file")

        parser.add_option(
            "-o", "--output_folder",
            action="store",
            type=str,
            dest="output_folder",
            help="Path to the output folder")

        parser.add_option(
            "-l", "--level", 
            default="INFO",
            action="store",
            type=str,
            dest="log_level",
            help="Set the logging level. [DEBUG|INFO|WARNING|ERROR|CRITICAL]")

        # parse the arguments
        (self.options, self.__args) = parser.parse_args()
        
        # validate input parameters
        if not os.path.exists(self.options.input_file):
            raise Exception("Input file does not exist")
        if not os.path.exists(self.options.output_folder):
            raise Exception("Output folder does not exist")
        
        print("Input file: %s", self.options.input_file)
        print("Output folder: %s", self.options.output_folder)
        print("Log level: %s", self.options.log_level)

    def init_log(self):
        """
        Initialise the log file
        """
        level = "INFO"

        if self.options.log_level == "DEBUG":
            level = logging.DEBUG
        elif self.options.log_level == "INFO":
            level = logging.INFO
        elif self.options.log_level == "WARNING":
            level = logging.WARNING
        elif self.options.log_level == "ERROR":
            level = logging.ERROR
        elif self.options.log_level == "CRITICAL":
            level = logging.CRITICAL

        logging.basicConfig(filename=os.path.join(self.options.output_folder + '/' + self.script_name + '.log'),
                            level=level,
                            format='%(asctime)s.%(msecs)03d %(levelname)5s: %(name)s %(message)s')
        logger = logging.getLogger(self.script_name)
        logger.info("Logger started ...")
        return logger

    def read_data(self, file_path) -> list[dict]:
        txns = []
        with open(file_path, 'r') as file:
            for line in file:
                data = json.loads(line)
                txn = Txn(**data)
                txns.append(txn.dict())
        return txns
    
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
       
    def write_to_json(self, output_filename, output_df):
        # Write output to JSON file
        output_df.to_json(output_filename, orient='records', lines=True)

    def run(self):
        self.logger.info("Run method started ...")
        try:
            self.logger.info(f"Reading data from {self.options.input_file} ...")
            records = self.read_data(self.options.input_file)
            simplified_records = self.transform_data(records)
            records_df = self.rcdstreams_to_pd_df(simplified_records)
            cleaned_records = self.clean_records_df(records_df)
            # Count unique number of account per minute
            aggregate_recordstreams_by_type = self.aggregate_recordstreams_by_type(cleaned_records)
            aggregate_recordstreams_by_submitted_topics = self.aggregate_recordstreams_submitted_topics(cleaned_records)
            # Write the aggregated output to a JSON file
            output_filename_type = f"{self.options.output_folder}/{self.script_name}_hcs_by_type.json"
            self.logger.info(f"Writing aggregated output to {output_filename_type} ...")
            self.write_to_json(output_filename_type, aggregate_recordstreams_by_type)
            output_filename_topics = f"{self.options.output_folder}/{self.script_name}_hcs_by_submitted_topics.json"
            self.logger.info(f"Writing aggregated output to {output_filename_topics} ...")
            self.write_to_json(output_filename_topics, aggregate_recordstreams_by_submitted_topics)
            self.logger.info("Run method completed ...")
        except Exception as e:
            self.logger.exception("Fatal Error!")
            self.logger.info(e)
            exit(1)

if __name__ == "__main__":
    myObject = NetworkOverview()
    myObject.run()
