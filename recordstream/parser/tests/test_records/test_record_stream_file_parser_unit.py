import os

import pytest
from pydantic import ValidationError

from hedera.records.record_file_parser import (
    RcdParser,
)
from hedera.util.common.serializable import RecordStreamObject
from hedera.util.common.stream import SerializableDataInputStream

parser = RcdParser()


@pytest.fixture(scope="module")

def test_check_version():
    filename = "2022-03-02T00_00_00.063618034Z.rcd"

    with open("tests/test_records/data/scan_path/2022-03-02T00_00_00.063618034Z.rcd", "rb") as f:
        dis = SerializableDataInputStream(f)

        parser.check_version(dis, filename)


def test_create_v5_transaction_body():
    filename = "2022-03-02T00_00_00.063618034Z.rcd"

    with open("tests/test_records/data/scan_path/2022-03-02T00_00_00.063618034Z.rcd", "rb") as f:
        dis = SerializableDataInputStream(f)
        parser.check_version(dis, filename)
        while dis.available():
            object = dis.readSerializable(True, None)
            if isinstance(object, RecordStreamObject):
                transaction_item_dict = parser.create_v5_transaction_body(object)

                assert type(transaction_item_dict) == dict


def test_create_v5_transaction_record():
    filename = "2022-03-02T00_00_00.063618034Z.rcd"

    with open("tests/test_records/data/scan_path/2022-03-02T00_00_00.063618034Z.rcd", "rb") as f:
        dis = SerializableDataInputStream(f)
        parser.check_version(dis, filename)
        while dis.available():
            object = dis.readSerializable(True, None)
            if isinstance(object, RecordStreamObject):
                transaction_record_dict = parser.create_v5_transaction_record(object)

                assert type(transaction_record_dict) == dict


def test_read_v6_file():
    out = parser.read_v6_file(
        "tests/test_records/data/rcd_v6/2022-10-14T00_00_00.626345694Z.rcd",
        "2022-10-14T00_00_00.626345694Z.rcd",
    )
    assert len(out) == 2
    assert len(out[0]) == 12
    assert os.path.exists("tests/test_records/data/rcd_v6/2022-10-14T00_00_00.626345694Z.rcd_processed")

    os.remove("tests/test_records/data/rcd_v6/2022-10-14T00_00_00.626345694Z.rcd_processed")


def test_consensus_submit_message(tx_item_consensus_submit_message_in, tx_item_consensus_submit_message_out):
    out = parser.parse_transaction_item(tx_item_consensus_submit_message_in)
    assert out == tx_item_consensus_submit_message_out


def test_consensus_create_topic(tx_item_consensus_create_topic_in, tx_item_consensus_create_topic_out):
    out = parser.parse_transaction_item(tx_item_consensus_create_topic_in)
    assert out == tx_item_consensus_create_topic_out


def test_consensus_update_topic(tx_item_consensus_update_topic_in, tx_item_consensus_update_topic_out):
    out = parser.parse_transaction_item(tx_item_consensus_update_topic_in)
    assert out == tx_item_consensus_update_topic_out


def test_crypto_transfer(tx_item_crypto_transfer_in, tx_item_crypto_transfer_out):
    out = parser.parse_transaction_item(tx_item_crypto_transfer_in)
    assert out == tx_item_crypto_transfer_out


def test_crypto_create_account(tx_item_crypto_create_account_in, tx_item_crypto_create_account_out):
    out = parser.parse_transaction_item(tx_item_crypto_create_account_in)
    assert out == tx_item_crypto_create_account_out


def test_crypto_update_account(tx_item_crypto_update_account_in, tx_item_crypto_update_account_out):
    out = parser.parse_transaction_item(tx_item_crypto_update_account_in)
    assert out == tx_item_crypto_update_account_out


def test_crypto_delete_account(tx_item_crypto_delete_in, tx_item_crypto_delete_out):
    out = parser.parse_transaction_item(tx_item_crypto_delete_in)
    assert out == tx_item_crypto_delete_out


def test_file_update(tx_item_file_update_in, tx_item_file_update_out):
    out = parser.parse_transaction_item(tx_item_file_update_in)
    assert out == tx_item_file_update_out


def test_file_delete(tx_item_file_delete_in, tx_item_file_delete_out):
    out = parser.parse_transaction_item(tx_item_file_delete_in)
    assert out == tx_item_file_delete_out


def test_file_append(tx_item_file_append_in, tx_item_file_append_out):
    out = parser.parse_transaction_item(tx_item_file_append_in)
    assert out == tx_item_file_append_out


def test_file_create(tx_item_file_create_in, tx_item_file_create_out):
    out = parser.parse_transaction_item(tx_item_file_create_in)
    assert out == tx_item_file_create_out


def test_schedule_create(tx_item_schedule_create_in, tx_item_schedule_create_out):
    out = parser.parse_transaction_item(tx_item_schedule_create_in)
    assert out == tx_item_schedule_create_out


