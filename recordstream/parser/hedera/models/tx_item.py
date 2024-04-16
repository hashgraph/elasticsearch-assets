from typing import Optional

from pydantic import BaseModel, Field


class Timestamp(BaseModel):
    seconds: int
    nanos: Optional[int] = 0


class AccountID(BaseModel):
    accountNum: Optional[str] = "0"


class TransactionID(BaseModel):
    transactionValidStart: Timestamp = Timestamp(seconds=0)
    accountID: AccountID = AccountID(accountNum="0")
    scheduled: bool = False
    nonce: Optional[int] = 0


class TransactionValidDuration(BaseModel):
    seconds: int


class TopicID(BaseModel):
    topicNum: str


class ConsensusSubmitMessage(BaseModel):
    topicID: TopicID
    message: bytes = b""
    txn_type: str = "CONSENSUSSUBMITMESSAGE"


class ConsensusCreateTopic(BaseModel):
    memo: Optional[str]
    txn_type: str = "CONSENSUSCREATETOPIC"


class ConsensusDeleteTopic(BaseModel):
    topicID: TopicID
    txn_type: str = "CONSENSUSDELETETOPIC"


class ConsensusUpdateTopic(BaseModel):
    topicID: TopicID
    txn_type: str = "CONSENSUSUPDATETOPIC"


class Key(BaseModel):
    ed25519: Optional[bytes] = b""
    keyList: Optional[dict] = {}


class AutoRenewPeriod(BaseModel):
    seconds: str


class CryptoCreateAccount(BaseModel):
    key: Key = Key(ed25519=b"")
    sendRecordThreshold: Optional[str] = "0"
    receiveRecordThreshold: Optional[str] = "0"
    autoRenewPeriod: AutoRenewPeriod = AutoRenewPeriod(seconds=0)
    txn_type: str = "CRYPTOCREATEACCOUNT"


class CryptoUpdateAccount(BaseModel):
    accountIDToUpdate: AccountID = AccountID(accountNum="0")
    key: Key = Key(ed25519=b"")
    txn_type: str = "CRYPTOUPDATEACCOUNT"


class CryptoDelete(BaseModel):
    deleteAccountID: AccountID = AccountID(accountNum="0")
    txn_type: str = "CRYPTODELETE"


class Transfers(BaseModel):
    accountAmounts: Optional[list]


class CryptoTransfer(BaseModel):
    transfers: Optional[Transfers]
    txn_type: str = "CRYPTOTRANSFER"


class TokenAssociate(BaseModel):
    account: AccountID = AccountID(accountNum="0")
    tokens: list
    txn_type: str = "TOKENASSOCIATE"


class TokenDissociate(BaseModel):
    account: AccountID = AccountID(accountNum="0")
    tokens: list
    txn_type: str = "TOKENDISSOCIATE"


class FileID(BaseModel):
    fileNum: str = "0"


class FileDelete(BaseModel):
    fileID: FileID
    txn_type: str = "FILEDELETE"


class FileUpdate(BaseModel):
    fileID: FileID
    txn_type: str = "FILEUPDATE"


class FileCreate(BaseModel):
    txn_type: str = "FILECREATE"


class FileAppend(BaseModel):
    fileID: FileID
    txn_type: str = "FILEAPPEND"


class ScheduleID(BaseModel):
    scheduleNum: str


class ScheduleCreate(BaseModel):
    scheduledTransactionBody: dict
    txn_type: str = "SCHEDULECREATE"


class ScheduleSign(BaseModel):
    scheduleID: ScheduleID
    txn_type: str = "SCHEDULESIGN"


class ScheduleDelete(BaseModel):
    scheduleID: ScheduleID
    txn_type: str = "SCHEDULEDELETE"


class TokenID(BaseModel):
    tokenNum: str


class TokenGrantKyc(BaseModel):
    token: TokenID
    account: AccountID
    txn_type: str = "TOKENGRANTKYC"


class TokenRevokeKyc(BaseModel):
    token: TokenID
    account: AccountID
    txn_type: str = "TOKENREVOKEKYC"


class TokenFreeze(BaseModel):
    token: TokenID
    account: AccountID
    txn_type: str = "TOKENFREEZE"


class TokenUnfreeze(BaseModel):
    token: TokenID
    account: AccountID
    txn_type: str = "TOKENUNFREEZE"


class TokenPause(BaseModel):
    token: TokenID
    txn_type: str = "TOKENPAUSE"


class TokenUnpause(BaseModel):
    token: TokenID
    txn_type: str = "TOKENUNPAUSE"


class TokenDeletion(BaseModel):
    token: TokenID
    txn_type: str = "TOKENDELETION"


class TokenMint(BaseModel):
    token: TokenID
    amount: Optional[int] = 0
    metadata: Optional[list[bytes]] = []
    txn_type: str = "TOKENMINT"


