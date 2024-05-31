import datetime
import hashlib
import os

from hedera.errors import FileScanError


def scan_for_new_files(scan_path: str, type: str) -> list:
    """
    Scan directory for new rcd files to parse

    :param scan_path: Path to scan for new files
    :param type: type of file to scan for

    :returns: List of files to be parsed
    """
    # x = glob.glob("scan_path/*[!.(processing|processed)]")
    # don't think glob works because it's not just excluding the _processed/_processing files,
    # it has slightly more complex logic (e.g., find this pattern and if find this pattern plus
    # and there isn't the patter + _processed/_processing then append to the list
    # Tried using list comprehension + glob but was 2-3 times slower than the scan function

    if type == "pb":
        file_split = [-2]
    if type == "evts":
        file_split = [-1]
    if type == "rcd":
        file_split = [-1, -2]

    files = []

    for i in file_split:
        try:
            for r, _d, f in os.walk(scan_path):
                for file in f:
                    if (
                        (file.split(".")[i] == type)
                        and (file.split("_")[-1] != "processed")
                        and (file.split("_")[-1] != "processing")
                    ):
                        processed_file = os.path.join(r, file + "_processed")
                        processing_file = os.path.join(r, file + "_processing")
                        if (
                            not os.path.isfile(processed_file)
                            and not os.path.exists(processed_file)
                            and (not os.path.isfile(processing_file) and not os.path.exists(processing_file))
                        ):
                            files.append(os.path.join(r, file))
        except Exception as ex:
            raise FileScanError("Unexpected error in utilities.py scan_for_new_files method") from ex
    return files


def get_datetime_from_filename(filename: str, precision="seconds"):
    """
    Converts filename to datetime
    """
    try:
        date_time_str_parts = filename.split("_")
        date_time_str = date_time_str_parts[0] + "_" + date_time_str_parts[1] + "_" + date_time_str_parts[2][:2]
    except IndexError:
        date_time_str_parts = filename.split(":")
        date_time_str = date_time_str_parts[0] + ":" + date_time_str_parts[1] + ":" + date_time_str_parts[2][:2]
    if precision == "seconds":
        try:
            date_time_obj = datetime.datetime.strptime(date_time_str, "%Y-%m-%dT%H_%M_%S")
        except ValueError:
            date_time_obj = datetime.datetime.strptime(date_time_str, "%Y-%m-%dT%H:%M:%S")
    elif precision == "nanoseconds":
        filename = filename.replace("Z", "")
        date_time_str_parts = filename.split(".")
        if 1 in date_time_str_parts:
            nanoseconds = date_time_str_parts[1]
        else:
            nanoseconds = "000000"
        if len(nanoseconds) > 6:
            remove_digits = len(nanoseconds) - 6
            nanoseconds = nanoseconds[:-remove_digits]
        if len(nanoseconds) < 6:
            add_zeros = 6 - len(nanoseconds)
            i = 0
            while i < add_zeros:
                nanoseconds = nanoseconds + "0"
                i += 1
        date_time_str = date_time_str + "." + nanoseconds
        try:
            date_time_obj = datetime.datetime.strptime(date_time_str, "%Y-%m-%dT%H_%M_%S.%f")
        except ValueError:
            date_time_obj = datetime.datetime.strptime(date_time_str, "%Y-%m-%dT%H:%M:%S.%f")
    return date_time_obj


def scan_for_new_files_backfill(scan_path, type, last_file_datetime_from, last_file_datetime_to):
    """
    [DEPRECATED]
    Scan directory for new rcd files to parse

    :param scan_path: Path to scan for new files
    :param type: type of file to scan for
    :param last_file_datetime_from: scan start time
    :param last_file_datetime_to: scan end time

    :returns: List of files to be parsed
    """
    # x = glob.glob("scan_path/*[!.(processing|processed)]")
    # don't think glob works because it's not just excluding the _processed/_processing files,
    # it has slightly more complex logic (e.g., find this pattern and if find this pattern plus
    # and there isn't the patter + _processed/_processing then append to the list
    # Tried using list comprehension + glob but was 2-3 times slower than the scan function
    if type == "gz":
        file_split = -2
    else:
        file_split = -1
    try:
        files = []
        for r, _d, f in os.walk(scan_path):
            for file in f:
                if file.split(".")[file_split] == type:
                    current_file_datetime = get_datetime_from_filename(file)

                    if last_file_datetime_from <= current_file_datetime <= last_file_datetime_to:
                        files.append(os.path.join(r, file))

        return files
    except Exception as ex:
        raise FileScanError("Unexpected error in utilities.py scan_for_new_files_backfill method") from ex


def dict_list_keys(d: dict):
    """
    Get keys of a dictionary or length of a list
    """
    if type(d) == dict:
        return d.keys()
    elif type(d) == list:
        return range(len(d))
    else:
        return ()


def dict_bytes_to_hex(d: dict) -> dict:
    """
    Convert bytes in a dictionary to hex
    """
    for k in dict_list_keys(d):
        v = d[k]
        if type(v) in (bytes, bytearray):
            d[k] = v.hex()
        elif type(v) in (dict, list):
            dict_bytes_to_hex(v)
    return d


def parse_flat_fields(response: dict, flat_fields: list, header_name: str) -> dict:
    """
    Returns parsed flat aggregation fields

    :param response: nested dictionary
    :param flat_fields: fields to look for in nested dictionary
    :param header_name: fields for flat dictionary
    """
    result_dict = {}
    if len(flat_fields) == 0:
        raise ValueError("flat_fields empty, please provide flat_fields")
    for f in flat_fields:
        if f in response:
            if type(response[f]) == dict:
                for key in response[f]:
                    result_dict[f"{header_name}.{f}.{key}"] = response[f][key]
            elif type(response[f]) == list:
                ct = 1
                for i in response[f]:
                    if type(i) == dict:
                        for key in i:
                            result_dict[f"{header_name}.{f}.{key}.{ct}"] = i[key]
                    else:
                        result_dict[f"{header_name}.{f}.{ct}"] = i
                    ct += 1
            else:
                result_dict[f"{header_name}.{f}"] = response[f]
    return result_dict
