import gzip
import logging
import os
import pathlib
import shutil
from typing import Union

import pendulum
import ray
from pydantic.error_wrappers import ValidationError

from hedera.config import settings
from hedera.errors import (
    AddTxnMetadataError,
    CreateTimestampError,
    CreateTransactionItemError,
    CreateTransactionRecordError,
    ParseSignKeysError,
    ParseTxnError,
    ParseTxnItemError,
    ParseTxnRecordError,
    ReclassifyTokenTxnError,
    RecordFormatVersionError,
)
from hedera.models.tx_item import TransactionItem, UnknownType
from hedera.models.tx_record import TransactionRecord
from hedera.records.parse_tx_item import (
    parseCommon,
    parseConsensusCreateTopic,
    parseConsensusDeleteTopic,
    parseConsensusSubmitMessage,
    parseConsensusUpdateTopic,
    parseContractCall,
    parseContractCreateInstance,
    parseContractDelete,
    parseContractUpdateInstance,
    parseCryptoApproveAllowance,
    parseCryptoCreateAccount,
    parseCryptoDelete,
    parseCryptoDeleteAllowance,
    parseCryptoTransfer,
    parseCryptoUpdateAccount,
    parseEthereumTransaction,
    parseFileAppend,
    parseFileCreate,
    parseFileDelete,
    parseFileUpdate,
    parseNodeStakeUpdate,
    parseScheduleCreate,
    parseScheduleDelete,
    parseScheduleSign,
    parseTokenAssociate,
    parseTokenBurn,
    parseTokenCreation,
    parseTokenDeletion,
    parseTokenDissociate,
    parseTokenFeeScheduleUpdate,
    parseTokenFreeze,
    parseTokenGrantKyc,
    parseTokenList,
    parseTokenMint,
    parseTokenPause,
    parseTokenRevokeKyc,
    parseTokenUnfreeze,
    parseTokenUnpause,
    parseTokenUpdate,
    parseTokenWipe,
    parseTransferListItem,
    parseUnknownType,
)
from hedera.records.parse_tx_record import (
    parseSmartContractInfo,
    parseTokenTransferList,
    parseTransferListRecord,
    parseTxRecord,
)
from hedera.util.common.serializable import RecordStreamObject
from hedera.util.common.stream import SerializableDataInputStream
from hedera.util.proto_pb import (
    record_stream_file_pb2,
    transaction_body_pb2,
    transaction_contents_pb2,
    transaction_pb2,
    transaction_record_pb2,
)
from hedera.util.protobuf_to_dict import protobuf_to_dict
from hedera.util.utilities import dict_bytes_to_hex


@ray.remote
def parse_transaction_v5(chunk: list, timestamp: str, logger: logging.Logger) -> dict:
    """
    Methods to parse transactions (ray method)
    WARNING: This method is untested as this transaction format is no longer used by Hedera - we're
    leaving it in the parser in case we ever need to backfill historical data that uses this format

    :param chunk: array of dictionaries - each dict has a txn object to process and a corresponding filename
    :param timestamp: timestamp the transaction is processed by metrika
    :param logger: logger
    :returns parsed_txns: Flattened dictionary of relevant info from the transaction item
    """
    parser = RcdParser()
    parsed_txns = []

    for txn in chunk:
        try:
            transaction_item_dict = parser.create_v5_transaction_body(txn["txn_object"])
            transaction_record_dict = parser.create_v5_transaction_record(txn["txn_object"])
            tx_item = parser.parse_transaction_item(transaction_item_dict)
            tx_record = parser.parse_transaction_record(transaction_record_dict)
            output = {**tx_record, **tx_item}
            output = parser.reclassify_token_txns(output)
            output = parser.add_txn_metadata(output, timestamp, txn["filename"])
            output = dict_bytes_to_hex(output)
            parsed_txns.append(output)

        except TypeError as ex:
            logger.exception(
                f"Transaction object is incorrect type in {txn['filename']}.\n"
                f"Skipping transaction and moving to next one:\n {ex}"
            )
            continue
        except ValidationError as ex:
            logger.exception(
                f"Missing field for a transaction in {txn['filename']}.\n "
                f"Skipping transaction and moving to next one:\n {ex}"
            )
            continue
        except AttributeError as ex:
            logger.exception(
                f"Missing attribute for a transaction in {txn['filename']}.\n "
                f"Skipping transaction and moving to next one:\n {ex}"
            )
            continue
        except (
            ParseTxnItemError,
            ParseTxnRecordError,
            ReclassifyTokenTxnError,
            AddTxnMetadataError,
            CreateTimestampError,
        ) as ex:
            logger.exception(
                f"Unexpected error parsing transaction in{txn['filename']}.\n "
                f"Skipping transaction and moving to next one:\n {ex}"
            )
            continue

        except Exception as ex:
            raise ParseTxnError("Error in parse_transaction_v5") from ex

    return parsed_txns