class TokenWipe(BaseModel):
    account: AccountID = AccountID(accountNum="0")
    token: TokenID
    amount: Optional[int] = 0
    serialNumbers: Optional[list]
    txn_type: str = "TOKENWIPE"


class TokenBurn(BaseModel):
    account: AccountID = AccountID(accountNum="0")
    token: TokenID
    amount: int = 0
    serialNumbers: Optional[list]
    txn_type: str = "TOKENBURN"


class TokenCreation(BaseModel):
    name: str
    symbol: str
    tokenType: Optional[int] = 0
    decimals: Optional[int] = 0
    treasury: AccountID = AccountID(accountNum="0")
    adminKey: Key = Key(ed25519=b"")
    kycKey: Key = Key(ed25519=b"")
    wipeKey: Key = Key(ed25519=b"")
    supplyKey: Key = Key(ed25519=b"")
    freezeKey: Key = Key(ed25519=b"")
    freezeDefault: Optional[bool]
    autoRenewAccount: AccountID = AccountID(accountNum="0")
    autoRenewPeriod: Timestamp = Timestamp(seconds=0)
    memo: Optional[str] = ""
    supplyType: Optional[int] = 0
    maxSupply: Optional[int] = 0
    initialSupply: Optional[int] = 0
    txn_type: str = "TOKENCREATION"
    # TODO: Need to classify into NFT and Token Creations


class TokenUpdate(BaseModel):
    name: Optional[str] = ""
    symbol: Optional[str] = ""
    tokenType: Optional[int] = 0
    treasury: AccountID = AccountID(accountNum="0")
    adminKey: Key = Key(ed25519=b"")
    kycKey: Key = Key(ed25519=b"")
    wipeKey: Key = Key(ed25519=b"")
    supplyKey: Key = Key(ed25519=b"")
    freezeKey: Key = Key(ed25519=b"")
    autoRenewAccount: AccountID = AccountID(accountNum="0")
    memo: Optional[str] = ""
    txn_type: str = "TOKENUPDATE"
    # TODO: Need to classify into NFT and Token Creations


class ContractID(BaseModel):
    contractNum: str = ""


class ContractCreateInstance(BaseModel):
    fileID: FileID = FileID(fileNum="0")
    gas: Optional[int] = 0
    autoRenewPeriod: Optional[Timestamp]
    adminKey: Optional[dict] = {}
    initialBalance: Optional[int] = 0
    proxyAccountID: Optional[dict] = {}
    constructorParameters: Optional[bytes] = b""
    memo: Optional[str] = ""
    txn_type: str = "CONTRACTCREATEINSTANCE"


class ContractUpdateInstance(BaseModel):
    contractID: ContractID
    txn_type: str = "CONTRACTUPDATEINSTANCE"


class ContractCall(BaseModel):
    contractID: ContractID
    gas: int
    amount: Optional[int] = 0
    functionParameters: Optional[bytes] = b""
    txn_type: str = "CONTRACTCALL"


class ContractDeleteInstance(BaseModel):
    contractID: ContractID
    txn_type: str = "CONTRACTDELETE"


class UnknownType(BaseModel):
    txn_type: str = "OTHER"


class EthereumTransaction(BaseModel):
    ethereum_data: Optional[bytes] = b""
    call_data: Optional[str] = ""
    max_gas_allowance: Optional[int] = 0
    txn_type: str = "ETHEREUMTRANSACTION"


class CryptoApproveAllowance(BaseModel):
    txn_type: str = "CRYPTOAPPROVEALLOWANCE"


class CryptoDeleteAllowance(BaseModel):
    txn_type: str = "CRYPTODELETEALLOWANCE"


class TokenFeeScheduleUpdate(BaseModel):
    txn_type: str = "TOKENFEESCHEDULEUPDATE"


class NodeStakeMessage(BaseModel):
    max_stake: Optional[int] = 0
    min_stake: Optional[int] = 0
    reward_rate: Optional[int] = 0
    stake_not_rewarded: Optional[int] = 0
    stake_rewarded: Optional[int] = 0
    node_id: Optional[int] = 0


class NodeStakeUpdate(BaseModel):
    end_of_staking_period: Optional[Timestamp]
    node_stake: list[NodeStakeMessage]
    txn_type: str = "NODESTAKEUPDATE"


