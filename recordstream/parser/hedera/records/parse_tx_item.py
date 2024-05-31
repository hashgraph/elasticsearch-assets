from typing import List, Union

from pydantic import validate_arguments

from hedera.models.tx_item import (
    CommonParsed,
    ConsensusCreateTopic,
    ConsensusCreateTopicParsed,
    ConsensusDeleteTopic,
    ConsensusDeleteTopicParsed,
    ConsensusSubmitMessage,
    ConsensusSubmitMessageParsed,
    ConsensusUpdateTopic,
    ConsensusUpdateTopicParsed,
    ContractCall,
    ContractCallParsed,
    ContractCreateInstance,
    ContractCreateInstanceParsed,
    ContractDeleteInstance,
    ContractDeleteInstanceParsed,
    ContractUpdateInstance,
    ContractUpdateInstanceParsed,
    CryptoApproveAllowance,
    CryptoApproveAllowanceParsed,
    CryptoCreateAccount,
    CryptoCreateAccountParsed,
    CryptoDelete,
    CryptoDeleteAllowance,
    CryptoDeleteAllowanceParsed,
    CryptoDeleteParsed,
    CryptoTransfer,
    CryptoTransferParsed,
    CryptoUpdateAccount,
    CryptoUpdateAccountParsed,
    EthereumTransaction,
    EthereumTransactionParsed,
    FileAppend,
    FileAppendParsed,
    FileCreate,
    FileCreateParsed,
    FileDelete,
    FileDeleteParsed,
    FileUpdate,
    FileUpdateParsed,
    NodeStakeUpdate,
    NodeStakeUpdateParsed,
    ScheduleCreate,
    ScheduleCreateParsed,
    ScheduleDelete,
    ScheduleDeleteParsed,
    ScheduleSign,
    ScheduleSignParsed,
    TokenAssociate,
    TokenAssociateParsed,
    TokenBurn,
    TokenBurnParsed,
    TokenCreation,
    TokenCreationParsed,
    TokenDeletion,
    TokenDeletionParsed,
    TokenDissociate,
    TokenDissociateParsed,
    TokenFeeScheduleUpdate,
    TokenFeeScheduleUpdateParsed,
    TokenFreeze,
    TokenFreezeParsed,
    TokenGrantKyc,
    TokenGrantKycParsed,
    TokenMint,
    TokenMintParsed,
    TokenPause,
    TokenPauseParsed,
    TokenRevokeKyc,
    TokenRevokeKycParsed,
    TokenUnfreeze,
    TokenUnfreezeParsed,
    TokenUnpause,
    TokenUnpauseParsed,
    TokenUpdate,
    TokenUpdateParsed,
    TokenWipe,
    TokenWipeParsed,
    TransactionItem,
    UnknownType,
    UnknownTypeParsed,
)


@validate_arguments()
def parseCommon(
    transaction_item: TransactionItem,
) -> CommonParsed:
    """
    Parses common fields from the transaction item

    :param transaction_item: The Hedera transaction item

    :returns: Dictionary of common fields in the transaction item object
    """
    output = {
        "body.transactionValidStart.seconds": transaction_item.transactionID.transactionValidStart.seconds,
        "body.transactionValidStart.nanos": transaction_item.transactionID.transactionValidStart.nanos,
        "body.accountID.accountNum": transaction_item.transactionID.accountID.accountNum,
        "body.nodeAccountID.accountNum": transaction_item.nodeAccountID.accountNum,
        "scheduled": transaction_item.transactionID.scheduled,
        "body.transactionFee": transaction_item.transactionFee,
        "body.transactionValidDuration.seconds": transaction_item.transactionValidDuration.seconds,
        "nonce": transaction_item.transactionID.nonce,
    }

    return CommonParsed(**output)


