from typing import Optional

from pydantic import BaseModel, Field


class Timestamp(BaseModel):
    seconds: int
    nanos: Optional[int] = 0


class AccountID(BaseModel):
    accountNum: Optional[str] = "0"


class TransactionID(BaseModel):
    transactionValidStart: Optional[Timestamp]
    accountID: Optional[AccountID]


class ExpirationTime(BaseModel):
    seconds: Optional[int] = 0


class XRate(BaseModel):
    hbarEquiv: Optional[int] = 0
    centEquiv: Optional[int] = 0
    expirationTime: ExpirationTime = ExpirationTime()


class ExchangeRate(BaseModel):
    currentRate: XRate = XRate()
    nextRate: XRate = XRate()


class ScheduleID(BaseModel):
    scheduleNum: Optional[str] = "0"


class TokenID(BaseModel):
    tokenNum: Optional[str] = "0"


class TopicID(BaseModel):
    topicNum: Optional[str] = "0"


class ContractID(BaseModel):
    contractNum: Optional[str] = "0"


class FileID(BaseModel):
    fileNum: Optional[str] = "0"


class Receipt(BaseModel):
    status: str
    exchangeRate: ExchangeRate = ExchangeRate()
    topicSequenceNumber: Optional[int] = 0
    topicRunningHash: Optional[bytes] = b""
    topicRunningHashVersion: Optional[int] = 0
    accountID: AccountID = AccountID(accountNum="0")
    serialNumbers: list = []
    scheduleID: ScheduleID = ScheduleID(scheduleNum="0")
    tokenID: TokenID = TokenID(tokenNum="0")
    topicID: TopicID = TopicID(topicNum="0")
    fileID: FileID = FileID(fileNum="0")


class TransferList(BaseModel):
    accountAmounts: Optional[list]


class TokenTransferLists(BaseModel):
    token: TokenID = TokenID(tokenNum="0")
    transfers: Optional[list]
    nftTransfers: Optional[list]


class LogInfo(BaseModel):
    contractID: Optional[ContractID]
    bloom: Optional[bytes] = b""
    topic: list[Optional[bytes]]
    data: Optional[bytes] = b""


class ContractCreateResult(BaseModel):
    contractID: Optional[ContractID]
    contractCallResult: Optional[bytes] = b""
    bloom: Optional[bytes] = b""
    gasUsed: Optional[int] = 0
    logInfo: Optional[list[LogInfo]]
    createdContractIDs: Optional[list[dict]]


class ContractCallResult(BaseModel):
    contractID: Optional[ContractID]
    bloom: Optional[bytes] = b""
    gasUsed: Optional[int] = 0
    logInfo: Optional[list[LogInfo]]
    createdContractIDs: Optional[list[dict]]


class TransactionRecord(BaseModel):
    receipt: Optional[Receipt]
    transactionHash: Optional[bytes] = b""
    consensusTimestamp: Timestamp = Timestamp(seconds=0)
    transactionID: Optional[TransactionID]
    transactionFee: Optional[int] = 0
    memo: Optional[str] = ""
    transferList: TransferList = TransferList(accountAmounts=[])
    tokenTransferLists: Optional[list[TokenTransferLists]]
    contractCreateResult: Optional[ContractCreateResult] = {}
    contractCallResult: Optional[ContractCallResult]

class TxRecordParsed(BaseModel):
    status: str
    currentRate_hbarEquiv: Optional[int] = Field(alias="currentRate.hbarEquiv")
    currentRate_centEquiv: Optional[int] = Field(alias="currentRate.centEquiv")
    currentRate_expirationTime_seconds: Optional[int] = Field(alias="currentRate.expirationTime.seconds")
    nextRate_hbarEquiv: Optional[int] = Field(alias="nextRate.hbarEquiv")
    nextRate_centEquiv: Optional[int] = Field(alias="nextRate.centEquiv")
    nextRate_expirationTime_seconds: Optional[int] = Field(alias="nextRate.expirationTime.seconds")
    record_transactionHash: str = Field(alias="record.transactionHash")
    record_consensusTimestamp_seconds: int = Field(alias="record.consensusTimestamp.seconds")
    record_consensusTimestamp_nanos: Optional[int] = Field(alias="record.consensusTimestamp.nanos")
    record_transactionValidStart_seconds: int = Field(alias="record.transactionValidStart.seconds")
    record_transactionValidStart_nanos: Optional[int] = Field(alias="record.transactionValidStart.nanos")
    record_accountID_accountNum: str = Field(alias="record.accountID.accountNum")
    record_transactionFee: Optional[int] = Field(alias="record.transactionFee")
    record_memo: Optional[str] = Field(alias="record.memo")
    topic_sequence_number: Optional[int]
    topic_running_hash: Optional[bytes]
    topic_running_hash_version: Optional[int]
    created_account: Optional[str]
    schedule_id: Optional[str]
    token_number: Optional[str]
    file_id: Optional[str]
    consensus_create_topicID: Optional[str]
    transfer_list: Optional[list]
    token_transfer_list: Optional[list]
    contract_create_result: Optional[dict]
    contract_call_result: Optional[dict]
