import datetime
from pydantic import BaseModel, Field


class accountNum(BaseModel):
    accountNum: int

class AccountID(BaseModel):
    accountID: accountNum
    amount: int | None = None

class Txn(BaseModel):
    status: str
    transaction_hash: str = Field(alias="record.transactionHash")
    txn_type: str
    processed_timestamp:  datetime.datetime = Field(alias="@processed")
    consensusTimestamp: datetime.datetime
    node_id: str = Field(alias="body.nodeAccountID.accountNum")

class TxnWithTransfer(BaseModel):
    status: str
    transaction_hash: str = Field(alias="record.transactionHash")
    txn_type: str
    processed_timestamp:  datetime.datetime = Field(alias="@processed")
    consensusTimestamp: datetime.datetime
    node_id: str = Field(alias="body.nodeAccountID.accountNum")
    payer: str = Field(alias="record.accountID.accountNum")
    transaction_fee: int = Field(alias="record.transactionFee")
    transfer_list: list[AccountID] | None = None