@validate_arguments()
def parseConsensusSubmitMessage(
    consensus_submit_message: ConsensusSubmitMessage,
) -> ConsensusSubmitMessageParsed:
    """
    Parses consensus submit message info from the transaction item

    :param transaction item: The Hedera transaction item

    :returns: Dictionary of consensus submit message fields in the transaction item object
    """
    output = {
        "consensus_submit_topicID": consensus_submit_message.topicID.topicNum,
        "consensus_submit_message": str(consensus_submit_message.message),
        "consensus_submit_message_bytes": len(consensus_submit_message.message),
        "txn_type": consensus_submit_message.txn_type,
    }

    return ConsensusSubmitMessageParsed(**output)


@validate_arguments()
def parseConsensusCreateTopic(
    consensus_create_topic: ConsensusCreateTopic,
) -> ConsensusCreateTopicParsed:
    """
    Parses consensus create topic info from the transaction item

    :param transaction item: The Hedera transaction item

    :returns: Dictionary of consensus create topic fields in the transaction item object
    """
    output = {
        "consensus_create_memo": consensus_create_topic.memo,
        "txn_type": consensus_create_topic.txn_type,
    }

    return ConsensusCreateTopicParsed(**output)


@validate_arguments()
def parseConsensusUpdateTopic(
    consensus_update_topic: ConsensusUpdateTopic,
) -> ConsensusUpdateTopicParsed:
    """
    Parses consensus update topic info from the transaction item

    :param transaction item: The Hedera transaction item

    :returns: Dictionary of consensus update topic fields in the transaction item object
    """
    output = {
        "consensus_update_topicID": consensus_update_topic.topicID.topicNum,
        "txn_type": consensus_update_topic.txn_type,
    }

    return ConsensusUpdateTopicParsed(**output)


@validate_arguments()
def parseConsensusDeleteTopic(
    consensus_delete_topic: ConsensusDeleteTopic,
) -> ConsensusDeleteTopicParsed:
    """
    Parses consensus update topic info from the transaction item

    :param transaction item: The Hedera transaction item

    :returns: Dictionary of consensus update topic fields in the transaction item object
    """
    output = {
        "consensus_delete_topicID": consensus_delete_topic.topicID.topicNum,
        "txn_type": consensus_delete_topic.txn_type,
    }

    return ConsensusDeleteTopicParsed(**output)


@validate_arguments()
def parseCryptoTransfer(
    crypto_transfer: CryptoTransfer,
) -> CryptoTransferParsed:
    """
    Parses token wipe info from the transaction item

    :param transaction item: The Hedera transaction item

    :returns: Dictionary of token wipe  info in the transaction item object
    """
    output = {
        "transferList": crypto_transfer.transfers,
        "txn_type": crypto_transfer.txn_type,
    }

    return CryptoTransferParsed(**output)


def parseTransferListItem(transfer_list):
    """
    Parses the crypto transfer list

    :param transaction record: The Hedera crypto transfer record

    :returns: Dictionary of senders, receivers, and amounts for transfers and txn fees
    """
    transfer_list_dict = {}

    transfer_account_id_account_num = [
        item["accountID"]["accountNum"] for item in transfer_list["accountAmounts"] if "accountNum" in item["accountID"]
    ]
    transfer_amounts = [item["amount"] for item in transfer_list["accountAmounts"] if "amount" in item]

    ct = 1
    for item in transfer_account_id_account_num:
        transfer_list_dict[f"body.accountNum.{str(ct)}"] = item
        ct += 1

    ct = 1
    for item in transfer_amounts:
        transfer_list_dict[f"body.amount.{str(ct)}"] = item
        ct += 1

    return transfer_list_dict


@validate_arguments()
def parseCryptoCreateAccount(
    crypto_create_account: CryptoCreateAccount,
) -> CryptoCreateAccountParsed:
    """
    Parses crypto create account info from the transaction item

    :param transaction item: The Hedera transaction item

    :returns: Dictionary of crypto create account fields in the transaction item object
    """
    output = {
        "body.key": str(crypto_create_account.key.ed25519),
        "body.sendRecordThreshold": crypto_create_account.sendRecordThreshold,
        "body.receiveRecordThreshold": str(crypto_create_account.receiveRecordThreshold),
        "body.autoRenewPeriod": str(crypto_create_account.autoRenewPeriod.seconds),
        "txn_type": crypto_create_account.txn_type,
    }

    return CryptoCreateAccountParsed(**output)