def test_schedule_sign(tx_item_schedule_sign_in, tx_item_schedule_sign_out):
    out = parser.parse_transaction_item(tx_item_schedule_sign_in)
    assert out == tx_item_schedule_sign_out


def test_schedule_delete(tx_item_schedule_delete_in, tx_item_schedule_delete_out):
    out = parser.parse_transaction_item(tx_item_schedule_delete_in)
    assert out == tx_item_schedule_delete_out


def test_token_associate_single(tx_item_token_associate_single_in, tx_item_token_associate_single_out):
    out = parser.parse_transaction_item(tx_item_token_associate_single_in)
    assert out == tx_item_token_associate_single_out


def test_token_associate_multiple(tx_item_token_associate_multiple_in, tx_item_token_associate_multiple_out):
    out = parser.parse_transaction_item(tx_item_token_associate_multiple_in)
    assert out == tx_item_token_associate_multiple_out


def test_token_dissociate(tx_item_token_dissociate_in, tx_item_token_dissociate_out):
    out = parser.parse_transaction_item(tx_item_token_dissociate_in)
    assert out == tx_item_token_dissociate_out


def test_token_revoke_kyc(tx_item_token_revoke_kyc_in, tx_item_token_revoke_kyc_out):
    out = parser.parse_transaction_item(tx_item_token_revoke_kyc_in)
    assert out == tx_item_token_revoke_kyc_out


def test_token_grant_kyc(tx_item_token_grant_kyc_in, tx_item_token_grant_kyc_out):
    out = parser.parse_transaction_item(tx_item_token_grant_kyc_in)
    assert out == tx_item_token_grant_kyc_out


def test_token_freeze(tx_item_token_freeze_in, tx_item_token_freeze_out):
    out = parser.parse_transaction_item(tx_item_token_freeze_in)
    assert out == tx_item_token_freeze_out


def test_token_unfreeze(tx_item_token_unfreeze_in, tx_item_token_unfreeze_out):
    out = parser.parse_transaction_item(tx_item_token_unfreeze_in)
    assert out == tx_item_token_unfreeze_out


def test_token_pause(tx_item_token_pause_in, tx_item_token_pause_out):
    out = parser.parse_transaction_item(tx_item_token_pause_in)
    assert out == tx_item_token_pause_out


def test_token_unpause(tx_item_token_unpause_in, tx_item_token_unpause_out):
    out = parser.parse_transaction_item(tx_item_token_unpause_in)
    assert out == tx_item_token_unpause_out


def test_token_delete(tx_item_token_delete_in, tx_item_token_delete_out):
    out = parser.parse_transaction_item(tx_item_token_delete_in)
    assert out == tx_item_token_delete_out


def test_token_mint(tx_item_token_mint_in, tx_item_token_mint_out):
    out = parser.parse_transaction_item(tx_item_token_mint_in)
    assert out == tx_item_token_mint_out


def test_token_wipe(tx_item_token_wipe_in, tx_item_token_wipe_out):
    out = parser.parse_transaction_item(tx_item_token_wipe_in)
    assert out == tx_item_token_wipe_out


def test_token_burn(tx_item_token_burn_in, tx_item_token_burn_out):
    out = parser.parse_transaction_item(tx_item_token_burn_in)
    assert out == tx_item_token_burn_out


def test_token_creation(tx_item_token_creation_in, tx_item_token_creation_out):
    out = parser.parse_transaction_item(tx_item_token_creation_in)
    assert out == tx_item_token_creation_out


def test_token_update(tx_item_token_update_in, tx_item_token_update_out):
    out = parser.parse_transaction_item(tx_item_token_update_in)
    assert out == tx_item_token_update_out


def test_contract_create(tx_item_contract_create_in, tx_item_contract_create_out):
    out = parser.parse_transaction_item(tx_item_contract_create_in)
    assert out == tx_item_contract_create_out


def test_contract_update(tx_item_contract_update_in, tx_item_contract_update_out):
    out = parser.parse_transaction_item(tx_item_contract_update_in)
    assert out == tx_item_contract_update_out


def test_contract_call(tx_item_contract_call_in, tx_item_contract_call_out):
    out = parser.parse_transaction_item(tx_item_contract_call_in)
    assert out == tx_item_contract_call_out


def test_contract_delete(tx_item_contract_delete_in, tx_item_contract_delete_out):
    out = parser.parse_transaction_item(tx_item_contract_delete_in)
    assert out == tx_item_contract_delete_out


def test_ethereum_transaction(tx_item_ethereum_transaction_in, tx_item_ethereum_transaction_out):
    out = parser.parse_transaction_item(tx_item_ethereum_transaction_in)
    assert out == tx_item_ethereum_transaction_out


def test_crypto_approve_allowance(tx_item_crypto_approve_allowance_in, tx_item_crypto_approve_allowance_out):
    out = parser.parse_transaction_item(tx_item_crypto_approve_allowance_in)
    assert out == tx_item_crypto_approve_allowance_out


