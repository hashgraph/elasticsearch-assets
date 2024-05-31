from typing import List, Union

from pydantic import validate_arguments

from hedera.models.tx_record import TransactionRecord, TxRecordParsed
from hedera.util.utilities import parse_flat_fields


@validate_arguments()
def parseTxRecord(transaction_record: TransactionRecord) -> TxRecordParsed:
    """
    Parses the transaction record

    :param transaction record: The Hedera transaction record

    :returns TxRecordParsed(**output): Dictionary key fields in the transaction record object
    """
    output = {
        "status": transaction_record.receipt.status,
        "currentRate.hbarEquiv": transaction_record.receipt.exchangeRate.currentRate.hbarEquiv,
        "currentRate.centEquiv": transaction_record.receipt.exchangeRate.currentRate.centEquiv,
        "currentRate.expirationTime.seconds": transaction_record.receipt.exchangeRate.currentRate.expirationTime.seconds,
        "nextRate.hbarEquiv": transaction_record.receipt.exchangeRate.nextRate.hbarEquiv,
        "nextRate.centEquiv": transaction_record.receipt.exchangeRate.nextRate.centEquiv,
        "nextRate.expirationTime.seconds": transaction_record.receipt.exchangeRate.nextRate.expirationTime.seconds,
        "record.transactionHash": str(transaction_record.transactionHash.hex()),
        "record.consensusTimestamp.seconds": transaction_record.consensusTimestamp.seconds,
        "record.consensusTimestamp.nanos": transaction_record.consensusTimestamp.nanos,
        "record.transactionValidStart.seconds": transaction_record.transactionID.transactionValidStart.seconds,
        "record.transactionValidStart.nanos": transaction_record.transactionID.transactionValidStart.nanos,
        "record.accountID.accountNum": transaction_record.transactionID.accountID.accountNum,
        "record.transactionFee": transaction_record.transactionFee,
        "record.memo": transaction_record.memo,
        "topic_sequence_number": transaction_record.receipt.topicSequenceNumber,
        "topic_running_hash": transaction_record.receipt.topicRunningHash,
        "topic_running_hash_version": transaction_record.receipt.topicRunningHashVersion,
        "created_account": transaction_record.receipt.accountID.accountNum,
        "schedule_id": transaction_record.receipt.scheduleID.scheduleNum,
        "token_number": transaction_record.receipt.tokenID.tokenNum,
        "file_id": transaction_record.receipt.fileID.fileNum,
        "consensus_create_topicID": transaction_record.receipt.topicID.topicNum,
        "serialNumbers": transaction_record.receipt.serialNumbers,
        "transfer_list": transaction_record.transferList.accountAmounts,
        "token_transfer_list": transaction_record.tokenTransferLists,
    }

    return TxRecordParsed(**output)


def parseTransferListRecord(transfer_list: list) -> dict:
    """
    Parses the transfer list

    :param transaction record: The Hedera transaction record

    :returns transfer_list_dict: Dictionary of senders, receivers, and amounts for transfers and txn fees
    """
    transfer_list_dict = {}

    transfer_account_id_account_num = [item["accountID"]["accountNum"] for item in transfer_list["accountAmounts"]]
    transfer_amounts = [item["amount"] for item in transfer_list["accountAmounts"]]

    ct = 1
    for item in transfer_account_id_account_num:
        transfer_list_dict[f"record.accountNum.{str(ct)}"] = item
        ct += 1

    ct = 1
    for item in transfer_amounts:
        transfer_list_dict[f"record.amount.{str(ct)}"] = item
        ct += 1

    return transfer_list_dict


def parseTokenTransferList(token_transfer_list: list, nft_receipt) -> dict:
    """
    Parses the token transfer list

    :param token_transfer_list: The Hedera transaction record

    :returns token_transfer_list_dict: Dictionary of senders, receivers, and amounts for token transfers
    """
    token_transfer_list_dict = {}
    token_transfer_list_dict["token_number"] = token_transfer_list.token.tokenNum

    if token_transfer_list.transfers is not None:
        token_transfers = parseTokenTransfers(token_transfer_list.transfers)
        token_transfer_list_dict = {
            **token_transfer_list_dict,
            **token_transfers,
        }

    if token_transfer_list.nftTransfers is not None:
        nft_transfers = parseNftTransfers(token_transfer_list.nftTransfers, nft_receipt)
        token_transfer_list_dict = {
            **token_transfer_list_dict,
            **nft_transfers,
        }

    return token_transfer_list_dict


def parseTokenTransfers(token_transfers: list) -> dict:
    """
    Parses token transfers

    :param token_transfers: List of senders, receivers, and amounts of token transfers

    :returns flat_token_transfers: Flattened dictionary of senders, receivers and amounts of token transfers
    """
    flat_token_transfers = {}

    ct = 1
    for item in token_transfers:
        flat_token_transfers["token_transfer_account_" + str(ct)] = item["accountID"]["accountNum"]
        flat_token_transfers["token_transfer_amount_" + str(ct)] = item["amount"]
        ct += 1

    return flat_token_transfers


def parseNftTransfers(nft_transfers, nft_receipt):
    """
    Parses nft specific info

    :param transaction record: The Hedera transaction record

    :returns flat_nft_transfers: Dictionary of nft specific fields
    """
    flat_nft_transfers = {}
    ct = 1
    for item in nft_transfers:
        if "accountNum" in item["senderAccountID"]:
            flat_nft_transfers["nft_sender_" + str(ct)] = item["senderAccountID"]["accountNum"]
        if "accountNum" in item["receiverAccountID"]:
            flat_nft_transfers["nft_receiver_" + str(ct)] = item["receiverAccountID"]["accountNum"]
        flat_nft_transfers["nft_serial_number_" + str(ct)] = item["serialNumber"]
        ct += 1

    if len(nft_receipt.serialNumbers) > 0:
        flat_nft_transfers["nft_serial_numbers"] = nft_receipt.serialNumbers

    return flat_nft_transfers


def parseSmartContractInfo(contract_result: dict) -> dict:
    """
    Parses smart contract specific info

    :param contract_result: The Hedera transaction record

    :returns flat_smart_contract_info: Dictionary of smart contract specific fields
    """
    flat_smart_contract_info = {}

    flat_fields = [
        "contractID",
        "contractCallResult",
        "bloom",
        "gasUsed",
        "createdContractIDs",
    ]
    flat_smart_contract_info.update(parse_flat_fields(contract_result, flat_fields, "record"))
    if "logInfo" in contract_result:
        logInfo_record = contract_result["logInfo"]
        logInfo_flat_fields = ["contractID", "bloom", "topic", "data"]
        if len(logInfo_record) == 1:
            flat_smart_contract_info.update(parse_flat_fields(logInfo_record[0], logInfo_flat_fields, "record.logInfo"))
        else:
            for i in range(len(logInfo_record)):
                flat_smart_contract_info.update(
                    parse_flat_fields(
                        logInfo_record[i],
                        logInfo_flat_fields,
                        f"record.logInfo.{i}",
                    )
                )

    return flat_smart_contract_info