@validate_arguments()
def parseCryptoUpdateAccount(
    crypto_update_account: CryptoUpdateAccount,
) -> CryptoUpdateAccountParsed:
    """
    Parses crypto update account info from the transaction item

    :param transaction item: The Hedera transaction item

    :returns: Dictionary of crypto update account fields in the transaction item object
    """
    output = {
        "updated_account": crypto_update_account.accountIDToUpdate.accountNum,
        "body.key": str(crypto_update_account.key.ed25519),
        "txn_type": crypto_update_account.txn_type,
    }

    return CryptoUpdateAccountParsed(**output)


@validate_arguments()
def parseCryptoDelete(
    crypto_delete: CryptoDelete,
) -> CryptoDeleteParsed:
    """
    Parses crypto update account info from the transaction item

    :param transaction item: The Hedera transaction item

    :returns: Dictionary of crypto update account fields in the transaction item object
    """
    output = {
        "deleted_account": crypto_delete.deleteAccountID.accountNum,
        "txn_type": crypto_delete.txn_type,
    }

    return CryptoDeleteParsed(**output)


@validate_arguments()
def parseFileUpdate(
    file_update: FileUpdate,
) -> FileUpdateParsed:
    """
    Parses file txn info from the transaction item

    :param transaction item: The Hedera transaction item

    :returns: Dictionary of file txn fields in the transaction item object
    """
    output = {
        "file_id": file_update.fileID.fileNum,
        "txn_type": file_update.txn_type,
    }

    return FileUpdateParsed(**output)


@validate_arguments()
def parseFileDelete(
    file_delete: FileDelete,
) -> FileDeleteParsed:
    """
    Parses file txn info from the transaction item

    :param transaction item: The Hedera transaction item

    :returns: Dictionary of file txn fields in the transaction item object
    """
    output = {
        "file_id": file_delete.fileID.fileNum,
        "txn_type": file_delete.txn_type,
    }

    return FileDeleteParsed(**output)


@validate_arguments()
def parseFileAppend(
    file_append: FileAppend,
) -> FileAppendParsed:
    """
    Parses file txn info from the transaction item

    :param transaction item: The Hedera transaction item

    :returns: Dictionary of file txn fields in the transaction item object
    """
    output = {
        "file_id": file_append.fileID.fileNum,
        "txn_type": file_append.txn_type,
    }

    return FileAppendParsed(**output)


@validate_arguments()
def parseFileCreate(
    file_create: FileCreate,
) -> FileCreateParsed:
    """
    Parses file txn info from the transaction item

    :param transaction item: The Hedera transaction item

    :returns: Dictionary of file txn fields in the transaction item object
    """
    output = {"txn_type": file_create.txn_type}

    return FileCreateParsed(**output)


@validate_arguments()
def parseScheduleCreate(
    schedule_create: ScheduleCreate,
) -> ScheduleCreateParsed:
    """
    Parses schedule create txn info from the transaction item

    :param transaction item: The Hedera transaction item

    :returns: Dictionary of schedule create txn fields in the transaction item object
    """
    output = {
        "schedule_txn_body": schedule_create.scheduledTransactionBody,
        "txn_type": schedule_create.txn_type,
    }

    return ScheduleCreateParsed(**output)


@validate_arguments()
def parseScheduleSign(
    schedule_sign: ScheduleSign,
) -> ScheduleSignParsed:
    """
    Parses schedule sign txn info from the transaction item

    :param transaction item: The Hedera transaction item

    :returns: Dictionary of schedule sign txn fields in the transaction item object
    """
    output = {
        "schedule_id": schedule_sign.scheduleID.scheduleNum,
        "txn_type": schedule_sign.txn_type,
    }

    return ScheduleSignParsed(**output)


