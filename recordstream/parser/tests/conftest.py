import pytest


@pytest.fixture
def tx_item_common_in():
    return {
        "transactionID": {
            "transactionValidStart": {
                "seconds": 1665619446,
                "nanos": 943094539,
            },
            "accountID": {"accountNum": 48461821},
        },
        "nodeAccountID": {"accountNum": 5},
        "transactionFee": 200000000,
        "transactionValidDuration": {"seconds": 120},
        "memo": "VC creation message",
    }


@pytest.fixture
def tx_item_common_out():
    return {
        "body.transactionValidStart.seconds": 1665619446,
        "body.transactionValidStart.nanos": 943094539,
        "body.accountID.accountNum": "48461821",
        "body.nodeAccountID.accountNum": "5",
        "scheduled": False,
        "body.transactionFee": 200000000,
        "body.transactionValidDuration.seconds": 120,
        "nonce": 0,
    }


@pytest.fixture
def tx_item_consensus_submit_message_in(tx_item_common_in):
    return {
        **tx_item_common_in,
        **{
            "consensusSubmitMessage": {
                "topicID": {"topicNum": 48461813},
                "message": b"message",
            }
        },
    }


@pytest.fixture
def tx_item_consensus_submit_message_out(tx_item_common_out):
    return {
        **tx_item_common_out,
        **{
            "consensus_submit_topicID": 48461813,
            "consensus_submit_message": "b'message'",
            "consensus_submit_message_bytes": 7,
            "txn_type": "CONSENSUSSUBMITMESSAGE",
        },
    }


@pytest.fixture
def tx_item_consensus_create_topic_in(tx_item_common_in):
    return {**tx_item_common_in, **{"consensusCreateTopic": {"memo": "memo"}}}


@pytest.fixture
def tx_item_consensus_create_topic_out(tx_item_common_out):
    return {
        **tx_item_common_out,
        **{
            "consensus_create_memo": "memo",
            "txn_type": "CONSENSUSCREATETOPIC",
        },
    }


@pytest.fixture
def tx_item_consensus_update_topic_in(tx_item_common_in):
    return {
        **tx_item_common_in,
        **{"consensusUpdateTopic": {"topicID": {"topicNum": 1}}},
    }


@pytest.fixture
def tx_item_consensus_update_topic_out(tx_item_common_out):
    return {
        **tx_item_common_out,
        **{"consensus_update_topicID": 1, "txn_type": "CONSENSUSUPDATETOPIC"},
    }


@pytest.fixture
def tx_item_crypto_transfer_in(tx_item_common_in):
    return {
        **tx_item_common_in,
        **{
            "cryptoTransfer": {
                "transfers": {
                    "accountAmounts": [
                        {"accountID": {"accountNum": 1}, "amount": -1},
                        {"accountID": {"accountNum": 0}, "amount": 1},
                    ]
                }
            }
        },
    }


@pytest.fixture
def tx_item_crypto_transfer_out(tx_item_common_out):
    return {
        **tx_item_common_out,
        **{
            "body.accountNum.1": 1,
            "body.amount.1": -1,
            "body.accountNum.2": 0,
            "body.amount.2": 1,
            "txn_type": "CRYPTOTRANSFER",
        },
    }


@pytest.fixture
def tx_item_crypto_create_account_in(tx_item_common_in):
    return {
        **tx_item_common_in,
        **{
            "cryptoCreateAccount": {
                "key": {"ed25519": b"key"},
                "sendRecordThreshold": 0,
                "receiveRecordThreshold": 0,
                "autoRenewPeriod": {"seconds": 0},
            }
        },
    }


@pytest.fixture
def tx_item_crypto_create_account_out(tx_item_common_out):
    return {
        **tx_item_common_out,
        **{
            "body.key": "b'key'",
            "body.sendRecordThreshold": "0",
            "body.receiveRecordThreshold": "0",
            "body.autoRenewPeriod": "0",
            "txn_type": "CRYPTOCREATEACCOUNT",
        },
    }


@pytest.fixture
def tx_item_crypto_update_account_in(tx_item_common_in):
    return {
        **tx_item_common_in,
        **{
            "cryptoUpdateAccount": {
                "key": {"ed25519": b"key"},
                "accountIDToUpdate": {"accountID": {"accountNum": "0"}},
            }
        },
    }


@pytest.fixture
def tx_item_crypto_update_account_out(tx_item_common_out):
    return {
        **tx_item_common_out,
        **{
            "body.key": "b'key'",
            "updated_account": "0",
            "txn_type": "CRYPTOUPDATEACCOUNT",
        },
    }


@pytest.fixture
def tx_item_crypto_delete_in(tx_item_common_in):
    return {
        **tx_item_common_in,
        **{"cryptoDelete": {"deleteAccountID": {"accountID": {"accountNum": "0"}}}},
    }


@pytest.fixture
def tx_item_crypto_delete_out(tx_item_common_out):
    return {
        **tx_item_common_out,
        **{"deleted_account": "0", "txn_type": "CRYPTODELETE"},
    }


@pytest.fixture
def tx_item_file_update_in(tx_item_common_in):
    return {
        **tx_item_common_in,
        **{"fileUpdate": {"fileID": {"fileNum": "0"}}},
    }


