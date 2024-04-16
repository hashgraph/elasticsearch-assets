import logging
import os
import pathlib
import random
import re
import socket
import time
from glob import glob

import jsonlines
import pendulum
import requests
import urllib3
from google.cloud import storage

from hedera.config import settings
from hedera.errors import (
    BlobMetadataValidationError,
    BucketSwitchError,
    CreateDownloadDirectoryError,
    DecomposeObjectError,
    DownloaderCheckerError,
    DownloadRunError,
    GetBlobMetadataError,
    GetMarkerError,
)


class GoogleDownloader:
    def __init__(self, json_file_name, downloader_type):
        """
        Constructor - Do All the initializations here.
        """
        self.logger = logging.getLogger(__name__)
    
        try:
            if not os.path.isfile(json_file_name):
                with jsonlines.open(json_file_name, mode="w") as jj:
                    jj.close()
        except Exception as ex:
            self.logger.error(f"Error creating {json_file_name}: {ex}")
            raise

        try:
            self.writer = jsonlines.open(json_file_name, mode="a", flush=True)
        except FileNotFoundError as ex:
            self.logger.error(f"Error creating {json_file_name}: {ex}")
            raise
        except Exception as ex:
            self.logger.error(f"Error opening {json_file_name}: {ex}")
            raise

        config = {
            "rcd": {
                "files_split": -1,
                "file_times_split": -3,
                "lag_threshold": 300,
                "default_bucket_prefix": settings.RECORDS_BUCKET_PREFIX,
                "random_bucket_prefix": "recordstreams/record",
            }
        }

        self.files_split = config[downloader_type]["files_split"]
        self.file_times_split = config[downloader_type]["file_times_split"]
        self.lag_threshold = config[downloader_type]["lag_threshold"]
        self.default_bucket_prefix = config[downloader_type]["default_bucket_prefix"]
        self.random_bucket_prefix = config[downloader_type]["random_bucket_prefix"]
        self.downloader_type = downloader_type

    def __del__(self):
        """
        Destructor
        """
        if hasattr(self, "writer"):
            try:
                self.writer.close()
            except Exception as ex:
                self.logger.error(f"Error closing {self.writer}: {ex}")

        logging.shutdown()

    def checker(self, file_path: str) -> str:
        """
        Check the time delta between the last downloaded file and now - if greater than
        5 minutes (for records and events) or 30 minutes (for accountbalances) assume there is a
        problem with the current node's google bucket and switch to another google bucket

        :param file_path: path to check timestamps of already downloaded files
        :param downloader_type: type of files the downloader looks for

        :returns prefix: (e.g., the node's google bucket) to download new rcd files from
        """
        try:
            files = [
                [os.path.join(r, file) for file in f if file.split(".")[self.files_split] == self.downloader_type]
                for r, d, f in os.walk(file_path)
            ]
            file_times = [
                pendulum.from_format(
                    re.sub(
                        "_",
                        ":",
                        f.split(".")[self.file_times_split].split("/")[-1],
                    ),
                    "YYYY-MM-DDTHH:mm:ss",
                )
                for f in files[0]
            ]

            if len(file_times) > 0:
                latest_file = max(t for t in file_times)
                lag = pendulum.now("UTC") - latest_file
                if lag.seconds > self.lag_threshold:
                    return self.switch_bucket(settings.ALT_NODES.split(","))
                else:
                    self.logger.debug("Downloader is up to date")
                    return self.default_bucket_prefix

            else:
                self.logger.debug(f"Starting to download files for {pendulum.now('UTC')}")
                return self.default_bucket_prefix
        except Exception as ex:
            raise DownloaderCheckerError("Unexpected error checking for recently downloaded files") from ex

    def switch_bucket(self, alt_node_list: list) -> str:
        """
        Switch to a random node's google bucket

        :param alt_node_list: list of alternative google buckets to download files from

        :returns prefix: (e.g., the node's google bucket) to download new files from
        """
        try:
            alt_node_account_id = random.choice(alt_node_list)
            self.logger.warning(f"Downloader is behind, switching to node {alt_node_account_id}'s google bucket")
            return f"{self.random_bucket_prefix}{alt_node_account_id}/"
        except Exception as ex:
            raise BucketSwitchError("Unexpected error switching buckets") from ex

    def get_marker(self) -> str:
        try:
            return (
                f"{'{:02d}'.format(pendulum.now('UTC').year)}-"
                f"{'{:02d}'.format(pendulum.now('UTC').month)}-"
                f"{'{:02d}'.format(pendulum.now('UTC').day)}"
            )

        except Exception as ex:
            raise GetMarkerError("Unexpected error getting marker") from ex

    def create_relevant_folders(
        self,
        local_path: str,
        download_to_directory: str,
        blob_name: str = None,
    ) -> str:
        """
        Create folders to place downloaded files

        :param local_path: path to top level of recordstreams dir
        :param download_to_directory: path to lowest level recordstreams dir (day)
        :param blob_name: path to files in google bucket

        :returns Location to download files
        """
        try:
            if blob_name is not None:
                components = self.decompose_object(blob_name)
            else:
                components = {
                    "year": "{:02d}".format(pendulum.now("UTC").year),
                    "month": "{:02d}".format(pendulum.now("UTC").month),
                    "day": "{:02d}".format(pendulum.now("UTC").day),
                }

            pathlib.Path(
                f"{local_path}"
                f"{download_to_directory}{os.path.sep}"
                f"{components['year']}{os.path.sep}"
                f"{components['month']}{os.path.sep}"
                f"{components['day']}"
            ).mkdir(parents=True, exist_ok=True)

            if blob_name is not None:
                return os.path.sep.join(
                    [
                        local_path,
                        download_to_directory,
                        components["year"],
                        components["month"],
                        components["day"],
                        components["fileName"],
                    ]
                )

            else:
                return os.path.sep.join(
                    [
                        local_path,
                        download_to_directory,
                        components["year"],
                        components["month"],
                        components["day"],
                    ]
                )

        except Exception as ex:
            raise CreateDownloadDirectoryError("Unexpected error creating downloade directory") from ex

    def decompose_object(self, blob_name: str) -> dict:
        """
        Break down blob name to create subfolders to download the files to

        :param blob_name: path to files in google bucket

        :returns Components to create subfolder in dictionary format
        """
        try:
            path_c = blob_name.split("/")
            components = dict()
            components["fileName"] = path_c[2]
            date_time_str = path_c[2].split(".")[0]
            try:
                if (
                    date_time_str[-1] == "Z"
                ):  # in some cases, it has no milliseconds and the Z is right after the minutes
                    d = pendulum.from_format(date_time_str, "YYYY-MM-DDTHH_mm_ssZ")
                else:
                    d = pendulum.from_format(date_time_str, "YYYY-MM-DDTHH_mm_ss")
            except ValueError:
                if (
                    date_time_str[-1] == "Z"
                ):  # in some cases, it has no milliseconds and the Z is right after the minutes
                    d = pendulum.from_format(date_time_str, "YYYY-MM-DDTHH_mm_ssZ")
                else:
                    d = pendulum.from_format(date_time_str, "YYYY-MM-DDTHH_mm_ss")

            components["year"] = "{:02d}".format(d.year)
            components["month"] = "{:02d}".format(d.month)
            components["day"] = "{:02d}".format(d.day)

            return components
        except Exception as ex:
            raise DecomposeObjectError("Unexpected decomposing objects") from ex

    def get_blob_metadata(self, blob) -> dict:
        """
        Create dictionary of blob metadata

        :param blob: rcd blob

        :returns Dictionary of rcd metadata
        """
        try:
            (
                blob_name,
                rcd_filename,
                bucket_name,
                blob_size,
                upload_time,
                content_type,
            ) = self.validate_metadata(blob)

            if str(upload_time)[22:] == ":Z":
                pass
            else:
                rcd_metadata = {
                    "uuid": f"{blob_name}-{upload_time}",
                    "txn_timestamp": upload_time,
                    "blob_name": blob_name,
                    "rcd_filename": rcd_filename,
                    "bucket_name": bucket_name,
                    "blob_size": blob_size,
                    "upload_time": upload_time,
                    "content_type": content_type,
                }

            return rcd_metadata
        except Exception as ex:
            raise GetBlobMetadataError("Unexpected error getting blob metadata") from ex

    def validate_metadata(self, blob):
        """
        Validate metadata for rcd blob - custom validation as pydantic doesn't seem simple with google blobs. Seems like
        the blobs are not a very compatible type and I got errors trying to convert it while testing

        :param blob: metadata for downloaded rcd files

        :returns validated rcd metadata fields to send to elasticsearch
        """
        try:
            if hasattr(blob, "name"):
                blob_name = "{}".format(blob.name)
                rcd_filename = blob_name.split("/")[2]
            else:
                blob_name = None
                rcd_filename = None

            if hasattr(blob, "bucket"):
                if hasattr(blob.bucket, "name"):
                    bucket_name = "{}".format(blob.bucket.name)
                else:
                    bucket_name = None
            else:
                bucket_name = None

            if hasattr(blob, "size"):
                blob_size = "{}".format(blob.size)
            else:
                blob_size = None

            if hasattr(blob, "updated"):
                upload_time = "{}".format(blob.updated)
                upload_time_short = upload_time[:23]
                upload_time_t = re.sub(" ", "T", upload_time_short)
                upload_time = upload_time_t + "Z"
            else:
                upload_time = pendulum.now("UTC").format("YYYY-MM-DDTHH:mm:ss.SSS")

            if hasattr(blob, "content_type"):
                content_type = "{}".format(blob.content_type)
            else:
                content_type = None

            return (
                blob_name,
                rcd_filename,
                bucket_name,
                blob_size,
                upload_time,
                content_type,
            )
        except Exception as ex:
            raise BlobMetadataValidationError("Unexpected error validating blob metadata") from ex

    def run(
        self,
        bucket_name: str,
        local_path: str,
        download_to_directory: str,
        prefix: str,
        delimiter=None,
        marker=None,
        metadata=False,
        file_time=None,
    ):
        """
        This method is an entry point of the main execution logic of the script.
        Includes logic and calls all the methods needed
        Get list of blobs in the google bucket and downloads to directory where blobs are picked up parser
        Note: Client.list_blobs requires at least package version 1.17.0.

        :param bucket_name: Bucket to scan for blobs
        :param local_path: Path to home directory
        :param download_to_directory: Location to download blobs to
        :param prefix: Determines which node's google bucket to scan
        :param delimiter: Delimiter for the bucket, default is "/"
        :param marker: Marker to scan specific date for blobs, default is current date
        :param metadata: Collect metadata or not, default is to not collect metadata
        :param file_time: File time in blob name (used to limit amount of files downloaded)
        """
        try:
            enforce_redownload = True
            if marker is None:
                marker = self.get_marker()
                enforce_redownload = False
            loop_scan_enabled = True
            while loop_scan_enabled:
                storage_client = storage.Client()

                self.logger.debug(
                    "Connecting to bucket {} with prefix {} and delimeter {}".format(bucket_name, prefix, delimiter)
                )
                blobs = storage_client.list_blobs(bucket_name, prefix=prefix + marker, delimiter=delimiter)

                i = 0
                already_downloaded_files = 0
                for blob in blobs:
                    if "sig" not in blob.name:
                        self.logger.debug(str(i) + ". - " + blob.name)
                        download_file_location = self.create_relevant_folders(
                            local_path, download_to_directory, blob.name
                        )

                        if os.path.isfile(download_file_location) and enforce_redownload is False:
                            already_downloaded_files += 1
                        else:
                            temp_download_file_location = download_file_location.replace(self.downloader_type, "tmpdld")
                            if metadata is True:
                                rcd_metadata = self.get_blob_metadata(blob)
                                self.writer.write(rcd_metadata)
                            if file_time is not None:
                                if file_time in blob.name:
                                    self.download_file(blob, temp_download_file_location, download_file_location)
                            else:
                                self.download_file(blob, temp_download_file_location, download_file_location)
                    i += 1
                self.logger.debug("Processed a list of {} blobs".format(blobs.num_results))
                if i == 0:  # Switch buckets if there were no files downloaded
                    prefix = self.switch_bucket(settings.ALT_NODES.split(","))

                if blobs.num_results == already_downloaded_files:  # we can move to the next day
                    self.logger.debug("Every processed file has been already downloaded, move marker to today")
                    loop_scan_enabled = True
                    marker = (
                        f"{'{:02d}'.format(pendulum.now('UTC').year)}-"
                        f"{'{:02d}'.format(pendulum.now('UTC').month)}-"
                        f"{'{:02d}'.format(pendulum.now('UTC').day)}"
                    )
                else:  # The loop can be exited
                    self.logger.debug("Ending GoogleDownloader.run() loop")
                    loop_scan_enabled = False
        except (
            GetMarkerError,
            CreateDownloadDirectoryError,
            DecomposeObjectError,
            GetBlobMetadataError,
            BlobMetadataValidationError,
        ) as ex:
            self.logger.exception(
                f"Unexpected error downloading files from node {prefix}'s bucket.\n "
                f"Skipping file and moving to next one:\n {ex}"
            )
        except (
            requests.exceptions.ReadTimeout,
            urllib3.exceptions.ReadTimeoutError,
            socket.timeout,
        ):
            raise
        except Exception as ex:
            raise DownloadRunError("Unexpected error in download files loop") from ex

    def download_file(self, blob, temp_download_file_location, download_file_location):
        self.logger.debug("Downloading file {} ".format(blob.name))
        blob.download_to_filename(temp_download_file_location)
        os.rename(
            temp_download_file_location,
            download_file_location,
        )
