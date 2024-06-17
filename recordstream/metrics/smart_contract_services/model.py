import datetime
from pydantic import BaseModel, Field

class accountNum(BaseModel):
    accountNum: int


class AccountID(BaseModel):
    accountID: accountNum
    amount: int | None = None


class Transfer(BaseModel):
    amount: int
    accountID: accountNum


class ContractID(BaseModel):
    contractNum: str | None = "0"


class LogInfo(BaseModel):
    contractID: ContractID | None = None
    bloom: bytes | None = None
    topic: list[bytes] | None = []
    data: bytes | None = None


class ContractCreateResult(BaseModel):
    contractID: ContractID | None = None
    contractCallResult: bytes | None = None
    bloom: bytes | None = None
    gasUsed:int | None = None
    logInfo: list[LogInfo] | None = None
    createdContractIDs: list[dict] | None = None


class ContractCallResult(BaseModel):
    contractID: ContractID | None = None
    bloom: bytes | None = None
    gasUsed:int | None = None
    logInfo: list[LogInfo] | None = None
    createdContractIDs: list[dict] | None = None

class Txn(BaseModel):
    status: str
    node_id: str = Field(alias="body.nodeAccountID.accountNum")
    transaction_hash: str = Field(alias="record.transactionHash")
    txn_type: str
    processed_timestamp:  datetime.datetime = Field(alias="@processed")
    consensusTimestamp: datetime.datetime
    contractNum: str = Field(None, alias="record.contractID.contractNum")
    gasUsed: int = Field(None, alias="record.gasUsed")
    contract_create_result: ContractCreateResult | None = None
    contract_call_result: ContractCallResult | None = None
    transfer_list: list[AccountID] | None = None