@pytest.fixture
def tx_item_file_update_out(tx_item_common_out):
    return {**tx_item_common_out, **{"file_id": "0", "txn_type": "FILEUPDATE"}}


@pytest.fixture
def tx_item_file_delete_in(tx_item_common_in):
    return {
        **tx_item_common_in,
        **{"fileDelete": {"fileID": {"fileNum": "0"}}},
    }


@pytest.fixture
def tx_item_file_delete_out(tx_item_common_out):
    return {**tx_item_common_out, **{"file_id": "0", "txn_type": "FILEDELETE"}}


@pytest.fixture
def tx_item_file_append_in(tx_item_common_in):
    return {
        **tx_item_common_in,
        **{"fileAppend": {"fileID": {"fileNum": "0"}}},
    }


@pytest.fixture
def tx_item_file_append_out(tx_item_common_out):
    return {**tx_item_common_out, **{"file_id": "0", "txn_type": "FILEAPPEND"}}


@pytest.fixture
def tx_item_file_create_in(tx_item_common_in):
    return {
        **tx_item_common_in,
        **{
            "fileCreate": {},
        },
    }


@pytest.fixture
def tx_item_file_create_out(tx_item_common_out):
    return {**tx_item_common_out, **{"txn_type": "FILECREATE"}}


@pytest.fixture
def tx_item_schedule_create_in(tx_item_common_in):
    return {
        **tx_item_common_in,
        **{"scheduleCreate": {"scheduledTransactionBody": {}}},
    }


@pytest.fixture
def tx_item_schedule_create_out(tx_item_common_out):
    return {
        **tx_item_common_out,
        **{"schedule_txn_body": {}, "txn_type": "SCHEDULECREATE"},
    }


@pytest.fixture
def tx_item_schedule_sign_in(tx_item_common_in):
    return {
        **tx_item_common_in,
        **{"scheduleSign": {"scheduleID": {"scheduleNum": "0"}}},
    }


@pytest.fixture
def tx_item_schedule_sign_out(tx_item_common_out):
    return {
        **tx_item_common_out,
        **{"schedule_id": "0", "txn_type": "SCHEDULESIGN"},
    }


@pytest.fixture
def tx_item_schedule_delete_in(tx_item_common_in):
    return {
        **tx_item_common_in,
        **{"scheduleDelete": {"scheduleID": {"scheduleNum": "0"}}},
    }


@pytest.fixture
def tx_item_schedule_delete_out(tx_item_common_out):
    return {
        **tx_item_common_out,
        **{"schedule_id": "0", "txn_type": "SCHEDULEDELETE"},
    }


@pytest.fixture
def tx_item_token_associate_single_in(tx_item_common_in):
    return {
        **tx_item_common_in,
        **{
            "tokenAssociate": {
                "account": {"accountNum": "0"},
                "tokens": [{"tokenNum": "0"}],
            }
        },
    }


@pytest.fixture
def tx_item_token_associate_single_out(tx_item_common_out):
    return {
        **tx_item_common_out,
        **{
            "token_account_number": "0",
            "token_number": "0",
            "txn_type": "TOKENASSOCIATE",
        },
    }


@pytest.fixture
def tx_item_token_associate_multiple_in(tx_item_common_in):
    return {
        **tx_item_common_in,
        **{
            "tokenAssociate": {
                "account": {"accountNum": "0"},
                "tokens": [{"tokenNum": "0"}, {"tokenNum": "1"}],
            }
        },
    }


@pytest.fixture
def tx_item_token_associate_multiple_out(tx_item_common_out):
    return {
        **tx_item_common_out,
        **{
            "token_account_number": "0",
            "token_number": "0",
            "token_number2": "1",
            "txn_type": "TOKENASSOCIATE",
        },
    }


@pytest.fixture
def tx_item_token_dissociate_in(tx_item_common_in):
    return {
        **tx_item_common_in,
        **{
            "tokenDissociate": {
                "account": {"accountNum": "0"},
                "tokens": [{"tokenNum": "0"}],
            }
        },
    }


@pytest.fixture
def tx_item_token_dissociate_out(tx_item_common_out):
    return {
        **tx_item_common_out,
        **{
            "token_account_number": "0",
            "token_number": "0",
            "txn_type": "TOKENDISSOCIATE",
        },
    }


@pytest.fixture
def tx_item_token_revoke_kyc_in(tx_item_common_in):
    return {
        **tx_item_common_in,
        **{
            "tokenRevokeKyc": {
                "token": {"tokenNum": 0},
                "account": {"accountNum": "0"},
                "tokens": [{"tokenNum": "0"}],
            }
        },
    }


@pytest.fixture
def tx_item_token_revoke_kyc_out(tx_item_common_out):
    return {
        **tx_item_common_out,
        **{
            "token_account_number": "0",
            "token_number": "0",
            "txn_type": "TOKENREVOKEKYC",
        },
    }


@pytest.fixture
def tx_item_token_grant_kyc_in(tx_item_common_in):
    return {
        **tx_item_common_in,
        **{
            "tokenGrantKyc": {
                "token": {"tokenNum": 0},
                "account": {"accountNum": "0"},
                "tokens": [{"tokenNum": "0"}],
            }
        },
    }


