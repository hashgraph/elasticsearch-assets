import json
from optparse import OptionParser
import os
import logging
import logging.config
import datetime
from typing import Optional

from pydantic import BaseModel, Field
import pandas as pd


class accountNum(BaseModel):
    accountNum: int


class AccountID(BaseModel):
    accountID: accountNum
    amount: int | None = None


class Transfer(BaseModel):
    amount: int
    accountID: accountNum


class ContractID(BaseModel):
    contractNum: Optional[str] = "0"


class LogInfo(BaseModel):
    contractID: Optional[ContractID]
    bloom: Optional[bytes] = b""
    topic: list[Optional[bytes]]
    data: Optional[bytes] = b""


class ContractCreateResult(BaseModel):
    contractID: Optional[ContractID]
    contractCallResult: Optional[bytes] = b""
    bloom: Optional[bytes] = b""
    gasUsed: Optional[int] = 0
    logInfo: Optional[list[LogInfo]]
    createdContractIDs: Optional[list[dict]]


class ContractCallResult(BaseModel):
    contractID: Optional[ContractID]
    bloom: Optional[bytes] = b""
    gasUsed: Optional[int] = 0
    logInfo: Optional[list[LogInfo]]
    createdContractIDs: Optional[list[dict]]

class Txn(BaseModel):
    status: str
    node_id: str = Field(alias="body.nodeAccountID.accountNum")
    transaction_hash: str = Field(alias="record.transactionHash")
    txn_type: str
    processed_timestamp:  datetime.datetime = Field(alias="@processed")
    consensusTimestamp: datetime.datetime
    contractNum: str = Field(None, alias="record.contractID.contractNum")
    gasUsed: int = Field(None, alias="record.gasUsed")
    contract_create_result: list[ContractCreateResult] | None = None
    contract_call_result: list[ContractCallResult] | None = None
    transfer_list: list[AccountID] | None = None


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
                    base_flat_record['internal_contract_number'] = [
                        record['contractID']['contractNum']
                        for record in record['contract_call_result']['logInfo']
                    ]
                    base_flat_record['created_contract_id'] = record['contract_call_result']['createdContractIDs']
                
                simplified_records.append(base_flat_record)
        return simplified_records

    def rcdstreams_to_pd_df(self, records):
        # Convert records to Pandas DataFrame
        records_df = pd.DataFrame(records)
        return records_df

    def clean_records_df(self, records_df):
        # Clean records DataFrame
        records_df.drop_duplicates(inplace=True, ignore_index=True, subset=['transaction_hash', 'contract_number'])
        # add rounded timestamp to a minute
        records_df['rounded_timestamp'] = records_df['consensusTimestamp'].dt.floor('min')
        # add high level transaction type based on txn_type

        return records_df

    def aggregate_recordstreams_by_type(self, records_df):
        # Aggregate record streams DataFrame
        # Count the number of transactions per minute per txn_type
        group_txn = records_df.groupby(['contract_number', 'txn_type']).agg(
            transaction_count=pd.NamedAgg(column="transaction_hash", aggfunc="count"),
            gas_used_total=pd.NamedAgg(column="gasUsed", aggfunc="sum"),
            gas_used_max=pd.NamedAgg(column="gasUsed", aggfunc="max"),
            gas_used_min=pd.NamedAgg(column="gasUsed", aggfunc="min"),
        ).reset_index()
          
        return group_txn

    def aggregate_recordstreams_by_contract(self, records_df):
        # Aggregate data by internal_token_number
        group_txn = records_df.groupby(['contract_number']).agg(
            transaction_count=pd.NamedAgg(column="transaction_hash", aggfunc="count"),
            gas_used_total=pd.NamedAgg(column="gasUsed", aggfunc="sum"),
            gas_used_max=pd.NamedAgg(column="gasUsed", aggfunc="max"),
            gas_used_min=pd.NamedAgg(column="gasUsed", aggfunc="min"),
        ).reset_index()

        return group_txn
    
    def aggregate_recordstreams_by_account_contract(self, records_df):
        # Explode the payer column
        records_df = records_df.explode('payer')
        # Aggregate data by internal_token_number
        group_txn = records_df.groupby(['contract_number', 'payer']).agg(
            transaction_count=pd.NamedAgg(column="transaction_hash", aggfunc="count"),
            gas_used_total=pd.NamedAgg(column="gasUsed", aggfunc="sum")
        ).reset_index()

        return group_txn
    
    def aggregate_recordstreams_by_account(self, records_df):
        # Explode the payer column
        records_df = records_df.explode('payer')
        # Aggregate data by internal_token_number
        group_txn = records_df.groupby(['payer', 'txn_type']).agg(
            transaction_count=pd.NamedAgg(column="transaction_hash", aggfunc="count"),
            gas_used_total=pd.NamedAgg(column="gasUsed", aggfunc="sum")
        ).reset_index()

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
    myObject = HTS()
    myObject.run()
