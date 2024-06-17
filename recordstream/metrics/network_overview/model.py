import datetime
from pydantic import BaseModel, Field

class Txn(BaseModel):
    status: str
    transaction_hash: str = Field(alias="record.transactionHash")
    txn_type: str
    processed_timestamp:  datetime.datetime = Field(alias="@processed")
    consensusTimestamp: datetime.datetime
    node_id: str = Field(alias="body.nodeAccountID.accountNum")