class FileScanError(Exception):
    """Base class for exceptions when scanning for rcd files"""

    pass


class ParserLoopError(Exception):
    """Base class for exceptions when looping through rcd files"""

    pass


class RecordFormatVersionError(Exception):
    """Base class for exceptions when checking record format"""

    pass


class CreateTransactionItemError(Exception):
    """Base class for exceptions when creating transaction record"""

    pass


class CreateTransactionRecordError(Exception):
    """Base class for exceptions when creating transaction record"""

    pass


class ParseTxnError(Exception):
    """Base class for exceptions when parsing transaction"""

    pass


class ParseTxnItemError(Exception):
    """Base class for exceptions when parsing transaction item"""

    pass


class ParseTxnRecordError(Exception):
    """Base class for exceptions when parsing transaction record"""

    pass


class ReclassifyTokenTxnError(Exception):
    """Base class for exceptions when reclassifying token transactions"""

    pass


class AddTxnMetadataError(Exception):
    """Base class for exceptions when parsing transaction metadata"""

    pass


class CreateTimestampError(Exception):
    """Base class for exceptions when parsing transaction timestamps"""

    pass


class DownloaderCheckerError(Exception):
    """Base class for exceptions when checking the lag between the current timestamp and last downloaded file"""

    pass


class BucketSwitchError(Exception):
    """Base class for exceptions when attempting to switch google buckets"""

    pass


class GetMarkerError(Exception):
    """Base class for exceptions when attempting to create marker for google bucket download"""

    pass


class CreateDownloadDirectoryError(Exception):
    """Base class for exceptions when attempting to create download directory"""

    pass


class DecomposeObjectError(Exception):
    """Base class for exceptions when attempting to break down location of google bucket"""

    pass


class GetBlobMetadataError(Exception):
    """Base class for exceptions when attempting to get blob metadata"""

    pass


class BlobMetadataValidationError(Exception):
    """Base class for exceptions when attempting to validate blob metadata"""

    pass


class DownloadRunError(Exception):
    """Base class for exceptions for the download run method"""

    pass


class BalanceToDictError(Exception):
    """Base class for exceptions when converting the account balance object to a dictionary"""

    pass


class FlattenError(Exception):
    """Base class for exceptions when flattening the account balance"""

    pass


class FlattenBalanceError(Exception):
    """Base class for exceptions when flattening the account balance"""

    pass


class ParseBalanceError(Exception):
    """Base class for exceptions when parsing the account balance"""

    pass


class ValidateBalanceError(Exception):
    """Base class for exceptions when converting the validating account balance"""

    pass


class ReadTimeoutError(Exception):
    """Base class for exceptions when converting the validating account balance"""

    pass


class ValidateEventError(Exception):
    """Base class for exceptions when converting the validating account balance"""

    pass


class ParseEventError(Exception):
    """Base class for exceptions when converting the validating account balance"""

    pass


class EventFormatVersionError(Exception):
    """Base class for exceptions when converting the validating account balance"""

    pass


class EventObjectVersionError(Exception):
    """Base class for exceptions when converting the validating account balance"""

    pass


class ParseSignKeysError(Exception):
    """Base class for exceptions when parsing transaction sign keys"""

    pass


class ApiTokenError(Exception):
    pass


class ApiQueryError(Exception):
    pass


class ApiPatchError(Exception):
    pass


class PingerRestartError(Exception):
    pass