@ray.remote
def parse_transaction_v6(chunk: list, timestamp: str, logger: logging.Logger) -> dict:
    """
    Methods to parse transactions (ray method)

    :param chunk: array of dictionaries - each dict has a txn object to process and a corresponding filename
    :param timestamp: timestamp the transaction is processed by metrika
    :param logger: logger

    :returns: Flattened dictionary of relevant info from the transaction item
    """
    parser = RcdParser()
    parsed_txns = []

    for txn in chunk:
        try:
            tx_item = parser.parse_transaction_item(txn["transaction_body"])
            tx_record = parser.parse_transaction_record(txn["transaction_record"])
            output = {**tx_record, **tx_item}
            output = {**output, **{"txn_sign_keys": txn["txn_sign_keys"]}}
            output = parser.reclassify_token_txns(output)
            output = parser.add_txn_metadata(output, timestamp, txn["filename"])
            output = dict_bytes_to_hex(output)
            parsed_txns.append(output)

        except TypeError as ex:
            logger.exception(
                f"Transaction object is incorrect type in {txn['filename']}.\n"
                f"Skipping transaction and moving to next one:\n {ex}"
            )
            continue
        except ValidationError as ex:
            logger.exception(
                f"Missing field for a transaction in {txn['filename']}.\n "
                f"Skipping transaction and moving to next one:\n {ex}"
            )
            continue
        except AttributeError as ex:
            logger.exception(
                f"Missing attribute for a transaction in {txn['filename']}.\n "
                f"Skipping transaction and moving to next one:\n {ex}"
            )
            continue
        except (
            ParseTxnItemError,
            ParseTxnRecordError,
            ReclassifyTokenTxnError,
            AddTxnMetadataError,
            CreateTimestampError,
            ParseSignKeysError,
        ) as ex:
            logger.exception(
                f"Unexpected error parsing transaction in{txn['filename']}.\n "
                f"Skipping transaction and moving to next one:\n {ex}"
            )
            continue

        except Exception as ex:
            raise ParseTxnError("Error in parse_transaction_v6") from ex

    return parsed_txns


