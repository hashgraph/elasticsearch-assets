
import datetime
from pydantic import BaseModel, Field

class accountNum(BaseModel):
    accountNum: int


class AccountID(BaseModel):
    accountID: accountNum
    amount: int | None = None


class Token(BaseModel):
    tokenNum: str


class Transfer(BaseModel):
    amount: int
    accountID: accountNum


class NftTransfer(BaseModel):
    serialNumber: int
    senderAccountID: accountNum
    receiverAccountID: accountNum


class TokenTransferList(BaseModel):
    token: Token
    transfers: list[Transfer] | None = None
    nftTransfers: list[NftTransfer] | None = None


class Txn(BaseModel):
    status: str
    node_id: str = Field(alias="body.nodeAccountID.accountNum")
    transaction_hash: str = Field(alias="record.transactionHash")
    txn_type: str
    processed_timestamp:  datetime.datetime = Field(alias="@processed")
    consensusTimestamp: datetime.datetime
    contractNum: int = Field(None, alias="record.contractID.contractNum")   # contractNum is not present in all records
    token_transfer_list: list[TokenTransferList] | None = None
    transfer_list: list[AccountID] | None = None
    token_number: str | None = None


class Token(BaseModel):
    name: str
    symbol: str
    token_id: str
    type: str