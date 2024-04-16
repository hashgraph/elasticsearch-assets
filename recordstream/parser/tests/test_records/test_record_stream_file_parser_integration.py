import logging

import pytest

from hedera.records.record_file_parser import parse_transaction_v6


def test_parse_transaction_v6(parse_v6_transaction_in, parser_v6_transaction_out):
    out = parse_transaction_v6(
            parse_v6_transaction_in,
            "2022-10-14T00_00_00.626345694Z",
            logging.Logger,
        )
    assert out == parser_v6_transaction_out


def test_parse_transaction_v6_type_error(parse_v6_transaction_in_type_error):
    with pytest.raises(TypeError):
        parse_transaction_v6(
            parse_v6_transaction_in_type_error,
            "2022-10-14T00_00_00.626345694Z",
            logging.Logger,
        )


def test_parse_v6_transaction_in_validation_error(
    parse_v6_transaction_in_validation_error,
):
    with pytest.raises(TypeError):
        parse_transaction_v6(
            parse_v6_transaction_in_validation_error,
            "2022-10-14T00_00_00.626345694Z",
            logging.Logger,
        )