@pytest.fixture
def tx_item_token_grant_kyc_out(tx_item_common_out):
    return {
        **tx_item_common_out,
        **{
            "token_account_number": "0",
            "token_number": "0",
            "txn_type": "TOKENGRANTKYC",
        },
    }


@pytest.fixture
def tx_item_token_freeze_in(tx_item_common_in):
    return {
        **tx_item_common_in,
        **{
            "tokenFreeze": {
                "token": {"tokenNum": 0},
                "account": {"accountNum": "0"},
                "tokens": [{"tokenNum": "0"}],
            }
        },
    }


@pytest.fixture
def tx_item_token_freeze_out(tx_item_common_out):
    return {
        **tx_item_common_out,
        **{
            "token_account_number": "0",
            "token_number": "0",
            "txn_type": "TOKENFREEZE",
        },
    }


@pytest.fixture
def tx_item_token_unfreeze_in(tx_item_common_in):
    return {
        **tx_item_common_in,
        **{
            "tokenUnfreeze": {
                "token": {"tokenNum": 0},
                "account": {"accountNum": "0"},
                "tokens": [{"tokenNum": "0"}],
            }
        },
    }


@pytest.fixture
def tx_item_token_unfreeze_out(tx_item_common_out):
    return {
        **tx_item_common_out,
        **{
            "token_account_number": "0",
            "token_number": "0",
            "txn_type": "TOKENUNFREEZE",
        },
    }


@pytest.fixture
def tx_item_token_pause_in(tx_item_common_in):
    return {
        **tx_item_common_in,
        **{
            "tokenPause": {
                "token": {"tokenNum": 0},
                "tokens": [{"tokenNum": "0"}],
            }
        },
    }


@pytest.fixture
def tx_item_token_pause_out(tx_item_common_out):
    return {
        **tx_item_common_out,
        **{"token_number": "0", "txn_type": "TOKENPAUSE"},
    }


@pytest.fixture
def tx_item_token_unpause_in(tx_item_common_in):
    return {
        **tx_item_common_in,
        **{
            "tokenUnpause": {
                "token": {"tokenNum": 0},
                "tokens": [{"tokenNum": "0"}],
            }
        },
    }


@pytest.fixture
def tx_item_token_unpause_out(tx_item_common_out):
    return {
        **tx_item_common_out,
        **{"token_number": "0", "txn_type": "TOKENUNPAUSE"},
    }


@pytest.fixture
def tx_item_token_delete_in(tx_item_common_in):
    return {
        **tx_item_common_in,
        **{
            "tokenDeletion": {
                "token": {"tokenNum": 0},
                "tokens": [{"tokenNum": "0"}],
            }
        },
    }


@pytest.fixture
def tx_item_token_delete_out(tx_item_common_out):
    return {
        **tx_item_common_out,
        **{"token_number": "0", "txn_type": "TOKENDELETION"},
    }


@pytest.fixture
def tx_item_token_mint_in(tx_item_common_in):
    return {
        **tx_item_common_in,
        **{
            "tokenMint": {
                "token": {"tokenNum": 0},
                "amount": 0,
                "metadata": [b"metadata"],
            }
        },
    }


@pytest.fixture
def tx_item_token_mint_out(tx_item_common_out):
    return {
        **tx_item_common_out,
        **{
            "token_number": "0",
            "token_mint_amount": 0,
            "token_mint_metadata": [b"metadata"],
            "txn_type": "TOKENMINT",
        },
    }


@pytest.fixture
def tx_item_token_wipe_in(tx_item_common_in):
    return {
        **tx_item_common_in,
        **{
            "tokenWipe": {
                "token": {"tokenNum": 0},
                "amount": 0,
                "account": {"accountNum": "0"},
            }
        },
    }


@pytest.fixture
def tx_item_token_wipe_out(tx_item_common_out):
    return {
        **tx_item_common_out,
        **{
            "token_number": "0",
            "token_wipe_amount": 0,
            "token_account_number": "0",
            "txn_type": "TOKENWIPE",
        },
    }


@pytest.fixture
def tx_item_token_burn_in(tx_item_common_in):
    return {
        **tx_item_common_in,
        **{
            "tokenBurn": {
                "token": {"tokenNum": 0},
                "amount": 0,
                "account": {"accountNum": "0"},
            }
        },
    }


@pytest.fixture
def tx_item_token_burn_out(tx_item_common_out):
    return {
        **tx_item_common_out,
        **{
            "token_number": "0",
            "token_burn_amount": 0,
            "token_account_number": "0",
            "txn_type": "TOKENBURN",
        },
    }


@pytest.fixture
def tx_item_token_creation_in(tx_item_common_in):
    return {
        **tx_item_common_in,
        **{
            "tokenCreation": {
                "name": "name",
                "symbol": "symbol",
                "tokenType": 1,
                "decimals": 1,
                "treasury": {"accountNum": 0},
                "adminKey": {"ed25519": b"bytes"},
                "kycKey": {"ed25519": b"bytes"},
                "wipeKey": {"ed25519": b"bytes"},
                "supplyKey": {"ed25519": b"bytes"},
                "freezeKey": {"ed25519": b"bytes"},
                "autoRenewAccount": {"accountNum": 0},
                "autoRenewPeriod": {"seconds": 1000, "nanos": 1000},
                "memo": "memo",
                "supplyType": 1,
                "maxSupply": 1000,
                "initialSupply": 1,
            }
        },
    }


