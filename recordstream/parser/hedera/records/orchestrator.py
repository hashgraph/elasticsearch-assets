import logging
import os
import pathlib
import time

import jsonlines
import pendulum
import ray

from hedera.config import settings
from hedera.errors import FileScanError, ParserLoopError
from hedera.records.record_file_parser import (
    RcdParser,
    parse_transaction_v5,
    parse_transaction_v6,
)
from hedera.util.utilities import scan_for_new_files


class RecordFileOrchestrator:
    def __init__(self, cli_options: dict):
        """
        Constructor - Do All the initializations here.
        """

        self.options = cli_options
        self.script_name = os.path.basename(__file__[:-3])
        self.logger = None
        self.__init_log__()
        self.parser = RcdParser()
        self.ray_chunk_size = 500
        self.txn_list_size = 5000
        try:
            self.writer = jsonlines.open(
                settings.PARSER_OUTPUT_DIR + "/recordstreams" + ".json",
                mode="a",
                flush=True,
            )
        except FileNotFoundError as ex:
            self.logger.exception(f"Error creating {settings.LOG_DIR + '/recordstreams' + '.json'}: {ex}")
            raise
        except Exception as ex:
            self.logger.exception(f"Error opening {settings.LOG_DIR + '/recordstreams' + '.json'}: {ex}")
            raise
        
        ray.init(_temp_dir=settings.RAY_TMP_DIR)

    def __init_log__(self):
        """
        Initialise the log file
        """
        logging.basicConfig(level=self.options["log_level"])
        self.logger = logging.getLogger(self.script_name)
        self.logger.info("Logger started ...")

    def parse_txns(self, files_to_parse: list, rcd_dir: str) -> None:
        """
        Logic to parse transactions

        :param files_to_parse: List of record files to be
        :param rcd_dir: Location of rcd files
        """
        v5_txns = []
        v6_txns = []
        v5_chunked_list = []
        v6_chunked_list = []

        for f in files_to_parse[:]:
            start = time.time()
            self.logger.debug(f)
            pathlib.Path(f"{f}_processed").touch()
            txns, version = self.parser.load_txns(f, rcd_dir)
            if version == "v5":
                v5_txns.extend(txns)
                if len(v5_txns) > self.txn_list_size or f == files_to_parse[-1]:
                    self.write_to_file(self.ray_v5_parser(v5_txns, v5_chunked_list, self.ray_chunk_size))
                    v5_txns = []
                    v5_chunked_list = []
            if version == "v6":
                v6_txns.extend(txns)
                if len(v6_txns) > self.txn_list_size or f == files_to_parse[-1]:
                    self.write_to_file(self.ray_v6_parser(v6_txns, v6_chunked_list, self.ray_chunk_size))
                    v6_txns = []
                    v6_chunked_list = []
            files_to_parse.remove(f)

            end = time.time()
            self.logger.debug(f"Parsed {f} in {end-start} seconds.")

    def ray_v5_parser(self, v5_txns: list, v5_chunked_list: list, chunk_size: int) -> list:
        """
        Uses ray remote to parse v5 transactions

        :param v6_txns: List of v5 transactions to be processes
        :param v6_chunked_list: List of list of v5 transactions to be processed in parallel
        :param chunk_size: Num of transactions in the sub lists

        :return parsed_txns: Processed transactions
        """
        parsed_txns = []
        for i in range(0, len(v5_txns), chunk_size):
            v5_chunked_list.append(v5_txns[i : i + chunk_size])

        parsed_txns.extend(
            ray.get(
                [
                    parse_transaction_v5.remote(
                        chunk,
                        pendulum.now("UTC").isoformat("T")[:26] + "Z",
                        self.logger,
                    )
                    for chunk in v5_chunked_list
                ]
            )
        )

        return parsed_txns

    def ray_v6_parser(self, v6_txns: list, v6_chunked_list: list[list], chunk_size: int) -> list:
        """
        Uses ray remote to parse v6 transactions

        :param v6_txns: List of v6 transactions to be processes
        :param v6_chunked_list: List of list of v6 transactions to be processed in parallel
        :param chunk_size: Num of transactions in the sub lists

        :return parsed_txns: Processed transactions
        """
        parsed_txns = []
        for i in range(0, len(v6_txns), chunk_size):
            v6_chunked_list.append(v6_txns[i : i + chunk_size])

        parsed_txns.extend(
            ray.get(
                [
                    parse_transaction_v6.remote(
                        chunk,
                        pendulum.now("UTC").isoformat("T")[:26] + "Z",
                        self.logger,
                    )
                    for chunk in v6_chunked_list
                ]
            )
        )

        return parsed_txns

    def write_to_file(self, parsed_txns: list) -> None:
        """
        Write list of transactions to file

        :param parsed_txns: List of processed transactions
        """
        for txn_list in parsed_txns:
            for txn in txn_list:
                self.writer.write(txn)

    def run(self):
        """
        Orchestration to parse downloaded record files
        """
        try:
            while True:

                if self.options["backfill_marker"] is None:
                    year = "{:02d}".format(pendulum.now("UTC").year)
                    month = "{:02d}".format(pendulum.now("UTC").month)
                    day = "{:02d}".format(pendulum.now("UTC").day)
                else:
                    year = self.options["backfill_marker"].split("-")[0]
                    month = self.options["backfill_marker"].split("-")[1]
                    day = self.options["backfill_marker"].split("-")[2]

                try:
                    files_to_parse = scan_for_new_files(
                        f"{settings.PARSED_RECORD_STREAM_FILES_PATH}{year}/{month}/{day}/",
                        "rcd",
                    )
                    files_to_parse.sort()
                    files_parsed = len(files_to_parse)

                    batch_start = time.time()

                    self.parse_txns(files_to_parse, f"{settings.PARSED_RECORD_STREAM_FILES_PATH}{year}/{month}/{day}/")

                    batch_end = time.time()
                    self.logger.info(f"Batch processed in {batch_end-batch_start} seconds.")

                    self.logger.info(
                        f"{pendulum.now('UTC').format('YYYY-MM-DDTHH:mm:ss')} "
                        f"Number of files parsed:  {(files_parsed)}"
                    )

                    time.sleep(settings.ORCHESTRATOR_LOOP_SLEEP)
                except FileScanError as ex:
                    raise FileScanError("Error scanning through files") from ex
                except Exception as ex:
                    raise ParserLoopError("Failed to parse files") from ex

        except FileScanError as ex:
            self.logger.exception(f"Error scanning through files: \n{ex}")
        except Exception as ex:
            self.logger.exception(f"Unexpected error with rcd parser:\n{ex}")
