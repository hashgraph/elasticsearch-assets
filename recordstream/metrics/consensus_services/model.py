
import datetime
from pydantic import BaseModel, Field


class Txn(BaseModel):
    status: str
    node_id: str = Field(alias="body.nodeAccountID.accountNum")
    transaction_hash: str = Field(alias="record.transactionHash")
    txn_type: str
    processed_timestamp:  datetime.datetime = Field(alias="@processed")
    consensusTimestamp: datetime.datetime
    consensus_create_topicID: int | None = None
    consensus_submit_topicID: int | None = None
    consensus_update_topicID: int | None = None
    consensus_delete_topicID: int | None = None
    consensus_submit_message_bytes: int | None = None