class TransactionItem(BaseModel):
    transactionID: TransactionID
    transactionValidDuration: TransactionValidDuration = TransactionValidDuration(seconds=0)
    nodeAccountID: AccountID = AccountID(accountNum="0")
    accountID: AccountID = AccountID(accountNum="0")
    transactionFee: Optional[int] = 0
    memo: Optional[str] = ""
    consensusSubmitMessage: Optional[ConsensusSubmitMessage]
    consensusCreateTopic: Optional[ConsensusCreateTopic]
    consensusUpdateTopic: Optional[ConsensusUpdateTopic]
    consensusDeleteTopic: Optional[ConsensusDeleteTopic]
    cryptoTransfer: Optional[CryptoTransfer]
    cryptoCreateAccount: Optional[CryptoCreateAccount]
    cryptoUpdateAccount: Optional[CryptoUpdateAccount]
    cryptoDelete: Optional[CryptoDelete]
    fileUpdate: Optional[FileUpdate]
    fileAppend: Optional[FileAppend]
    fileCreate: Optional[FileCreate]
    fileDelete: Optional[FileDelete]
    contractCreateInstance: Optional[ContractCreateInstance]
    contractUpdateInstance: Optional[ContractUpdateInstance]
    contractCall: Optional[ContractCall]
    contractDeleteInstance: Optional[ContractDeleteInstance]
    scheduleSign: Optional[ScheduleSign]
    scheduleCreate: Optional[ScheduleCreate]
    scheduleDelete: Optional[ScheduleDelete]
    tokenGrantKyc: Optional[TokenGrantKyc]
    tokenDeletion: Optional[TokenDeletion]
    tokenRevokeKyc: Optional[TokenRevokeKyc]
    tokenMint: Optional[TokenMint]
    tokenCreation: Optional[TokenCreation]
    tokenFreeze: Optional[TokenFreeze]
    tokenUnfreeze: Optional[TokenUnfreeze]
    tokenWipe: Optional[TokenWipe]
    tokenAssociate: Optional[TokenAssociate]
    tokenUpdate: Optional[TokenUpdate]
    tokenBurn: Optional[TokenBurn]
    tokenDissociate: Optional[TokenDissociate]
    tokenPause: Optional[TokenPause]
    tokenUnpause: Optional[TokenUnpause]
    ethereumTransaction: Optional[EthereumTransaction]
    cryptoApproveAllowance: Optional[CryptoApproveAllowance]
    cryptoDeleteAllowance: Optional[CryptoDeleteAllowance]
    token_fee_schedule_update: Optional[TokenFeeScheduleUpdate]
    node_stake_update: Optional[NodeStakeUpdate]


class CommonParsed(BaseModel):
    body_transactionValidStart_seconds: int = Field(alias="body.transactionValidStart.seconds")
    body_transactionValidStart_nanos: Optional[int] = Field(alias="body.transactionValidStart.nanos")
    body_accountID_accountNum: Optional[str] = Field(alias="body.accountID.accountNum")
    body_nodeAccountID_accountNum: Optional[str] = Field(alias="body.nodeAccountID.accountNum")
    scheduled: bool = False
    body_transactionFee: Optional[int] = Field(alias="body.transactionFee")
    body_transactionValidDuration_seconds: Optional[int] = Field(alias="body.transactionValidDuration.seconds")
    nonce: int = 0


class ConsensusSubmitMessageParsed(BaseModel):
    consensus_submit_topicID: Optional[int]
    consensus_submit_message: Optional[str]
    consensus_submit_message_bytes: Optional[int]
    txn_type: str


class ConsensusCreateTopicParsed(BaseModel):
    consensus_create_memo: Optional[str]
    txn_type: str


class ConsensusUpdateTopicParsed(BaseModel):
    consensus_update_topicID: Optional[int]
    txn_type: str


class ConsensusDeleteTopicParsed(BaseModel):
    consensus_delete_topicID: Optional[int]
    txn_type: str


class UnknownTypeParsed(BaseModel):
    txn_type: str


class CryptoTransferParsed(BaseModel):
    transferList: Optional[dict]
    txn_type: str


class CryptoCreateAccountParsed(BaseModel):
    body_key: Optional[str] = Field(alias="body.key")
    body_sendRecordThreshold: Optional[str] = Field(alias="body.sendRecordThreshold")
    body_receiveRecordThreshold: Optional[str] = Field(alias="body.receiveRecordThreshold")
    body_autoRenewPeriod: Optional[str] = Field(alias="body.autoRenewPeriod")
    txn_type: str


class CryptoUpdateAccountParsed(BaseModel):
    updated_account: str
    body_key: Optional[str] = Field(alias="body.key")
    txn_type: str


class CryptoDeleteParsed(BaseModel):
    deleted_account: str
    txn_type: str


class FileUpdateParsed(BaseModel):
    file_id: Optional[str]
    txn_type: str


class FileAppendParsed(BaseModel):
    file_id: Optional[str]
    txn_type: str


class FileCreateParsed(BaseModel):
    txn_type: str


class FileDeleteParsed(BaseModel):
    file_id: Optional[str]
    txn_type: str