@validate_arguments()
def parseScheduleDelete(
    schedule_delete: ScheduleDelete,
) -> ScheduleDeleteParsed:
    """
    Parses schedule delete txn info from the transaction item

    :param transaction item: The Hedera transaction item

    :returns: Dictionary of schedule delete txn fields in the transaction item object
    """
    output = {
        "schedule_id": schedule_delete.scheduleID.scheduleNum,
        "txn_type": schedule_delete.txn_type,
    }

    return ScheduleDeleteParsed(**output)


@validate_arguments()
def parseTokenAssociate(
    token_associate: TokenAssociate,
) -> TokenAssociateParsed:
    """
    Parses token associate info from the transaction item

    :param transaction item: The Hedera transaction item

    :returns: Dictionary of token associate fields in the transaction item object
    """
    output = {
        "token_account_number": token_associate.account.accountNum,
        "tokenList": token_associate.tokens,
        "txn_type": token_associate.txn_type,
    }

    return TokenAssociateParsed(**output)


@validate_arguments()
def parseTokenDissociate(
    token_dissociate: TokenDissociate,
) -> TokenDissociateParsed:
    """
    Parses token associate info from the transaction item

    :param transaction item: The Hedera transaction item

    :returns: Dictionary of token associate fields in the transaction item object
    """
    output = {
        "token_account_number": token_dissociate.account.accountNum,
        "tokenList": token_dissociate.tokens,
        "txn_type": token_dissociate.txn_type,
    }

    return TokenDissociateParsed(**output)


def parseTokenList(token_list):
    token_list_dict = {}
    ct = 1
    for token in token_list:
        if ct == 1:
            token_list_dict["token_number"] = str(token["tokenNum"])
        else:
            token_list_dict["token_number" + str(ct)] = str(token["tokenNum"])
        ct += 1

    return token_list_dict


@validate_arguments()
def parseTokenRevokeKyc(
    token_revoke_kyc: TokenRevokeKyc,
) -> TokenRevokeKycParsed:
    """
    Parses token wipe info from the transaction item

    :param transaction item: The Hedera transaction item

    :returns: Dictionary of token wipe  info in the transaction item object
    """
    output = {
        "token_number": token_revoke_kyc.token.tokenNum,
        "token_account_number": token_revoke_kyc.account.accountNum,
        "txn_type": token_revoke_kyc.txn_type,
    }

    return TokenRevokeKycParsed(**output)


@validate_arguments()
def parseTokenGrantKyc(
    token_grant_kyc: TokenGrantKyc,
) -> TokenGrantKycParsed:
    """
    Parses token wipe info from the transaction item

    :param transaction item: The Hedera transaction item

    :returns: Dictionary of token wipe  info in the transaction item object
    """
    output = {
        "token_number": token_grant_kyc.token.tokenNum,
        "token_account_number": token_grant_kyc.account.accountNum,
        "txn_type": token_grant_kyc.txn_type,
    }

    return TokenGrantKycParsed(**output)


@validate_arguments()
def parseTokenFreeze(
    token_freeze: TokenFreeze,
) -> TokenFreezeParsed:
    """
    Parses token wipe info from the transaction item

    :param transaction item: The Hedera transaction item

    :returns: Dictionary of token wipe  info in the transaction item object
    """
    output = {
        "token_number": token_freeze.token.tokenNum,
        "token_account_number": token_freeze.account.accountNum,
        "txn_type": token_freeze.txn_type,
    }

    return TokenFreezeParsed(**output)


@validate_arguments()
def parseTokenUnfreeze(
    token_unfreeze: TokenUnfreeze,
) -> TokenUnfreezeParsed:
    """
    Parses token wipe info from the transaction item

    :param transaction item: The Hedera transaction item

    :returns: Dictionary of token wipe  info in the transaction item object
    """
    output = {
        "token_number": token_unfreeze.token.tokenNum,
        "token_account_number": token_unfreeze.account.accountNum,
        "txn_type": token_unfreeze.txn_type,
    }

    return TokenUnfreezeParsed(**output)