@pytest.fixture
def tx_item_token_creation_out(tx_item_common_out):
    return {
        **tx_item_common_out,
        **{
            "token_name": "name",
            "token_symbol": "symbol",
            "token_type": 1,
            "token_decimals": 1,
            "token_account_number": "0",
            "token_admin_key": "b'bytes'",
            "token_kyc_key": "b'bytes'",
            "token_wipe_key": "b'bytes'",
            "token_supply_key": "b'bytes'",
            "token_freeze_key": "b'bytes'",
            "auto_renew_account": "0",
            "freeze_default": False,
            "auto_renew_period_seconds": 1000,
            "auto_renew_period_nanos": 1000,
            "memo": "memo",
            "supply_type": 1,
            "max_supply": 1000,
            "token_initial_supply": 1,
            "txn_type": "TOKENCREATION",
        },
    }


@pytest.fixture
def tx_item_token_update_in(tx_item_common_in):
    return {
        **tx_item_common_in,
        **{
            "tokenUpdate": {
                "name": "name",
                "symbol": "symbol",
                "tokenType": 1,
                "treasury": {"accountNum": 0},
                "adminKey": {"ed25519": b"bytes"},
                "kycKey": {"ed25519": b"bytes"},
                "wipeKey": {"ed25519": b"bytes"},
                "supplyKey": {"ed25519": b"bytes"},
                "freezeKey": {"ed25519": b"bytes"},
                "autoRenewAccount": {"accountNum": 0},
                "memo": "memo",
            }
        },
    }


@pytest.fixture
def tx_item_token_update_out(tx_item_common_out):
    return {
        **tx_item_common_out,
        **{
            "token_name": "name",
            "token_symbol": "symbol",
            "token_type": 1,
            "token_account_number": "0",
            "token_admin_key": "b'bytes'",
            "token_kyc_key": "b'bytes'",
            "token_wipe_key": "b'bytes'",
            "token_supply_key": "b'bytes'",
            "token_freeze_key": "b'bytes'",
            "auto_renew_account": "0",
            "memo": "memo",
            "txn_type": "TOKENUPDATE",
        },
    }


@pytest.fixture
def tx_item_contract_create_in(tx_item_common_in):
    return {
        **tx_item_common_in,
        **{
            "contractCreateInstance": {
                "fileID": {"fileNum": 0},
                "gas": 1000,
                "autoRenewPeriod": {"seconds": 1000, "nanos": 1000},
                "adminKey": {"ed25519": b"bytes"},
                "initialBalance": 1000,
                "proxyAccountId": {},
                "autoRenewAccount": {"accountNum": 0},
                "memo": "memo",
            }
        },
    }


@pytest.fixture
def tx_item_contract_create_out(tx_item_common_out):
    return {
        **tx_item_common_out,
        **{
            "file_id": "0",
            "body.gasUsed": 1000,
            "auto_renew_period_seconds": 1000,
            "auto_renew_period_nanos": 1000,
            "admin_key": {"ed25519": b"bytes"},
            "initial_balance": 1000,
            "proxy_account_id": {},
            "memo": "memo",
            "txn_type": "CONTRACTCREATEINSTANCE",
        },
    }


@pytest.fixture
def tx_item_contract_update_in(tx_item_common_in):
    return {
        **tx_item_common_in,
        **{"contractUpdateInstance": {"contractID": {"contractNum": 0}}},
    }


@pytest.fixture
def tx_item_contract_update_out(tx_item_common_out):
    return {
        **tx_item_common_out,
        **{"body.contractID": "0", "txn_type": "CONTRACTUPDATEINSTANCE"},
    }


@pytest.fixture
def tx_item_contract_call_in(tx_item_common_in):
    return {
        **tx_item_common_in,
        **{
            "contractCall": {
                "contractID": {"contractNum": 0},
                "gas": 1000,
                "amount": 1000,
            }
        },
    }


@pytest.fixture
def tx_item_contract_call_out(tx_item_common_out):
    return {
        **tx_item_common_out,
        **{
            "body.contractID": "0",
            "body.gasUsed": 1000,
            "amount": 1000,
            "txn_type": "CONTRACTCALL",
        },
    }


@pytest.fixture
def tx_item_contract_delete_in(tx_item_common_in):
    return {
        **tx_item_common_in,
        **{"contractDeleteInstance": {"contractID": {"contractNum": 0}}},
    }


@pytest.fixture
def tx_item_contract_delete_out(tx_item_common_out):
    return {
        **tx_item_common_out,
        **{"body.contractID": "0", "txn_type": "CONTRACTDELETE"},
    }


