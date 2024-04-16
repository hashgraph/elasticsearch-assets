# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: crypto_get_account_balance.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from hedera.util.proto_pb import basic_types_pb2 as basic__types__pb2
from hedera.util.proto_pb import query_header_pb2 as query__header__pb2
from hedera.util.proto_pb import response_header_pb2 as response__header__pb2
from hedera.util.proto_pb import timestamp_pb2 as timestamp__pb2

DESCRIPTOR = _descriptor.FileDescriptor(
    name="crypto_get_account_balance.proto",
    package="proto",
    syntax="proto3",
    serialized_options=b'\n"com.hederahashgraph.api.proto.javaP\001',
    serialized_pb=b'\n crypto_get_account_balance.proto\x12\x05proto\x1a\x11\x62\x61sic_types.proto\x1a\x12query_header.proto\x1a\x15response_header.proto\x1a\x0ftimestamp.proto"\xa3\x01\n\x1c\x43ryptoGetAccountBalanceQuery\x12"\n\x06header\x18\x01 \x01(\x0b\x32\x12.proto.QueryHeader\x12%\n\taccountID\x18\x02 \x01(\x0b\x32\x10.proto.AccountIDH\x00\x12\'\n\ncontractID\x18\x03 \x01(\x0b\x32\x11.proto.ContractIDH\x00\x42\x0f\n\rbalanceSource"\xaa\x01\n\x1f\x43ryptoGetAccountBalanceResponse\x12%\n\x06header\x18\x01 \x01(\x0b\x32\x15.proto.ResponseHeader\x12#\n\taccountID\x18\x02 \x01(\x0b\x32\x10.proto.AccountID\x12\x0f\n\x07\x62\x61lance\x18\x03 \x01(\x04\x12*\n\rtokenBalances\x18\x04 \x03(\x0b\x32\x13.proto.TokenBalanceB&\n"com.hederahashgraph.api.proto.javaP\x01\x62\x06proto3',
    dependencies=[
        basic__types__pb2.DESCRIPTOR,
        query__header__pb2.DESCRIPTOR,
        response__header__pb2.DESCRIPTOR,
        timestamp__pb2.DESCRIPTOR,
    ],
)


_CRYPTOGETACCOUNTBALANCEQUERY = _descriptor.Descriptor(
    name="CryptoGetAccountBalanceQuery",
    full_name="proto.CryptoGetAccountBalanceQuery",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="header",
            full_name="proto.CryptoGetAccountBalanceQuery.header",
            index=0,
            number=1,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="accountID",
            full_name="proto.CryptoGetAccountBalanceQuery.accountID",
            index=1,
            number=2,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="contractID",
            full_name="proto.CryptoGetAccountBalanceQuery.contractID",
            index=2,
            number=3,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[
        _descriptor.OneofDescriptor(
            name="balanceSource",
            full_name="proto.CryptoGetAccountBalanceQuery.balanceSource",
            index=0,
            containing_type=None,
            fields=[],
        ),
    ],
    serialized_start=123,
    serialized_end=286,
)


_CRYPTOGETACCOUNTBALANCERESPONSE = _descriptor.Descriptor(
    name="CryptoGetAccountBalanceResponse",
    full_name="proto.CryptoGetAccountBalanceResponse",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="header",
            full_name="proto.CryptoGetAccountBalanceResponse.header",
            index=0,
            number=1,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="accountID",
            full_name="proto.CryptoGetAccountBalanceResponse.accountID",
            index=1,
            number=2,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="balance",
            full_name="proto.CryptoGetAccountBalanceResponse.balance",
            index=2,
            number=3,
            type=4,
            cpp_type=4,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="tokenBalances",
            full_name="proto.CryptoGetAccountBalanceResponse.tokenBalances",
            index=3,
            number=4,
            type=11,
            cpp_type=10,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=289,
    serialized_end=459,
)

_CRYPTOGETACCOUNTBALANCEQUERY.fields_by_name["header"].message_type = query__header__pb2._QUERYHEADER
_CRYPTOGETACCOUNTBALANCEQUERY.fields_by_name["accountID"].message_type = basic__types__pb2._ACCOUNTID
_CRYPTOGETACCOUNTBALANCEQUERY.fields_by_name["contractID"].message_type = basic__types__pb2._CONTRACTID
_CRYPTOGETACCOUNTBALANCEQUERY.oneofs_by_name["balanceSource"].fields.append(
    _CRYPTOGETACCOUNTBALANCEQUERY.fields_by_name["accountID"]
)
_CRYPTOGETACCOUNTBALANCEQUERY.fields_by_name[
    "accountID"
].containing_oneof = _CRYPTOGETACCOUNTBALANCEQUERY.oneofs_by_name["balanceSource"]
_CRYPTOGETACCOUNTBALANCEQUERY.oneofs_by_name["balanceSource"].fields.append(
    _CRYPTOGETACCOUNTBALANCEQUERY.fields_by_name["contractID"]
)
_CRYPTOGETACCOUNTBALANCEQUERY.fields_by_name[
    "contractID"
].containing_oneof = _CRYPTOGETACCOUNTBALANCEQUERY.oneofs_by_name["balanceSource"]
_CRYPTOGETACCOUNTBALANCERESPONSE.fields_by_name["header"].message_type = response__header__pb2._RESPONSEHEADER
_CRYPTOGETACCOUNTBALANCERESPONSE.fields_by_name["accountID"].message_type = basic__types__pb2._ACCOUNTID
_CRYPTOGETACCOUNTBALANCERESPONSE.fields_by_name["tokenBalances"].message_type = basic__types__pb2._TOKENBALANCE
DESCRIPTOR.message_types_by_name["CryptoGetAccountBalanceQuery"] = _CRYPTOGETACCOUNTBALANCEQUERY
DESCRIPTOR.message_types_by_name["CryptoGetAccountBalanceResponse"] = _CRYPTOGETACCOUNTBALANCERESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

CryptoGetAccountBalanceQuery = _reflection.GeneratedProtocolMessageType(
    "CryptoGetAccountBalanceQuery",
    (_message.Message,),
    {
        "DESCRIPTOR": _CRYPTOGETACCOUNTBALANCEQUERY,
        "__module__": "crypto_get_account_balance_pb2"
        # @@protoc_insertion_point(class_scope:proto.CryptoGetAccountBalanceQuery)
    },
)
_sym_db.RegisterMessage(CryptoGetAccountBalanceQuery)

CryptoGetAccountBalanceResponse = _reflection.GeneratedProtocolMessageType(
    "CryptoGetAccountBalanceResponse",
    (_message.Message,),
    {
        "DESCRIPTOR": _CRYPTOGETACCOUNTBALANCERESPONSE,
        "__module__": "crypto_get_account_balance_pb2"
        # @@protoc_insertion_point(class_scope:proto.CryptoGetAccountBalanceResponse)
    },
)
_sym_db.RegisterMessage(CryptoGetAccountBalanceResponse)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
