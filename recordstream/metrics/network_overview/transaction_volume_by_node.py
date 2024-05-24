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
    transaction_hash: str = Field(alias="record.transactionHash")
    txn_type: str
    processed_timestamp:  datetime.datetime = Field(alias="@processed")
    consensusTimestamp: datetime.datetime
    node_id: str = Field(alias="body.nodeAccountID.accountNum")


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
        # Get the total number of transactions by transaction type per minute
        network_overview = records_df.groupby(['rounded_timestamp', 'node_id'])['transaction_hash'].count().reset_index()
        return network_overview

    def write_to_json(self, output_df):
        # Write output to JSON file
        output_df.to_json(f"{self.options.output_folder}/{self.script_name}.json", orient='records', lines=True)

    def run(self):
        self.logger.info("Run method started ...")
        try:
            records = self.read_data(self.options.input_file)
            records_df = self.rcdstreams_to_pd_df(records)
            cleaned_records = self.clean_records_df(records_df)
            aggregated_records = self.aggregate_recordstreams(cleaned_records)
            self.write_to_json(aggregated_records)
            self.logger.info("Total runtime: %s" % str(datetime.datetime.now() - self.starttime))
        except Exception as e:
            self.logger.exception("Fatal Error!")
            self.logger.info(e)
            exit(1)

if __name__ == "__main__":
    myObject = NetworkOverview()
    myObject.run()