@pytest.fixture
def tx_item_ethereum_transaction_in(tx_item_common_in):
    return {
        **tx_item_common_in,
        **{
            "ethereumTransaction": {
                "ethereum_data": b"ethereum data",
                "call_data": "call data",
                "max_gas_allowance": 1000,
            }
        },
    }


@pytest.fixture
def tx_item_ethereum_transaction_out(tx_item_common_out):
    return {
        **tx_item_common_out,
        **{
            "ethereum_data": "b'ethereum data'",
            "call_data": "call data",
            "max_gas_allowance": 1000,
            "txn_type": "ETHEREUMTRANSACTION",
        },
    }


@pytest.fixture
def tx_item_crypto_approve_allowance_in(tx_item_common_in):
    return {**tx_item_common_in, **{"cryptoApproveAllowance": {}}}


@pytest.fixture
def tx_item_crypto_approve_allowance_out(tx_item_common_out):
    return {**tx_item_common_out, **{"txn_type": "CRYPTOAPPROVEALLOWANCE"}}


@pytest.fixture
def tx_item_crypto_delete_allowance_in(tx_item_common_in):
    return {**tx_item_common_in, **{"cryptoDeleteAllowance": {}}}


@pytest.fixture
def tx_item_crypto_delete_allowance_out(tx_item_common_out):
    return {**tx_item_common_out, **{"txn_type": "CRYPTODELETEALLOWANCE"}}


@pytest.fixture
def tx_item_token_fee_schedule_update_in(tx_item_common_in):
    return {**tx_item_common_in, **{"token_fee_schedule_update": {}}}


@pytest.fixture
def tx_item_token_fee_schedule_update_out(tx_item_common_out):
    return {**tx_item_common_out, **{"txn_type": "TOKENFEESCHEDULEUPDATE"}}


@pytest.fixture
def tx_item_node_stake_update_in(tx_item_common_in):
    return {
        **tx_item_common_in,
        **{
            "node_stake_update": {
                "node_stake": [
                    {
                        "max_stake": 100000000,
                        "min_stake": 0,
                        "node_id": 0,
                        "reward_rate": 1,
                        "stake_not_rewarded": 0,
                        "stake_rewarded": 0,
                    }
                ]
            }
        },
    }


@pytest.fixture
def tx_item_node_stake_update_out(tx_item_common_out):
    return {
        **tx_item_common_out,
        **{
            "txn_type": "NODESTAKEUPDATE",
            "node_stake_max_stake": [1],
            "node_stake_min_stake": [0],
            "node_stake_id": [0],
            "node_stake_account": ["0.0.3"],
            "node_stake_reward_rate": [1],
            "node_stake_not_rewarded": [0],
            "node_stake_rewarded": [0],
        },
    }


@pytest.fixture
def tx_item_unknown_in(tx_item_common_in):
    return {**tx_item_common_in, **{"newTransactionType": {}}}


@pytest.fixture
def tx_item_unknown_out(tx_item_common_out):
    return {**tx_item_common_out, **{"txn_type": "OTHER"}}


@pytest.fixture
def tx_item_validation_error_in(tx_item_common_in):
    return {
        **tx_item_common_in,
        **{"contractCall": {"contractID": "", "gas": "gas", "amount": 1000}},
    }


@pytest.fixture
def tx_record_common_in():
    return {
        "receipt": {
            "status": 22,
            "exchangeRate": {
                "currentRate": {
                    "hbarEquiv": 30000,
                    "centEquiv": 195899,
                    "expirationTime": {"seconds": 1665709200},
                },
                "nextRate": {
                    "hbarEquiv": 30000,
                    "centEquiv": 195031,
                    "expirationTime": {"seconds": 1665712800},
                },
            },
        },
        "transactionHash": b"\xceD\xad6:\xd26>\xfe\xc6\xc3;\x13\xd2\xa9\xdfi26m\x11\xb2\x8d\xff1\xca\x86\nCX\xe7\n\xb9X\xde\xd1W\xc8\x1f\xf1,\xf0\x18\xc8Z\xfb\x1c\xcc",
        "consensusTimestamp": {"seconds": 1665705839, "nanos": 283835039},
        "transactionID": {
            "transactionValidStart": {
                "seconds": 1665705826,
                "nanos": 654229976,
            },
            "accountID": {"accountNum": 48524011},
        },
        "transactionFee": 154346,
        "transferList": {
            "accountAmounts": [
                {"accountID": {"accountNum": 7}, "amount": 6267},
                {"accountID": {"accountNum": 98}, "amount": 148094},
                {"accountID": {"accountNum": 48524011}, "amount": -154361},
            ]
        },
    }