class RcdParser:
    def __init__(self):
        """
        Constructor - Do All the initializations here.
        """
        self.logger = logging.getLogger(__name__)

    def __del__(self):
        """
        Destructor
        """
        logging.shutdown()

    def check_version(self, dis: bytes, filename: Union[str, pathlib.Path]) -> None:
        """
        Check versions of rcd file and asserts the record format version is 5

        :param dis: data input stream from rcd file
        :param filename: filename to track errors
        """
        EXPECTED_RECORD_FORMAT_VERSION = 5

        try:
            record_format_version = dis.read_int()
            assert record_format_version == EXPECTED_RECORD_FORMAT_VERSION
        except AssertionError:
            raise
        except Exception as ex:
            raise RecordFormatVersionError("Error checking record format version") from ex
        try:
            hapi_proto_major_version = dis.read_int()
            hapi_proto_minor_version = dis.read_int()
            hapi_proto_patch_version = dis.read_int()
            self.logger.debug(
                f"HAPI proto version: {hapi_proto_major_version}."
                f"{hapi_proto_minor_version}.{hapi_proto_patch_version}"
            )
        except Exception as ex:
            self.logger.exception(f"Error with hapi_proto_*_version: {filename} \nException: {repr(ex)}")
        try:
            object_stream_version = dis.read_int()
            self.logger.debug(f"Object stream version: {object_stream_version}")
        except Exception as ex:
            self.logger.exception(f"Error with object_stream_version: {filename} \nException: {repr(ex)}")

    def read_v6_file(self, rcd_name, filename):
        """
        Open/read protobuf formatted rcd files

        :param rcd_name: Full pth of file to open/read
        :param filename: Filename to track in data/logs

        :returns objs: List of transcations in file
        :returns version: Version of file format
        """
        with open(rcd_name, "rb") as f:
            pathlib.Path(f"{rcd_name}_processed").touch()
            objs = []
            record_stream_file = record_stream_file_pb2.RecordStreamFile()
            version = int.from_bytes(f.read(4), "big")
            f_read = f.read()
            record_stream_file.ParseFromString(f_read)
            record_stream_items = record_stream_file.record_stream_items
            if len(record_stream_items) > 0:
                objs = []
                for i in record_stream_items:
                    transaction_body = transaction_body_pb2.TransactionBody()
                    if len(i.transaction.signedTransactionBytes) > 0:
                        signed_transaction = transaction_contents_pb2.SignedTransaction()
                        signed_transaction.ParseFromString(i.transaction.signedTransactionBytes)
                        transaction_body.ParseFromString(signed_transaction.bodyBytes)
                        txn_keys = [list(protobuf_to_dict(k).keys())[-1] for k in signed_transaction.sigMap.sigPair]
                    else:
                        transaction_body.ParseFromString(i.transaction.bodyBytes)
                        txn_keys = [list(protobuf_to_dict(k).keys())[-1] for k in i.transaction.sigMap.sigPair]

                    transaction_record = protobuf_to_dict(i.record)
                    objs.append(
                        {
                            "filename": filename,
                            "transaction_record": transaction_record,
                            "transaction_body": protobuf_to_dict(transaction_body),
                            "txn_sign_keys": txn_keys,
                        }
                    )

            return objs, f"v{version}"

    def create_v5_transaction_body(self, object: bytes) -> dict:
        """
        Read the transaction item from the transaction object

        :param object: transaction object

        :returns: data collected when a transaction is submitted to the hedera network
        """
        try:
            transaction = transaction_pb2.Transaction()
            transaction.ParseFromString(object.transaction)
            transaction_body = transaction_body_pb2.TransactionBody()

            if len(transaction.signedTransactionBytes) > 0:
                signed_transaction = transaction_contents_pb2.SignedTransaction()
                signed_transaction.ParseFromString(transaction.signedTransactionBytes)
                transaction_body.ParseFromString(signed_transaction.bodyBytes)
            else:
                transaction_body.ParseFromString(transaction.bodyBytes)

            return protobuf_to_dict(transaction_body)
        except Exception as ex:
            raise CreateTransactionItemError("Unexpected error creating transaction item") from ex

    def create_v5_transaction_record(self, object: bytes) -> dict:
        """
        Read the transaction record from the transaction object

        :param object: transaction object

        :returns: data collected after a transaction is completed on the hedera network
        """
        try:
            transaction_record = transaction_record_pb2.TransactionRecord()
            transaction_record.ParseFromString(object.transactionRecord)

            return protobuf_to_dict(transaction_record)

        except Exception as ex:
            raise CreateTransactionRecordError("Unexpected error creating transaction record") from ex

    def parse_transaction_item(self, transaction_item_dict: dict) -> dict:
        """
        Parses info out of the hedera transaction item

        :param transaction_item_dict: dict data collected when a transaction is submitted to the hedera network

        :returns: Flattened dictionary of relevant info from the transaction item
        """
        try:
            tx_item = TransactionItem(**transaction_item_dict)
            tx_item_common = parseCommon(tx_item)

            if tx_item.consensusSubmitMessage is not None:
                tx_item_type = parseConsensusSubmitMessage(tx_item.consensusSubmitMessage)
            elif tx_item.consensusCreateTopic is not None:
                tx_item_type = parseConsensusCreateTopic(tx_item.consensusCreateTopic)
            elif tx_item.consensusUpdateTopic is not None:
                tx_item_type = parseConsensusUpdateTopic(tx_item.consensusUpdateTopic)
            elif tx_item.consensusDeleteTopic is not None:
                tx_item_type = parseConsensusDeleteTopic(tx_item.consensusDeleteTopic)
            elif tx_item.cryptoTransfer is not None:
                tx_item_type = parseCryptoTransfer(tx_item.cryptoTransfer)
                if tx_item_type.transferList is not None and tx_item_type.transferList["accountAmounts"] is not None:
                    transfer_list = parseTransferListItem(tx_item_type.transferList)
                    tx_item_type = {
                        **tx_item_type.dict(exclude_none=True),
                        **transfer_list,
                    }
                    del tx_item_type["transferList"]
            elif tx_item.cryptoCreateAccount is not None:
                tx_item_type = parseCryptoCreateAccount(tx_item.cryptoCreateAccount)
            elif tx_item.cryptoUpdateAccount is not None:
                tx_item_type = parseCryptoUpdateAccount(tx_item.cryptoUpdateAccount)
            elif tx_item.cryptoDelete is not None:
                tx_item_type = parseCryptoDelete(tx_item.cryptoDelete)
            elif tx_item.fileUpdate is not None:
                tx_item_type = parseFileUpdate(tx_item.fileUpdate)
            elif tx_item.fileAppend is not None:
                tx_item_type = parseFileAppend(tx_item.fileAppend)
            elif tx_item.fileDelete is not None:
                tx_item_type = parseFileDelete(tx_item.fileDelete)
            elif tx_item.fileCreate is not None:
                tx_item_type = parseFileCreate(tx_item.fileCreate)
            elif tx_item.scheduleSign is not None:
                tx_item_type = parseScheduleSign(tx_item.scheduleSign)
            elif tx_item.scheduleCreate is not None:
                tx_item_type = parseScheduleCreate(tx_item.scheduleCreate)
            elif tx_item.scheduleDelete is not None:
                tx_item_type = parseScheduleDelete(tx_item.scheduleDelete)
            elif tx_item.tokenCreation is not None:
                tx_item_type = parseTokenCreation(tx_item.tokenCreation)
            elif tx_item.tokenAssociate is not None:
                tx_item_type = parseTokenAssociate(tx_item.tokenAssociate)
                token_list = parseTokenList(tx_item_type.tokenList)
                tx_item_type = {
                    **tx_item_type.dict(exclude_none=True),
                    **token_list,
                }
                del tx_item_type["tokenList"]
            elif tx_item.tokenDissociate is not None:
                tx_item_type = parseTokenDissociate(tx_item.tokenDissociate)
                token_list = parseTokenList(tx_item_type.tokenList)
                tx_item_type = {
                    **tx_item_type.dict(exclude_none=True),
                    **token_list,
                }
                del tx_item_type["tokenList"]
            elif tx_item.tokenGrantKyc is not None:
                tx_item_type = parseTokenGrantKyc(tx_item.tokenGrantKyc)
            elif tx_item.tokenRevokeKyc is not None:
                tx_item_type = parseTokenRevokeKyc(tx_item.tokenRevokeKyc)
            elif tx_item.tokenMint is not None:
                tx_item_type = parseTokenMint(tx_item.tokenMint)
            elif tx_item.tokenFreeze is not None:
                tx_item_type = parseTokenFreeze(tx_item.tokenFreeze)
            elif tx_item.tokenUnfreeze is not None:
                tx_item_type = parseTokenUnfreeze(tx_item.tokenUnfreeze)
            elif tx_item.tokenPause is not None:
                tx_item_type = parseTokenPause(tx_item.tokenPause)
            elif tx_item.tokenUnpause is not None:
                tx_item_type = parseTokenUnpause(tx_item.tokenUnpause)
            elif tx_item.tokenDeletion is not None:
                tx_item_type = parseTokenDeletion(tx_item.tokenDeletion)
            elif tx_item.tokenUpdate is not None:
                tx_item_type = parseTokenUpdate(tx_item.tokenUpdate)
            elif tx_item.tokenBurn is not None:
                tx_item_type = parseTokenBurn(tx_item.tokenBurn)
            elif tx_item.tokenWipe is not None:
                tx_item_type = parseTokenWipe(tx_item.tokenWipe)
            elif tx_item.contractCreateInstance is not None:
                tx_item_type = parseContractCreateInstance(tx_item.contractCreateInstance)
            elif tx_item.contractUpdateInstance is not None:
                tx_item_type = parseContractUpdateInstance(tx_item.contractUpdateInstance)
            elif tx_item.contractCall is not None:
                tx_item_type = parseContractCall(tx_item.contractCall)
            elif tx_item.contractDeleteInstance is not None:
                tx_item_type = parseContractDelete(tx_item.contractDeleteInstance)
            elif tx_item.ethereumTransaction is not None:
                tx_item_type = parseEthereumTransaction(tx_item.ethereumTransaction)
            elif tx_item.cryptoApproveAllowance is not None:
                tx_item_type = parseCryptoApproveAllowance(tx_item.cryptoApproveAllowance)
            elif tx_item.cryptoDeleteAllowance is not None:
                tx_item_type = parseCryptoDeleteAllowance(tx_item.cryptoDeleteAllowance)
            elif tx_item.token_fee_schedule_update is not None:
                tx_item_type = parseTokenFeeScheduleUpdate(tx_item.token_fee_schedule_update)
            elif tx_item.node_stake_update is not None:
                tx_item_type = parseNodeStakeUpdate(tx_item.node_stake_update)
            else:
                unknown_type = UnknownType(**{"txn_type": "OTHER"})
                tx_item_type = parseUnknownType(unknown_type)

            if isinstance(tx_item_type, dict):
                tx_item_output = {
                    **tx_item_common.dict(by_alias=True),
                    **tx_item_type,
                }
            else:
                tx_item_output = {
                    **tx_item_common.dict(by_alias=True, exclude_none=True),
                    **tx_item_type.dict(by_alias=True, exclude_none=True),
                }

            return tx_item_output

        except AttributeError:
            raise
        except TypeError:
            raise
        except ValidationError:
            raise
        except Exception as ex:
            raise ParseTxnItemError("Unexpected error parsing transaction item") from ex

    def parse_transaction_record(self, transaction_record_dict: dict) -> dict:
        """
        Parses info out of the hedera transaction record

        :param transaction_record_dict: dict of data collected after a transaction is processed by the hedera network

        :returns: Flattened dictionary of relevant info from the transaction item
        """
        try:
            tx_record = TransactionRecord(**transaction_record_dict)
            tx_record_common = parseTxRecord(tx_record).dict(by_alias=True, exclude_none=True)
            tx_record_output = tx_record_common
            if tx_record.transferList is not None:
                if tx_record.transferList.accountAmounts is not None:
                    transfer_list = parseTransferListRecord(tx_record.transferList.dict())
                    tx_record_output = {**tx_record_common, **transfer_list}

            if tx_record.tokenTransferLists is not None:
                token_transfer_list = parseTokenTransferList(tx_record.tokenTransferLists[0], tx_record.receipt)
                tx_record_output = {**tx_record_output, **token_transfer_list}

            if tx_record.contractCreateResult is not None:
                smart_contract_info = parseSmartContractInfo(tx_record.contractCreateResult)
                tx_record_output = {**tx_record_output, **smart_contract_info}

            if tx_record.contractCallResult is not None:
                smart_contract_info = parseSmartContractInfo(tx_record.contractCallResult)
                tx_record_output = {**tx_record_output, **smart_contract_info}

            return tx_record_output

        except AttributeError:
            raise
        except TypeError:
            raise
        except ValidationError:
            raise
        except Exception as ex:
            raise ParseTxnRecordError("Unexpected error parsing transaction record") from ex

    def reclassify_token_txns(self, d: dict) -> dict:
        """
        By default, fungible token transactions are the same as nfts in the hedera transaction record/item - logic
        to correctly classify nft transactions

        :param d: dictionary of txn item/record with token transactions classified as one (e.g., TOKENMINT includes both
        fungible token mints and nft token mints)

        :returns: Output dictionary different txn types for fungible and non-fungible token transactions
        """
        try:
            if "nft_serial_number_1" in d:
                if d["txn_type"] == "CRYPTOTRANSFER":
                    d["txn_type"] = "NFTTRANSFER"
                if d["txn_type"] == "TOKENWIPE":
                    d["txn_type"] = "NFTWIPE"
                if d["txn_type"] == "TOKENBURN":
                    d["txn_type"] = "NFTBURN"
                if d["txn_type"] == "TOKENMINT":
                    d["txn_type"] = "NFTMINT"

            if "nft_serial_numbers" in d:
                if d["txn_type"] == "TOKENMINT":
                    d["txn_type"] = "NFTMINT"

            if "token_transfer_amount_1" in d:
                if d["txn_type"] == "CRYPTOTRANSFER":
                    d["txn_type"] = "TOKENTRANSFERS"

            if "token_type" in d:
                if d["token_type"] == 1:
                    d["txn_type"] = "NFTCREATION"

            return d

        except Exception as ex:
            raise ReclassifyTokenTxnError("Unexpected error reclassifying token transactions") from ex

    def add_txn_metadata(self, d: dict, ts: str, f: str) -> dict:
        """
        General cleanup and adding txn metadata(e.g., converting epochs to datetime)

         :param f: rcd filename
         :param ts: processed timestamp
         :param d: The Hedera transaction record in json format

         :returns: Output dictionary with metadata and elastic-compatible timestamps
        """
        try:
            d["@processed"] = ts
            d["rcd_filename"] = f.split("/")[-1]
            d["msg"] = "transaction"

            d["body.@timestamp"] = self.create_ts(
                d["body.transactionValidStart.seconds"],
                d["body.transactionValidStart.nanos"],
            )
            d["record.@timestamp"] = self.create_ts(
                d["record.transactionValidStart.seconds"],
                d["record.transactionValidStart.nanos"],
            )
            d["consensusTimestamp"] = self.create_ts(
                d["record.consensusTimestamp.seconds"],
                d["record.consensusTimestamp.nanos"],
            )

            return d

        except CreateTimestampError:
            raise
        except Exception as ex:
            raise AddTxnMetadataError("Unexpected error adding transaction metadata") from ex

    def create_ts(self, seconds: int, nanos: int) -> dict:
        """
        Convert epoch seconds and nanos to elastic compatible iso-8601 format timestamp

        :param seconds: epoch seconds
        :param nanos: epoch nanoseconds

        :returns: Output dictionary with metadata and elastic-compatible timestamps
        """
        try:
            if nanos is not None:
                ts = (
                    pendulum.from_timestamp(int(str(seconds))).isoformat("T")[:19]
                    + "."
                    + str(round(int(str(nanos)) / 10**6))
                    + "Z"
                )
            else:
                ts = pendulum.from_timestamp(seconds).isoformat("T")[:19] + ".000Z"
            return ts

        except Exception as ex:
            raise CreateTimestampError("Unexpected error creating timestamp") from ex

    def load_txns(self, filename, path):
        """
        This method loads transactions from an rcd file and appends them to an array that can be processed
        in parallel by ray

        :param filename: The recordstream/RCD file to be loaded
        :param path: Path to recordstream/RCD file

        :returns objs: List of transcations in file
        :returns version: Version of file format
        """
        try:
            if filename.split(".")[-2] == "rcd":
                rcd_file_basename = os.path.basename(filename)
                index = rcd_file_basename.rindex(".")
                rcd_name = path + rcd_file_basename[:index]
                with gzip.open(filename, "rb") as f_in:
                    with open(rcd_name, "wb") as f_out:
                        shutil.copyfileobj(f_in, f_out)
                    f_out.close()
                return self.read_v6_file(rcd_name, filename)
            else:
                with open(filename, "rb") as f:
                    objs = []
                    dis = SerializableDataInputStream(f)
                    self.check_version(dis, filename)
                    while dis.available():
                        object = dis.readSerializable(True, None)
                        if isinstance(object, RecordStreamObject):
                            objs.append({"filename": filename, "txn_object": object})
                    return objs, "v5"

        except FileNotFoundError as ex:
            self.logger.exception(f"{filename} not found: {ex}")
        except AssertionError as ex:
            self.logger.exception(f"Mismatch between expected record format version found in {filename}:\n {ex}")
        except RecordFormatVersionError as ex:
            self.logger.exception(f"Unexpected error when checking record version in {filename}:\n {ex}")
        except NameError as ex:
            self.logger.exception(f"{ex}")
        except AttributeError as ex:
            self.logger.exception(f"{ex}")
