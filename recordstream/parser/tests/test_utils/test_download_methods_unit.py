import os
import shutil

import pendulum
from test_blob import Blob

from hedera.util.downloadMethods import GoogleDownloader

FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)

rcd_downloader = GoogleDownloader("rcd_test_metadata.json", "rcd")

test_blob_dict = {
    "name": "test/blob/name",
    "bucket": {"name": "test_bucket"},
    "size": "1000",
    "updated": "2022-03-16T00:00:48.750000Z",
    "content_type": "test_content",
}

blob = Blob(**test_blob_dict)


def test_switch_bucket_rcd():
    prefix = rcd_downloader.switch_bucket(["0.0.4", "0.0.5", "0.0.6"])

    assert prefix != "recordstreams/record/0.0.3/"


def test_checker_behind_rcd():
    prefix = rcd_downloader.checker(f"{FILE_DIR}/data/scan_path")

    assert prefix != "recordstreams/record/0.0.3"


def test_checker_up_to_date_rcd():
    now = pendulum.datetime(2022, 3, 2, 0, 0, 0)
    file_name = (
        "{:02d}".format(now.year)
        + "-"
        + "{:02d}".format(now.month)
        + "-"
        + "{:02d}".format(now.day)
        + "T"
        + "{:02d}".format(now.hour)
        + "_"
        + "{:02d}".format(now.minute)
        + "_"
        + "{:02d}".format(now.second)
        + ".063618034Z.rcd"
    )
    file = open(f"{FILE_DIR}/data/scan_path/{file_name}", "w")
    file.close()

    prefix = rcd_downloader.checker(f"{FILE_DIR}/data/scan_path/")

    assert prefix == "recordstreams/record0.0.3/"

    os.remove(f"{FILE_DIR}/data/scan_path/{file_name}")


def test_get_marker():
    marker = rcd_downloader.get_marker()
    now = pendulum.now("UTC")

    assert marker == "{:02d}".format(now.year) + "-" + "{:02d}".format(now.month) + "-" + "{:02d}".format(now.day)


def test_create_relevant_folders():
    if os.path.exists("tests/data/download_dir/"):
        shutil.rmtree("tests/data/download_dir/")

    download_directory = rcd_downloader.create_relevant_folders(
        "",
        "tests/data/download_dir",
        "recordstreams/record0.0.3/" "2022-03-10T18_19_04.143828000Z.rcd",
    )
    assert download_directory == f"/tests/data/download_dir/2022/03/10/2022-03-10T18_19_04.143828000Z.rcd"

    shutil.rmtree("tests/data/download_dir/")


def test_decompose_object():
    components = rcd_downloader.decompose_object("recordstreams/record0.0.3/2022-03-10T18_19_04.143828000Z.rcd")

    assert components["year"] == "2022"
    assert components["month"] == "03"
    assert components["day"] == "10"


def test_validate_metadata():
    (
        blob_name,
        rcd_filename,
        bucket_name,
        blob_size,
        upload_time,
        content_type,
    ) = rcd_downloader.validate_metadata(blob)

    assert blob_name == "test/blob/name"
    assert rcd_filename == "name"
    assert bucket_name == "test_bucket"
    assert blob_size == "1000"
    assert upload_time == "2022-03-16T00:00:48.750Z"
    assert content_type == "test_content"


def test_get_blob_metadata():
    rcd_metadata = rcd_downloader.get_blob_metadata(blob)

    assert rcd_metadata["uuid"] == "test/blob/name-2022-03-16T00:00:48.750Z"