@pytest.fixture
def tx_record_common_out():
    return {
        "status": "22",
        "currentRate.hbarEquiv": 30000,
        "currentRate.centEquiv": 195899,
        "currentRate.expirationTime.seconds": 1665709200,
        "nextRate.hbarEquiv": 30000,
        "nextRate.centEquiv": 195031,
        "nextRate.expirationTime.seconds": 1665712800,
        "record.transactionHash": "ce44ad363ad2363efec6c33b13d2a9df6932366d11b28dff31ca860a4358e70ab958ded157c81ff12cf018c85afb1ccc",
        "record.consensusTimestamp.seconds": 1665705839,
        "record.consensusTimestamp.nanos": 283835039,
        "record.transactionValidStart.seconds": 1665705826,
        "record.transactionValidStart.nanos": 654229976,
        "record.accountID.accountNum": "48524011",
        "record.transactionFee": 154346,
        "record.memo": "",
        "topic_sequence_number": 0,
        "topic_running_hash": b"",
        "topic_running_hash_version": 0,
        "created_account": "0",
        "schedule_id": "0",
        "token_number": "0",
        "file_id": "0",
        "consensus_create_topicID": "0",
        "record.accountNum.1": 7,
        "record.amount.1": 6267,
        "record.accountNum.2": 98,
        "record.amount.2": 148094,
        "record.accountNum.3": 48524011,
        "record.amount.3": -154361,
        "transfer_list": [
            {"accountID": {"accountNum": 7}, "amount": 6267},
            {"accountID": {"accountNum": 98}, "amount": 148094},
            {"accountID": {"accountNum": 48524011}, "amount": -154361},
        ],
    }


@pytest.fixture
def tx_record_transfer_list_out(tx_record_common_out):
    return tx_record_common_out


@pytest.fixture
def tx_record_ft_transfer_list_in(tx_record_common_in):
    return {
        **tx_record_common_in,
        **{
            "tokenTransferLists": [
                {
                    "token": {"tokenNum": 0},
                    "transfers": [
                        {"accountID": {"accountNum": 0}, "amount": 1},
                        {"accountID": {"accountNum": 1}, "amount": -1},
                    ],
                }
            ]
        },
    }


@pytest.fixture
def tx_record_ft_transfer_list_out(tx_record_common_out):
    return {
        **tx_record_common_out,
        **{
            "token_transfer_account_1": 0,
            "token_transfer_amount_1": 1,
            "token_transfer_account_2": 1,
            "token_transfer_amount_2": -1,
            "token_transfer_list": [
                {
                    "token": {"tokenNum": "0"},
                    "transfers": [
                        {"accountID": {"accountNum": 0}, "amount": 1},
                        {"accountID": {"accountNum": 1}, "amount": -1},
                    ],
                }
            ],
        },
    }


@pytest.fixture
def tx_record_nft_transfer_list_in(tx_record_common_in):
    nft_receipt_temp = {
        **tx_record_common_in["receipt"],
        **{"serialNumbers": [1]},
    }
    nft_receipt = {"receipt": nft_receipt_temp}
    nft_tx_record = {
        **nft_receipt,
        **{
            "transactionHash": b"\xceD\xad6:\xd26>\xfe\xc6\xc3;\x13\xd2\xa9\xdfi26m\x11\xb2\x8d\xff1\xca\x86\nCX\xe7\n\xb9X\xde\xd1W\xc8\x1f\xf1,\xf0\x18\xc8Z\xfb\x1c\xcc",
            "consensusTimestamp": {"seconds": 1665705839, "nanos": 283835039},
            "transactionID": {
                "transactionValidStart": {
                    "seconds": 1665705826,
                    "nanos": 654229976,
                },
                "accountID": {"accountNum": 48524011},
            },
            "transactionFee": 154346,
            "transferList": {
                "accountAmounts": [
                    {"accountID": {"accountNum": 7}, "amount": 6267},
                    {"accountID": {"accountNum": 98}, "amount": 148094},
                    {"accountID": {"accountNum": 48524011}, "amount": -154361},
                ]
            },
        },
    }

    return {
        **nft_tx_record,
        **{
            "tokenTransferLists": [
                {
                    "token": {"tokenNum": "0"},
                    "nftTransfers": [
                        {
                            "senderAccountID": {"accountNum": 0},
                            "receiverAccountID": {"accountNum": 1},
                            "serialNumber": 1,
                        }
                    ],
                }
            ]
        },
    }


@pytest.fixture
def tx_record_nft_transfer_list_out(tx_record_common_out):
    return {
        **tx_record_common_out,
        **{
            "nft_sender_1": 0,
            "nft_receiver_1": 1,
            "nft_serial_number_1": 1,
            "nft_serial_numbers": [1],
            "token_transfer_list": [
                {
                    "token": {"tokenNum": "0"},
                    "nftTransfers": [
                        {
                            "senderAccountID": {"accountNum": 0},
                            "receiverAccountID": {"accountNum": 1},
                            "serialNumber": 1,
                        }
                    ],
                }
            ],
        },
    }


@pytest.fixture
def tx_record_contract_create_in(tx_record_common_in):
    return {
        **tx_record_common_in,
        **{
            "contractCreateResult": {
                "contractID": {"contractNum": 0},
                "bloom": b"bloom",
                "gasUsed": 1000,
                "logInfo": [
                    {
                        "contractID": {"contractNum": 1},
                        "bloom": b"log bloom",
                        "topic": b"topic",
                        "data": b"data",
                    }
                ],
                "createdContractIDs": [{"contractNum": 2}],
            }
        },
    }


