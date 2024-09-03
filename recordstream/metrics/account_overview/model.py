
import datetime
from pydantic import BaseModel, Field

class AccountNum(BaseModel):
    accountNum: int


class Account(BaseModel):
    accountID: AccountNum
    amount: float


class Txn(BaseModel):
    status: str
    transaction_hash: str = Field(alias="record.transactionHash")
    txn_type: str
    txn_sign_keys: list[str] | None = None
    processed_timestamp:  datetime.datetime = Field(alias="@processed")
    consensusTimestamp: datetime.datetime
    payer: int = Field(alias="record.accountID.accountNum")
    transfer_list: list[Account] | None = None