def test_crypto_delete_allowance(tx_item_crypto_delete_allowance_in, tx_item_crypto_delete_allowance_out):
    out = parser.parse_transaction_item(tx_item_crypto_delete_allowance_in)
    assert out == tx_item_crypto_delete_allowance_out


def test_token_fee_schedule_update(tx_item_token_fee_schedule_update_in, tx_item_token_fee_schedule_update_out):
    out = parser.parse_transaction_item(tx_item_token_fee_schedule_update_in)
    assert out == tx_item_token_fee_schedule_update_out


def test_node_stake_update(tx_item_node_stake_update_in, tx_item_node_stake_update_out):
    out = parser.parse_transaction_item(tx_item_node_stake_update_in)
    assert out == tx_item_node_stake_update_out


def test_unknown_type(tx_item_unknown_in, tx_item_unknown_out):
    out = parser.parse_transaction_item(tx_item_unknown_in)
    assert out == tx_item_unknown_out


def test_tx_item_validation_error(tx_item_validation_error_in):
    with pytest.raises(ValidationError):
        parser.parse_transaction_item(tx_item_validation_error_in)


def test_tx_record_transfer_list(tx_record_common_in, tx_record_transfer_list_out):
    out = parser.parse_transaction_record(tx_record_common_in)
    assert out == tx_record_transfer_list_out


def test_tx_record_ft_transfer(tx_record_ft_transfer_list_in, tx_record_ft_transfer_list_out):
    out = parser.parse_transaction_record(tx_record_ft_transfer_list_in)
    assert out == tx_record_ft_transfer_list_out


def test_tx_record_nft_transfer(tx_record_nft_transfer_list_in, tx_record_nft_transfer_list_out):
    out = parser.parse_transaction_record(tx_record_nft_transfer_list_in)
    assert out == tx_record_nft_transfer_list_out


def test_tx_record_contract_create(tx_record_contract_create_in, tx_record_contract_create_out):
    out = parser.parse_transaction_record(tx_record_contract_create_in)
    assert out == tx_record_contract_create_out


def test_tx_record_contract_call(tx_record_contract_call_in, tx_record_contract_call_out):
    out = parser.parse_transaction_record(tx_record_contract_call_in)
    assert out == tx_record_contract_call_out


def test_reclassify_nft_transfer(reclassify_nft_transfer):
    out = parser.reclassify_token_txns(reclassify_nft_transfer)
    assert out["txn_type"] == "NFTTRANSFER"


def test_reclassify_nft_wipe(reclassify_nft_wipe):
    out = parser.reclassify_token_txns(reclassify_nft_wipe)
    assert out["txn_type"] == "NFTWIPE"


def test_reclassify_nft_burn(reclassify_nft_burn):
    out = parser.reclassify_token_txns(reclassify_nft_burn)
    assert out["txn_type"] == "NFTBURN"


def test_reclassify_nft_mint_1(reclassify_nft_mint_1):
    out = parser.reclassify_token_txns(reclassify_nft_mint_1)
    assert out["txn_type"] == "NFTMINT"


def test_reclassify_nft_mint_2(reclassify_nft_mint_2):
    out = parser.reclassify_token_txns(reclassify_nft_mint_2)
    assert out["txn_type"] == "NFTMINT"


def test_reclassify_ft_transfer(reclassify_ft_transfer):
    out = parser.reclassify_token_txns(reclassify_ft_transfer)
    assert out["txn_type"] == "TOKENTRANSFERS"


def test_reclassify_nft_creation(reclassify_nft_creation):
    out = parser.reclassify_token_txns(reclassify_nft_creation)
    assert out["txn_type"] == "NFTCREATION"


def test_create_ts():
    # Test with seconds and nanos
    ts = parser.create_ts(1665705830, 19767741)
    assert ts == "2022-10-14T00:03:50.20Z"

    # Test if nanos are missing
    ts = parser.create_ts(1665705830, 0)
    assert ts == "2022-10-14T00:03:50.0Z"


def test_add_txn_metadata(add_txn_metadata_in, add_txn_metadata_out):
    out = parser.add_txn_metadata(add_txn_metadata_in, "2022-10-14T00:03:50.20Z", "filename")

    assert out == add_txn_metadata_out


def test_load_txns():
    out = parser.load_txns(
        "tests/test_records/data/rcd_gz/2022-10-14T00_00_00.626345694Z.rcd.gz",
        "tests/test_records/data/rcd_gz/",
    )
    assert len(out) == 2
    assert len(out[0]) == 12
    assert os.path.exists("tests/test_records/data/rcd_gz/2022-10-14T00_00_00.626345694Z.rcd")
    assert os.path.exists("tests/test_records/data/rcd_gz/2022-10-14T00_00_00.626345694Z.rcd_processed")

    os.remove("tests/test_records/data/rcd_gz/2022-10-14T00_00_00.626345694Z.rcd_processed")
    os.remove("tests/test_records/data/rcd_gz/2022-10-14T00_00_00.626345694Z.rcd")