@pytest.fixture
def tx_record_contract_create_out(tx_record_common_out):
    return {
        **tx_record_common_out,
        **{
            "record.contractID.contractNum": 0,
            "record.bloom": b"bloom",
            "record.gasUsed": 1000,
            "record.logInfo.contractID.contractNum": 1,
            "record.logInfo.bloom": b"log bloom",
            "record.logInfo.topic": b"topic",
            "record.logInfo.data": b"data",
            "record.createdContractIDs.contractNum.1": 2,
        },
    }


@pytest.fixture
def tx_record_contract_call_in(tx_record_common_in):
    return {
        **tx_record_common_in,
        **{
            "contractCallResult": {
                "contractID": {"contractNum": 0},
                "bloom": b"bloom",
                "gasUsed": 1000,
                "logInfo": [
                    {
                        "contractID": {"contractNum": 1},
                        "bloom": b"log bloom",
                        "topic": b"topic",
                        "data": b"data",
                    }
                ],
                "createdContractIDs": [{"contractNum": 2}],
            }
        },
    }


@pytest.fixture
def tx_record_contract_call_out(tx_record_common_out):
    return {
        **tx_record_common_out,
        **{
            "record.contractID.contractNum": 0,
            "record.bloom": b"bloom",
            "record.gasUsed": 1000,
            "record.logInfo.contractID.contractNum": 1,
            "record.logInfo.bloom": b"log bloom",
            "record.logInfo.topic": b"topic",
            "record.logInfo.data": b"data",
            "record.createdContractIDs.contractNum.1": 2,
        },
    }


@pytest.fixture
def reclassify_nft_transfer():
    return {"txn_type": "CRYPTOTRANSFER", "nft_serial_number_1": 1}


@pytest.fixture
def reclassify_nft_wipe():
    return {"txn_type": "TOKENWIPE", "nft_serial_number_1": 1}


@pytest.fixture
def reclassify_nft_burn():
    return {"txn_type": "TOKENBURN", "nft_serial_number_1": 1}


@pytest.fixture
def reclassify_nft_mint_1():
    return {"txn_type": "TOKENMINT", "nft_serial_number_1": 1}


@pytest.fixture
def reclassify_nft_mint_2():
    return {"txn_type": "TOKENMINT", "nft_serial_numbers": [1]}


@pytest.fixture
def reclassify_ft_transfer():
    return {"txn_type": "CRYPTOTRANSFER", "token_transfer_amount_1": 1}


@pytest.fixture
def reclassify_nft_creation():
    return {"txn_type": "TOKENCREATION", "token_type": 1}


@pytest.fixture
def add_txn_metadata_in():
    return {
        "body.transactionValidStart.seconds": 1665705830,
        "body.transactionValidStart.nanos": 19767741,
        "record.transactionValidStart.seconds": 1665705830,
        "record.transactionValidStart.nanos": 19767741,
        "record.consensusTimestamp.seconds": 1665705830,
        "record.consensusTimestamp.nanos": 19767741,
    }


@pytest.fixture
def add_txn_metadata_out():
    return {
        "body.transactionValidStart.seconds": 1665705830,
        "body.transactionValidStart.nanos": 19767741,
        "record.transactionValidStart.seconds": 1665705830,
        "record.transactionValidStart.nanos": 19767741,
        "record.consensusTimestamp.seconds": 1665705830,
        "record.consensusTimestamp.nanos": 19767741,
        "@processed": "2022-10-14T00:03:50.20Z",
        "rcd_filename": "filename",
        "msg": "transaction",
        "body.@timestamp": "2022-10-14T00:03:50.20Z",
        "record.@timestamp": "2022-10-14T00:03:50.20Z",
        "consensusTimestamp": "2022-10-14T00:03:50.20Z",
    }


@pytest.fixture
def parse_v6_transaction_in():
    return [
        {
            "filename": "tests/data/rcd_gz/2022-10-14T00_00_00.626345694Z.rcd.gz",
            "transaction_record": {
                "receipt": {"status": 22},
                "transactionHash": b"\xa2\\6\xee\x92\xaf6A\x97\xddln\x18\xaf(\xb4H|\xee\x90\xae+aY\xd5\x9c\x9cv\x8a\n\x7f9\xf6\x85\x10\xf0\\\xb2\xfeJ\xbf\x9f\xff\x01\xb4\xba\x17\xd5",
                "consensusTimestamp": {
                    "seconds": 1665705600,
                    "nanos": 626345694,
                },
                "transactionID": {
                    "transactionValidStart": {
                        "seconds": 1665705589,
                        "nanos": 242461200,
                    },
                    "accountID": {"accountNum": 48524011},
                    "nonce": 1,
                },
                "memo": "End of staking period calculation record",
                "transferList": {},
            },
            "transaction_body": {
                "transactionID": {
                    "transactionValidStart": {
                        "seconds": 1665705589,
                        "nanos": 242461200,
                    },
                    "accountID": {"accountNum": 48524011},
                    "nonce": 1,
                },
                "node_stake_update": {
                    "end_of_staking_period": {
                        "seconds": 1665705599,
                        "nanos": 999999999,
                    },
                    "node_stake": [
                        {
                            "max_stake": 714285714285714285,
                            "min_stake": 178571428571428571,
                            "reward_rate": 17808,
                            "stake_not_rewarded": 100002000000000,
                            "stake_rewarded": 227121500000000,
                        },
                        {
                            "max_stake": 714285714285714285,
                            "min_stake": 178571428571428571,
                            "node_id": 1,
                            "reward_rate": 17808,
                            "stake_rewarded": 230172100000000,
                        },
                        {
                            "max_stake": 714285714285714285,
                            "min_stake": 178571428571428571,
                            "node_id": 2,
                            "reward_rate": 17808,
                            "stake_rewarded": 99027600000000,
                        },
                        {
                            "max_stake": 714285714285714285,
                            "min_stake": 178571428571428571,
                            "node_id": 3,
                            "reward_rate": 17808,
                            "stake_not_rewarded": 170000000000,
                            "stake_rewarded": 6083400000000,
                        },
                        {
                            "max_stake": 714285714285714285,
                            "min_stake": 178571428571428571,
                            "node_id": 4,
                            "reward_rate": 17808,
                            "stake_not_rewarded": 104700000000,
                            "stake_rewarded": 2790200000000,
                        },
                        {
                            "max_stake": 714285714285714285,
                            "min_stake": 178571428571428571,
                            "node_id": 5,
                            "reward_rate": 17808,
                            "stake_rewarded": 1083300900000000,
                        },
                        {
                            "max_stake": 714285714285714285,
                            "min_stake": 178571428571428571,
                            "node_id": 6,
                            "reward_rate": 17808,
                            "stake_rewarded": 26552900000000,
                        },
                    ],
                },
            },
            "txn_sign_keys": ["ed25519", "ed25519"],
        }
    ]


