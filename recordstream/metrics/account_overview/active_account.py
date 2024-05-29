import json
from optparse import OptionParser
import os
import logging
import logging.config
import datetime

from pydantic import BaseModel, Field
import pandas as pd


class AccountNum(BaseModel):
    accountNum: int


class Account(BaseModel):
    accountID: AccountNum
    amount: float


class Txn(BaseModel):
    status: str
    transaction_hash: str = Field(alias="record.transactionHash")
    txn_type: str
    txn_sign_keys: list[str] | None = None
    processed_timestamp:  datetime.datetime = Field(alias="@processed")
    consensusTimestamp: datetime.datetime
    payer: str = Field(alias="record.accountID.accountNum")
    transfer_list: list[Account] | None = None

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
            "-f", "--output_format",
            default='json',
            action='store',
            type=str,
            dest='output_format',
            help='Output format [json|csv]')
        
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
        simplified_records = []
        for record in records:
            if record['transfer_list'] is None:
                simplified_records.append({
                    'consensusTimestamp': record['consensusTimestamp'],
                    'accountNum': record["payer"]
                })
            for transfer in record['transfer_list']:
                simplified_records.append({
                    'consensusTimestamp': record['consensusTimestamp'],
                    'key_type': record["txn_sign_keys"]
                })
        return simplified_records

    def transform_data_payer_ec_key(self, records):
        # Extract only timestamp and unnested accountNum from the transfer_list column
        simplified_records = []
        for record in records:
            if record['transfer_list'] is None:
                simplified_records.append({
                    'consensusTimestamp': record['consensusTimestamp'],
                    'accountNum': record["payer"],
                    'key_type': record["txn_sign_keys"]
                })
            for transfer in record['transfer_list']:
                if transfer['accountID']['accountNum'] < 0:
                    simplified_records.append({
                        'consensusTimestamp': record['consensusTimestamp'],
                        'key_type': record["txn_sign_keys"],
                        'accountNum': transfer['accountID']['accountNum']
                    })
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

    def aggregate_recordstreams(self, records_df):
        # Aggregate record streams DataFrame
        # Count distinct accountNums per minute
        active_account = records_df.groupby(['rounded_timestamp'])['accountNum'].nunique().reset_index()
        return active_account
    
    def unique_account(self, records_df):
        # extract unique accountNums
        unique_account = records_df['accountNum'].unique()
        return unique_account
    
    def aggregated_recordstreams_payer_ec_key(self, records_df):
        # Aggregate record streams DataFrame
        # Count distinct accountNums per minute
        active_account = records_df.groupby(['key_type']).agg(
            transaction_count=pd.NamedAgg(column="transaction_hash", aggfunc="count"),
            account_count=pd.NamedAgg(column="accountNum", aggfunc="nunique")
        ).reset_index()
        return active_account

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
            records = self.read_data(self.options.input_file)
            simplified_records = self.transform_data(records)
            records_df = self.rcdstreams_to_pd_df(simplified_records)
            cleaned_records = self.clean_records_df(records_df)
            # Count unique number of account per minute
            aggregated_records = self.aggregate_recordstreams(cleaned_records)
            output_filename = f"{self.options.output_folder}/{self.script_name}_active_account"
            self.logger.info(f"Writing aggregated output to {output_filename} ...")
            self.write_df_to_file(output_filename, aggregated_records)
            # Aggegate EC account
            simplified_records_payer_ec_key = self.transform_data_payer_ec_key(records)
            records_df_payer_ec_key = self.rcdstreams_to_pd_df(simplified_records_payer_ec_key)
            cleaned_records_payer_ec_key = self.clean_records_df(records_df_payer_ec_key)
            aggregated_records_payer_ec_key = self.aggregated_recordstreams_payer_ec_key(cleaned_records_payer_ec_key)
            output_filename = f"{self.options.output_folder}/{self.script_name}_ec_account"
            self.logger.info(f"Writing aggregated output to {output_filename} ...")
            self.write_df_to_file(output_filename, aggregated_records_payer_ec_key)
            # Get list of unique accountNums in the records
            unique_account = self.unique_account(cleaned_records)
            output_filename = f"{self.options.output_folder}/unique_active_accounts.json"
            self.logger.info(f"Writing unique accountNums to {output_filename} ...")
            with open(output_filename, 'w') as f:
                json.dump(unique_account.tolist(), f)   
            self.logger.info("Total runtime: %s" % str(datetime.datetime.now() - self.starttime))
        except Exception as e:
            self.logger.exception("Fatal Error!")
            self.logger.info(e)
            exit(1)

if __name__ == "__main__":
    myObject = NetworkOverview()
    myObject.run()
