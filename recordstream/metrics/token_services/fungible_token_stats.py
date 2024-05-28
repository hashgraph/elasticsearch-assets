import json
from optparse import OptionParser
import os
import logging
import logging.config
import datetime

from pydantic import BaseModel, Field
import pandas as pd


class accountNum(BaseModel):
    accountNum: int


class AccountID(BaseModel):
    accountID: accountNum
    amount: int | None = None


class Token(BaseModel):
    tokenNum: str


class Transfer(BaseModel):
    amount: int
    accountID: accountNum


class TokenTransferList(BaseModel):
    token: Token
    transfers: list[Transfer]


class Txn(BaseModel):
    status: str
    node_id: str = Field(alias="body.nodeAccountID.accountNum")
    transaction_hash: str = Field(alias="record.transactionHash")
    txn_type: str
    processed_timestamp:  datetime.datetime = Field(alias="@processed")
    consensusTimestamp: datetime.datetime
    contractNum: int = Field(None, alias="record.contractID.contractNum")   # contractNum is not present in all records
    token_transfer_list: list[TokenTransferList] | None = None
    transfer_list: list[AccountID] | None = None
    token_number: str | None = None


class HTS:
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
        print("Output format: %s", self.options.output_format)
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
            if record['status'] == '22' and ('TOKEN' in record['txn_type']):
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
                        # overwrite internal_token_number when token_number is present
                        flat_records['internal_token_number'] = token['token']['tokenNum']
                        # list sender/receiver
                        flat_records['sender'] = [transfer['accountID']['accountNum'] for transfer in token['transfers']  if transfer['amount'] < 0]
                        flat_records['receiver'] = [transfer['accountID']['accountNum'] for transfer in token['transfers'] if transfer['amount'] >= 0]
                        # token burn/mint/transfer amount
                        flat_records['send_amount'] = sum([transfer['amount'] for token in token_list for transfer in token['transfers'] if transfer['amount'] < 0])
                        flat_records['receive_amount'] = sum([transfer['amount'] for token in token_list for transfer in token['transfers'] if transfer['amount'] >= 0])

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
        # Count the number of transactions per minute per txn_type
        group_txn = records_df.groupby(['rounded_timestamp', 'txn_type']).agg(
            transaction_count=pd.NamedAgg(column="transaction_hash", aggfunc="count"),
            send_amount=pd.NamedAgg(column="send_amount", aggfunc="sum"),
            receive_amount=pd.NamedAgg(column="receive_amount", aggfunc="sum")
        ).reset_index()
        group_txn['tps'] = group_txn['transaction_count'] / 60
          
        return group_txn

    def aggregate_recordstreams_by_token(self, records_df):
        # Aggregate data by internal_token_number
        group_txn = records_df.groupby(['rounded_timestamp', 'internal_token_number']).agg(
            transaction_count=pd.NamedAgg(column="transaction_hash", aggfunc="count"),
            send_amount=pd.NamedAgg(column="send_amount", aggfunc="sum"),
            receive_amount=pd.NamedAgg(column="receive_amount", aggfunc="sum")
        ).reset_index()

        # caculate distinct payer, sender and receiver
        exploded_df = records_df.explode('payer').explode('sender').explode('receiver')
        group_user_df = exploded_df.groupby(['rounded_timestamp', 'internal_token_number']).agg(
            distinct_payers=pd.NamedAgg(column='payer', aggfunc=pd.Series.nunique),
            distinct_receivers=pd.NamedAgg(column='receiver', aggfunc=pd.Series.nunique),
            distinct_senders=pd.NamedAgg(column='sender', aggfunc=pd.Series.nunique)
        ).reset_index()

        # merge group_txn and group_user_df
        group_txn = pd.merge(group_txn, group_user_df, on=['rounded_timestamp', 'internal_token_number'], how='left')

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
            records = self.read_data(self.options.input_file)
            simplified_records = self.transform_data(records)
            records_df = self.rcdstreams_to_pd_df(simplified_records)
            # write synthetic data to a file
            output_filename = f"{self.options.output_folder}/{self.script_name}_synthetic_data"
            self.logger.info(f"Writing synthetic data to {output_filename} ...")
            self.write_df_to_file(output_filename, records_df)
            cleaned_records = self.clean_records_df(records_df)
            # Count unique number of account per minute
            aggregate_recordstreams_by_type = self.aggregate_recordstreams_by_type(cleaned_records)
            aggregate_recordstreams_by_token = self.aggregate_recordstreams_by_token(cleaned_records)
            # Write the aggregated output to a JSON file
            output_filename_type = f"{self.options.output_folder}/{self.script_name}_by_type"
            self.logger.info(f"Writing aggregated output to {output_filename_type} ...")
            self.write_df_to_file(output_filename_type, aggregate_recordstreams_by_type)
            output_filename_topics = f"{self.options.output_folder}/{self.script_name}_by_token"
            self.logger.info(f"Writing aggregated output to {output_filename_topics} ...")
            self.write_df_to_file(output_filename_topics, output_filename_type)
            self.logger.info("Run method completed ...")
        except Exception as e:
            self.logger.exception("Fatal Error!")
            self.logger.info(e)
            exit(1)

if __name__ == "__main__":
    myObject = HTS()
    myObject.run()
