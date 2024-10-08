# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: token_grant_kyc.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from hedera.util.proto_pb import basic_types_pb2 as basic__types__pb2

DESCRIPTOR = _descriptor.FileDescriptor(
    name="token_grant_kyc.proto",
    package="proto",
    syntax="proto3",
    serialized_options=b'\n"com.hederahashgraph.api.proto.javaP\001',
    serialized_pb=b'\n\x15token_grant_kyc.proto\x12\x05proto\x1a\x11\x62\x61sic_types.proto"`\n\x1cTokenGrantKycTransactionBody\x12\x1d\n\x05token\x18\x01 \x01(\x0b\x32\x0e.proto.TokenID\x12!\n\x07\x61\x63\x63ount\x18\x02 \x01(\x0b\x32\x10.proto.AccountIDB&\n"com.hederahashgraph.api.proto.javaP\x01\x62\x06proto3',
    dependencies=[
        basic__types__pb2.DESCRIPTOR,
    ],
)


_TOKENGRANTKYCTRANSACTIONBODY = _descriptor.Descriptor(
    name="TokenGrantKycTransactionBody",
    full_name="proto.TokenGrantKycTransactionBody",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="token",
            full_name="proto.TokenGrantKycTransactionBody.token",
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
            name="account",
            full_name="proto.TokenGrantKycTransactionBody.account",
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
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=51,
    serialized_end=147,
)

_TOKENGRANTKYCTRANSACTIONBODY.fields_by_name["token"].message_type = basic__types__pb2._TOKENID
_TOKENGRANTKYCTRANSACTIONBODY.fields_by_name["account"].message_type = basic__types__pb2._ACCOUNTID
DESCRIPTOR.message_types_by_name["TokenGrantKycTransactionBody"] = _TOKENGRANTKYCTRANSACTIONBODY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

TokenGrantKycTransactionBody = _reflection.GeneratedProtocolMessageType(
    "TokenGrantKycTransactionBody",
    (_message.Message,),
    {
        "DESCRIPTOR": _TOKENGRANTKYCTRANSACTIONBODY,
        "__module__": "token_grant_kyc_pb2"
        # @@protoc_insertion_point(class_scope:proto.TokenGrantKycTransactionBody)
    },
)
_sym_db.RegisterMessage(TokenGrantKycTransactionBody)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