class ScheduleCreateParsed(BaseModel):
    schedule_txn_body: dict = {}
    txn_type: str


class ScheduleSignParsed(BaseModel):
    schedule_id: Optional[str]
    txn_type: str


class ScheduleDeleteParsed(BaseModel):
    schedule_id: Optional[str]
    txn_type: str


class TokenAssociateParsed(BaseModel):
    token_account_number: Optional[str] = "0"
    tokenList: Optional[list]
    txn_type: str


class TokenDissociateParsed(BaseModel):
    token_account_number: Optional[str] = "0"
    tokenList: Optional[list]
    txn_type: str


class TokenWipeParsed(BaseModel):
    token_number: str
    token_account_number: Optional[str] = "0"
    token_wipe_amount: Optional[int]
    nft_serial_numbers: Optional[list]
    txn_type: str


class TokenGrantKycParsed(BaseModel):
    token_number: str
    token_account_number: Optional[str] = "0"
    txn_type: str


class TokenRevokeKycParsed(BaseModel):
    token_number: str
    token_account_number: Optional[str] = "0"
    txn_type: str


class TokenFreezeParsed(BaseModel):
    token_number: str
    token_account_number: Optional[str] = "0"
    txn_type: str


class TokenUnfreezeParsed(BaseModel):
    token_number: str
    token_account_number: Optional[str] = "0"
    txn_type: str


class TokenMintParsed(BaseModel):
    token_number: str
    token_mint_amount: Optional[int]
    token_mint_metadata: list = []
    txn_type: str


class TokenPauseParsed(BaseModel):
    token_number: str
    txn_type: str


class TokenUnpauseParsed(BaseModel):
    token_number: str
    txn_type: str


class TokenDeletionParsed(BaseModel):
    token_number: str
    txn_type: str


class TokenBurnParsed(BaseModel):
    token_account_number: Optional[str] = "0"
    token_number: str
    token_burn_amount: int = 0
    nft_serial_numbers: Optional[list]
    txn_type: str


class TokenCreationParsed(BaseModel):
    token_name: str
    token_symbol: str
    token_type: Optional[int]
    token_decimals: Optional[int]
    token_account_number: Optional[str] = "0"
    token_admin_key: str
    token_wipe_key: str
    token_kyc_key: str
    token_supply_key: str
    token_freeze_key: str
    freeze_default: bool = False
    auto_renew_account: Optional[str]
    auto_renew_period_seconds: Optional[int]
    auto_renew_period_nanos: Optional[int]
    memo: Optional[str]
    supply_type: Optional[int]
    max_supply: Optional[int]
    token_initial_supply: Optional[int]
    txn_type: str
    # TO DO Txn type based on token type


class TokenUpdateParsed(BaseModel):
    token_name: str = ""
    token_symbol: str = ""
    token_type: Optional[int] = None
    token_account_number: Optional[str] = "0"
    token_admin_key: str
    token_wipe_key: str
    token_kyc_key: str
    token_supply_key: str
    token_freeze_key: str
    auto_renew_account: Optional[str]
    memo: Optional[str]
    txn_type: str
    # TO DO Txn type based on token type


class ContractCreateInstanceParsed(BaseModel):
    file_id: Optional[str]
    body_gasUsed: int = Field(alias="body.gasUsed")
    auto_renew_period_seconds: Optional[int] = None
    auto_renew_period_nanos: Optional[int] = None
    admin_key: dict = {}
    initial_balance: Optional[int] = None
    proxy_account_id: dict = {}
    memo: Optional[str]
    txn_type: str


class ContractUpdateInstanceParsed(BaseModel):
    body_contractID: str = Field(alias="body.contractID")
    txn_type: str


class ContractCallParsed(BaseModel):
    body_contractID: str = Field(alias="body.contractID")
    body_gasUsed: int = Field(alias="body.gasUsed")
    amount: int = 0
    txn_type: str


class ContractDeleteInstanceParsed(BaseModel):
    body_contractID: str = Field(alias="body.contractID")
    txn_type: str


class EthereumTransactionParsed(BaseModel):
    ethereum_data: str
    call_data: Optional[str]
    max_gas_allowance: Optional[int]
    txn_type: str


class CryptoApproveAllowanceParsed(BaseModel):
    txn_type: str


class CryptoDeleteAllowanceParsed(BaseModel):
    txn_type: str


class TokenFeeScheduleUpdateParsed(BaseModel):
    txn_type: str


class NodeStakeUpdateParsed(BaseModel):
    node_stake_max_stake: list[int]
    node_stake_min_stake: list[int]
    node_stake_id: list[int]
    node_stake_account: list[str]
    node_stake_reward_rate: list[int]
    node_stake_not_rewarded: list[int]
    node_stake_rewarded: list[int]
    txn_type: str