@validate_arguments()
def parseTokenPause(
    token_pause: TokenPause,
) -> TokenPauseParsed:
    """
    Parses token wipe info from the transaction item

    :param transaction item: The Hedera transaction item

    :returns: Dictionary of token wipe  info in the transaction item object
    """
    output = {
        "token_number": token_pause.token.tokenNum,
        "txn_type": token_pause.txn_type,
    }

    return TokenPauseParsed(**output)


@validate_arguments()
def parseTokenUnpause(
    token_unpause: TokenUnpause,
) -> TokenUnpauseParsed:
    """
    Parses token wipe info from the transaction item

    :param transaction item: The Hedera transaction item

    :returns: Dictionary of token wipe  info in the transaction item object
    """
    output = {
        "token_number": token_unpause.token.tokenNum,
        "txn_type": token_unpause.txn_type,
    }

    return TokenUnpauseParsed(**output)


@validate_arguments()
def parseTokenDeletion(
    token_deletion: TokenDeletion,
) -> TokenDeletionParsed:
    """
    Parses token wipe info from the transaction item

    :param transaction item: The Hedera transaction item

    :returns: Dictionary of token wipe  info in the transaction item object
    """
    output = {
        "token_number": token_deletion.token.tokenNum,
        "txn_type": token_deletion.txn_type,
    }

    return TokenDeletionParsed(**output)


@validate_arguments()
def parseTokenMint(
    token_mint: TokenMint,
) -> TokenMintParsed:
    """
    Parses token wipe info from the transaction item

    :param transaction item: The Hedera transaction item

    :returns: Dictionary of token wipe  info in the transaction item object
    """
    output = {
        "token_number": token_mint.token.tokenNum,
        "token_mint_amount": token_mint.amount,
        "token_mint_metadata": token_mint.metadata,
        "txn_type": token_mint.txn_type,
    }

    return TokenMintParsed(**output)


@validate_arguments()
def parseTokenWipe(
    token_wipe: TokenWipe,
) -> TokenWipeParsed:
    """
    Parses token wipe info from the transaction item

    :param transaction item: The Hedera transaction item

    :returns: Dictionary of token wipe  info in the transaction item object
    """
    print(token_wipe)
    output = {
        "token_number": token_wipe.token.tokenNum,
        "token_account_number": token_wipe.account.accountNum,
        "token_wipe_amount": token_wipe.amount,
        "nft_serial_numbers": token_wipe.serialNumbers,
        "txn_type": token_wipe.txn_type,
    }
    return TokenWipeParsed(**output)


@validate_arguments()
def parseTokenBurn(
    token_burn: TokenBurn,
) -> TokenBurnParsed:
    """
    Parses token burn info from the transaction item

    :param transaction item: The Hedera transaction item

    :returns: Dictionary of token burn  info in the transaction item object
    """
    output = {
        "token_number": token_burn.token.tokenNum,
        "token_account_number": token_burn.account.accountNum,
        "token_burn_amount": token_burn.amount,
        "nft_serial_numbers": token_burn.serialNumbers,
        "txn_type": token_burn.txn_type,
    }

    return TokenBurnParsed(**output)


