import csv
import json
import os
import logging
import datetime
from optparse import OptionParser

import pandas as pd

from abc import ABC, abstractmethod


class BaseScript(ABC):
    """
    BaseScript is an abstract base class that provides common functionality for scripts.
    """

    @abstractmethod
    def __init__(self, log_filename):
        """
        Initializes the BaseScript object.

        Args:
            log_filename (str): The name of the log file.
        """
        self.starttime = datetime.datetime.now()
        self.log_filename = log_filename

        self.__init_params__()
        self.logger = self.init_log()
        self.__init_env_var__()

    def __init_env_var__(self):
        """
        Initializes the environment variable.

        Raises:
            Exception: If the environment variable PATH is not set.
        """
        self.path = os.getenv("PATH")
        if self.path is None:
            raise Exception("Environment variable PATH is not set")
        else:
            self.logger.info("Environment variable PATH=%s", self.path)

    def __init_params__(self):
        """
        Initializes the script parameters.
        """
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

        self.options, self.__args = parser.parse_args()

        print("Input file: %s", self.options.input_file if self.options.input_file else "None")
        print("Output folder: %s", self.options.output_folder if self.options.output_folder else "None")
        print("Output format: %s", self.options.output_format if self.options.output_format else "None")
        print("Log level: %s", self.options.log_level)

    def init_log(self):
        """
        Initializes the log file.

        Returns:
            logging.Logger: The logger object.
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

        logging.basicConfig(filename=os.path.join(self.options.output_folder + '/' + self.log_filename + '.log'),
                            level=level,
                            format='%(asctime)s.%(msecs)03d %(levelname)5s: %(name)s %(message)s')
        logger = logging.getLogger(self.log_filename)
        logger.info("Logger started ...")
        return logger

    def read_data(self, file_path, Txn) -> list[dict]:
        """
        Reads data from a file and returns a list of dictionaries.

        Args:
            file_path (str): The path to the input file.
            Txn (Type): The type of transaction object.

        Returns:
            list[dict]: A list of dictionaries representing the transactions.

        Raises:
            FileNotFoundError: If the file is not found.
            json.JSONDecodeError: If there is an error decoding JSON from the file.
            csv.Error: If there is an error reading the CSV file.
            Exception: If there is an error reading the file.
        """
        try:
            txns = []
            if file_path.endswith('.json'):
                with open(file_path, 'r') as file:
                    for line in file:
                        data = json.loads(line)
                        txn = Txn(**data)
                        txns.append(txn.dict())
            elif file_path.endswith('.csv'):
                with open(file_path, 'r') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        txn = Txn(**row)
                        txns.append(txn.dict())
            else:
                self.logger.error("Invalid input file format")
                return None
            return txns
        except FileNotFoundError:
            self.logger.error(f"File not found: {file_path}")
            return None
        except json.JSONDecodeError:
            self.logger.error(f"Error decoding JSON from file: {file_path}")
            return None
        except csv.Error:
            self.logger.error(f"Error reading CSV file: {file_path}")
            return None
        except Exception as e:
            self.logger.error(f"An error occurred while reading the file: {e}")
            return None

    def write_df_to_file(self, output_filename, output_df):
        """
        Writes a DataFrame to a file.

        Args:
            output_filename (str): The name of the output file.
            output_df (pandas.DataFrame): The DataFrame to write.

        Raises:
            Exception: If the output format is invalid.
        """
        output_filename = f"{output_filename}_{self.starttime.strftime('%Y%m%d%H%M%S')}.{self.options.output_format}"
        if self.options.output_format == 'json':    
            # Write output to JSON file
            output_df.to_json(output_filename, orient='records', lines=True)
        elif self.options.output_format == 'csv':
            # Write output to CSV file
            output_df.to_csv(output_filename, index=False)
        else:
            raise Exception("Invalid output format")
    
    def rcdstreams_to_pd_df(self, records):
        """
        Converts records to a Pandas DataFrame.

        Args:
            records (list[dict]): A list of dictionaries representing the records.

        Returns:
            pandas.DataFrame: The DataFrame containing the records.
        """
        records_df = pd.DataFrame(records)
        return records_df