from hedera.util.utilities import scan_for_new_files


def test_scan_for_new_files():
    files = scan_for_new_files("tests/test_utils/data/scan_path/", "rcd")

    assert len(files) == 13