@validate_arguments()
def parseTokenCreation(
    token_creation: TokenCreation,
) -> TokenCreationParsed:
    """
    Parses token creation info from the transaction item

    :param transaction item: The Hedera transaction item

    :returns: Dictionary of token creation info in the transaction item object
    """
    output = {
        "token_name": token_creation.name,
        "token_symbol": token_creation.symbol,
        "token_type": token_creation.tokenType,
        "token_decimals": token_creation.decimals,
        "token_account_number": token_creation.treasury.accountNum,
        "token_admin_key": str(token_creation.adminKey.ed25519),
        "token_kyc_key": str(token_creation.kycKey.ed25519),
        "token_wipe_key": str(token_creation.wipeKey.ed25519),
        "token_supply_key": str(token_creation.supplyKey.ed25519),
        "token_freeze_key": str(token_creation.freezeKey.ed25519),
        "auto_renew_account": token_creation.autoRenewAccount.accountNum,
        "auto_renew_period_seconds": token_creation.autoRenewPeriod.seconds,
        "auto_renew_period_nanos": token_creation.autoRenewPeriod.nanos,
        "memo": token_creation.memo,
        "supply_type": token_creation.supplyType,
        "max_supply": token_creation.maxSupply,
        "token_initial_supply": token_creation.initialSupply,
        "txn_type": token_creation.txn_type,
    }

    return TokenCreationParsed(**output)


@validate_arguments()
def parseTokenUpdate(
    token_update: TokenUpdate,
) -> TokenUpdateParsed:
    """
    Parses token creation info from the transaction item

    :param transaction item: The Hedera transaction item

    :returns: Dictionary of token creation info in the transaction item object
    """
    output = {
        "token_name": token_update.name,
        "token_symbol": token_update.symbol,
        "token_type": token_update.tokenType,
        "token_account_number": token_update.treasury.accountNum,
        "token_admin_key": str(token_update.adminKey.ed25519),
        "token_kyc_key": str(token_update.kycKey.ed25519),
        "token_wipe_key": str(token_update.wipeKey.ed25519),
        "token_supply_key": str(token_update.supplyKey.ed25519),
        "token_freeze_key": str(token_update.freezeKey.ed25519),
        "auto_renew_account": token_update.autoRenewAccount.accountNum,
        "memo": token_update.memo,
        "txn_type": token_update.txn_type,
    }

    return TokenUpdateParsed(**output)


@validate_arguments()
def parseContractCreateInstance(
    contract_create_instance: ContractCreateInstance,
) -> ContractCreateInstanceParsed:
    """
    Parses token creation info from the transaction item

    :param transaction item: The Hedera transaction item

    :returns: Dictionary of token creation info in the transaction item object
    """
    output = {
        "file_id": contract_create_instance.fileID.fileNum,
        "body.gasUsed": contract_create_instance.gas,
        "auto_renew_period_seconds": contract_create_instance.autoRenewPeriod.seconds,
        "auto_renew_period_nanos": contract_create_instance.autoRenewPeriod.nanos,
        "admin_key": contract_create_instance.adminKey,
        "initial_balance": contract_create_instance.initialBalance,
        "proxy_account_id": contract_create_instance.proxyAccountID,
        "memo": contract_create_instance.memo,
        "txn_type": contract_create_instance.txn_type,
    }

    return ContractCreateInstanceParsed(**output)


@validate_arguments()
def parseContractUpdateInstance(
    contract_update_instance: ContractUpdateInstance,
) -> ContractUpdateInstanceParsed:
    """
    Parses token creation info from the transaction item

    :param transaction item: The Hedera transaction item

    :returns: Dictionary of token creation info in the transaction item object
    """
    output = {
        "body.contractID": contract_update_instance.contractID.contractNum,
        "txn_type": contract_update_instance.txn_type,
    }

    return ContractUpdateInstanceParsed(**output)


@validate_arguments()
def parseContractCall(
    contract_call: ContractCall,
) -> ContractCallParsed:
    """
    Parses token creation info from the transaction item

    :param transaction item: The Hedera transaction item

    :returns: Dictionary of token creation info in the transaction item object
    """
    output = {
        "body.contractID": contract_call.contractID.contractNum,
        "body.gasUsed": contract_call.gas,
        "amount": contract_call.amount,
        "txn_type": contract_call.txn_type,
    }

    return ContractCallParsed(**output)


