import logging
import os
import socket
import time

import pendulum
import requests
import urllib3

from hedera.config import settings
from hedera.errors import BucketSwitchError, DownloaderCheckerError
from hedera.util.downloadMethods import GoogleDownloader

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.GOOGLE_APP_CREDENTIALS


class RecordFileDownloader:
    def __init__(self, cli_options: dict):
        """
        Constructor - Do All the initializations here.
        """

        self.options = cli_options
        self.script_name = os.path.basename(__file__[:-3])
        self.logger = None
        self.__init_log__()
        self.__init_param__()

    def __init_log__(self):
        """
        Initialise the log file
        """
        logging.basicConfig(level=self.options["log_level"])
        self.logger = logging.getLogger(self.script_name)
        self.logger.info("Logger started ...")

    def __init_param__(self):
        """
        Initialise input parameters
        """

    def run(self) -> None:
        """
        Orchestration to download record files from Hedera google buckets
        """
        try:

            while True:

                i = 1
                while i < 10:
                    backoff = 2**i
                    try:
                        self.logger.debug("Starting google downloader")
                        downloader = GoogleDownloader(
                            settings.LOG_DIR + "/rcd-metadata.json",
                            settings.RECORDS_FILE_EXTENSION,
                        )
                        rcd_file_path = downloader.create_relevant_folders(
                            settings.RECORDS_FILES_PATH,
                            settings.PARSED_RECORD_STREAM_FILES_DIR,
                            blob_name=None,
                        )
                        prefix = downloader.checker(rcd_file_path)
                        now = pendulum.now("UTC")
                        date_time = now.format("%Y-%m-%d %H:%M:%S")
                        self.logger.debug(date_time + " - Get list of blobs " + prefix)
                        downloader.run(
                            settings.HEDERA_BUCKET_NAME,
                            settings.RECORDS_FILES_PATH,
                            settings.PARSED_RECORD_STREAM_FILES_DIR,
                            prefix,
                            "/",
                            self.options["backfill_marker"],
                            metadata=True,
                        )
                        # sleep before the next file check
                        time.sleep(settings.DOWNLOADER_LOOP_SLEEP)
                    except (requests.exceptions.ReadTimeout, urllib3.exceptions.ReadTimeoutError, socket.timeout) as ex:
                        self.logger.error(
                            f"Downloader timed out, retry #{i}\n" f"Sleeping for {backoff} seconds and then restarting"
                        )
                        i += 1
                        time.sleep(2 * backoff)
                        continue

        except DownloaderCheckerError as ex:
            self.logger.exception("Error when checking difference between current timestamp and last downloaded file")
        except BucketSwitchError as ex:
            self.logger.exception("Error when checking difference between current timestamp and last downloaded file")
        except Exception as ex:
            self.logger.exception("Unexpected error downloading files")
            time.sleep(5)