@pytest.fixture()
def parser_v6_transaction_out():
    return [
        {
            "status": "22",
            "currentRate.hbarEquiv": 0,
            "currentRate.centEquiv": 0,
            "currentRate.expirationTime.seconds": 0,
            "nextRate.hbarEquiv": 0,
            "nextRate.centEquiv": 0,
            "nextRate.expirationTime.seconds": 0,
            "record.transactionHash": "a25c36ee92af364197dd6c6e18af28b4487cee90ae2b6159d59c9c768a0a7f39f68510f05cb2fe4abf9fff01b4ba17d5",
            "record.consensusTimestamp.seconds": 1665705600,
            "record.consensusTimestamp.nanos": 626345694,
            "record.transactionValidStart.seconds": 1665705589,
            "record.transactionValidStart.nanos": 242461200,
            "record.accountID.accountNum": "48524011",
            "record.transactionFee": 0,
            "record.memo": "End of staking period calculation record",
            "topic_sequence_number": 0,
            "topic_running_hash": "",
            "topic_running_hash_version": 0,
            "created_account": "0",
            "schedule_id": "0",
            "token_number": "0",
            "file_id": "0",
            "consensus_create_topicID": "0",
            "body.transactionValidStart.seconds": 1665705589,
            "body.transactionValidStart.nanos": 242461200,
            "body.accountID.accountNum": "48524011",
            "body.nodeAccountID.accountNum": "0",
            "scheduled": False,
            "body.transactionFee": 0,
            "body.transactionValidDuration.seconds": 0,
            "nonce": 1,
            "node_stake_max_stake": [
                7142857142,
                7142857142,
                7142857142,
                7142857142,
                7142857142,
                7142857142,
                7142857142,
            ],
            "node_stake_min_stake": [
                1785714285,
                1785714285,
                1785714285,
                1785714285,
                1785714285,
                1785714285,
                1785714285,
            ],
            "node_stake_id": [0, 1, 2, 3, 4, 5, 6],
            "node_stake_account": [
                "0.0.3",
                "0.0.4",
                "0.0.5",
                "0.0.6",
                "0.0.7",
                "0.0.8",
                "0.0.9",
            ],
            "node_stake_reward_rate": [
                17808,
                17808,
                17808,
                17808,
                17808,
                17808,
                17808,
            ],
            "node_stake_not_rewarded": [1000020, 0, 0, 1700, 1047, 0, 0],
            "node_stake_rewarded": [
                2271215,
                2301721,
                990276,
                60834,
                27902,
                10833009,
                265529,
            ],
            "txn_type": "NODESTAKEUPDATE",
            "@processed": "2022-10-14T00_00_00.626345694Z",
            "rcd_filename": "2022-10-14T00_00_00.626345694Z.rcd.gz",
            "msg": "transaction",
            "body.@timestamp": "2022-10-13T23:59:49.242Z",
            "record.@timestamp": "2022-10-13T23:59:49.242Z",
            "consensusTimestamp": "2022-10-14T00:00:00.626Z",
            "txn_sign_keys": ["ed25519", "ed25519"],
        }
    ]


@pytest.fixture
def parse_v6_transaction_in_type_error():
    return [
        {
            "filename": "tests/data/rcd_gz/2022-10-14T00_00_00.626345694Z.rcd.gz",
            "transaction_record": "",
            "transaction_body": "",
        }
    ]


@pytest.fixture
def parse_v6_transaction_in_validation_error():
    return [
        {
            "filename": "tests/data/rcd_gz/2022-10-14T00_00_00.626345694Z.rcd.gz",
            "transaction_record": {},
            "transaction_body": {},
        }
    ]