@validate_arguments()
def parseContractDelete(
    contract_delete: ContractDeleteInstance,
) -> ContractDeleteInstanceParsed:
    """
    Parses token creation info from the transaction item

    :param transaction item: The Hedera transaction item

    :returns: Dictionary of token creation info in the transaction item object
    """
    output = {
        "body.contractID": contract_delete.contractID.contractNum,
        "txn_type": contract_delete.txn_type,
    }

    return ContractDeleteInstanceParsed(**output)


@validate_arguments()
def parseEthereumTransaction(
    ethereum_transaction: EthereumTransaction,
) -> EthereumTransactionParsed:
    """
    Parses ethereum transaction info from the transaction item

    :param transaction item: The Hedera transaction item

    :returns: Dictionary of ethereum transaction info in the transaction item object
    """
    output = {
        "ethereum_data": str(ethereum_transaction.ethereum_data),
        "call_data": ethereum_transaction.call_data,
        "max_gas_allowance": ethereum_transaction.max_gas_allowance,
        "txn_type": ethereum_transaction.txn_type,
    }

    return EthereumTransactionParsed(**output)


@validate_arguments()
def parseCryptoApproveAllowance(
    crypto_approve_allowance: CryptoApproveAllowance,
) -> CryptoApproveAllowanceParsed:
    """
    Parses crypto approve allowance type from the transaction item

    :param transaction item: The Hedera transaction item

    :returns: Dictionary of crypto approve allowance type in the transaction item object
    """
    output = {"txn_type": crypto_approve_allowance.txn_type}

    return CryptoApproveAllowanceParsed(**output)


@validate_arguments()
def parseCryptoDeleteAllowance(
    crypto_delete_allowance: CryptoDeleteAllowance,
) -> CryptoDeleteAllowanceParsed:
    """
    Parses crypto delete allowance type from the transaction item

    :param transaction item: The Hedera transaction item

    :returns: Dictionary of crypto delete allowance type in the transaction item object
    """
    output = {"txn_type": crypto_delete_allowance.txn_type}

    return CryptoDeleteAllowanceParsed(**output)


@validate_arguments()
def parseTokenFeeScheduleUpdate(
    token_fee_schedule_update: TokenFeeScheduleUpdate,
) -> TokenFeeScheduleUpdateParsed:
    """
    Parses token fee schedule update type from the transaction item

    :param transaction item: The Hedera transaction item

    :returns: Dictionary of token fee schedule update type in the transaction item object
    """
    output = {"txn_type": token_fee_schedule_update.txn_type}

    return TokenFeeScheduleUpdateParsed(**output)


@validate_arguments()
def parseNodeStakeUpdate(
    node_stake_update: NodeStakeUpdate,
) -> NodeStakeUpdateParsed:
    """
    Parses node stake update update type from the transaction item

    :param transaction item: The Hedera transaction item

    :returns: Dictionary of node stake update schedule update type in the transaction item object
    """
    output = {
        "txn_type": node_stake_update.txn_type,
        "node_stake_max_stake": [int(i.max_stake) / 100000000 for i in node_stake_update.node_stake],
        "node_stake_min_stake": [int(i.min_stake) / 100000000 for i in node_stake_update.node_stake],
        "node_stake_id": [i.node_id for i in node_stake_update.node_stake],
        "node_stake_account": [f"0.0.{i.node_id+3}" for i in node_stake_update.node_stake],
        "node_stake_reward_rate": [i.reward_rate for i in node_stake_update.node_stake],
        "node_stake_not_rewarded": [i.stake_not_rewarded / 100000000 for i in node_stake_update.node_stake],
        "node_stake_rewarded": [i.stake_rewarded / 100000000 for i in node_stake_update.node_stake],
    }

    return NodeStakeUpdateParsed(**output)


@validate_arguments()
def parseUnknownType(
    unknown_type: UnknownType,
) -> UnknownTypeParsed:
    """
    Parses token creation info from the transaction item

    :param transaction item: The Hedera transaction item

    :returns: Dictionary of token creation info in the transaction item object
    """
    output = {"txn_type": unknown_type.txn_type}

    return UnknownTypeParsed(**output)
