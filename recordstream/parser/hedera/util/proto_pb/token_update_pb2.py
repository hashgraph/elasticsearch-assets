# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: token_update.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2

from hedera.util.proto_pb import basic_types_pb2 as basic__types__pb2
from hedera.util.proto_pb import duration_pb2 as duration__pb2
from hedera.util.proto_pb import timestamp_pb2 as timestamp__pb2

DESCRIPTOR = _descriptor.FileDescriptor(
    name="token_update.proto",
    package="proto",
    syntax="proto3",
    serialized_options=b'\n"com.hederahashgraph.api.proto.javaP\001',
    serialized_pb=b'\n\x12token_update.proto\x12\x05proto\x1a\x11\x62\x61sic_types.proto\x1a\x0e\x64uration.proto\x1a\x0ftimestamp.proto\x1a\x1egoogle/protobuf/wrappers.proto"\xfb\x03\n\x1aTokenUpdateTransactionBody\x12\x1d\n\x05token\x18\x01 \x01(\x0b\x32\x0e.proto.TokenID\x12\x0e\n\x06symbol\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12"\n\x08treasury\x18\x04 \x01(\x0b\x32\x10.proto.AccountID\x12\x1c\n\x08\x61\x64minKey\x18\x05 \x01(\x0b\x32\n.proto.Key\x12\x1a\n\x06kycKey\x18\x06 \x01(\x0b\x32\n.proto.Key\x12\x1d\n\tfreezeKey\x18\x07 \x01(\x0b\x32\n.proto.Key\x12\x1b\n\x07wipeKey\x18\x08 \x01(\x0b\x32\n.proto.Key\x12\x1d\n\tsupplyKey\x18\t \x01(\x0b\x32\n.proto.Key\x12*\n\x10\x61utoRenewAccount\x18\n \x01(\x0b\x32\x10.proto.AccountID\x12(\n\x0f\x61utoRenewPeriod\x18\x0b \x01(\x0b\x32\x0f.proto.Duration\x12 \n\x06\x65xpiry\x18\x0c \x01(\x0b\x32\x10.proto.Timestamp\x12*\n\x04memo\x18\r \x01(\x0b\x32\x1c.google.protobuf.StringValue\x12$\n\x10\x66\x65\x65_schedule_key\x18\x0e \x01(\x0b\x32\n.proto.Key\x12\x1d\n\tpause_key\x18\x0f \x01(\x0b\x32\n.proto.KeyB&\n"com.hederahashgraph.api.proto.javaP\x01\x62\x06proto3',
    dependencies=[
        basic__types__pb2.DESCRIPTOR,
        duration__pb2.DESCRIPTOR,
        timestamp__pb2.DESCRIPTOR,
        google_dot_protobuf_dot_wrappers__pb2.DESCRIPTOR,
    ],
)


_TOKENUPDATETRANSACTIONBODY = _descriptor.Descriptor(
    name="TokenUpdateTransactionBody",
    full_name="proto.TokenUpdateTransactionBody",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="token",
            full_name="proto.TokenUpdateTransactionBody.token",
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
            name="symbol",
            full_name="proto.TokenUpdateTransactionBody.symbol",
            index=1,
            number=2,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"".decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="name",
            full_name="proto.TokenUpdateTransactionBody.name",
            index=2,
            number=3,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"".decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="treasury",
            full_name="proto.TokenUpdateTransactionBody.treasury",
            index=3,
            number=4,
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
            name="adminKey",
            full_name="proto.TokenUpdateTransactionBody.adminKey",
            index=4,
            number=5,
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
            name="kycKey",
            full_name="proto.TokenUpdateTransactionBody.kycKey",
            index=5,
            number=6,
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
            name="freezeKey",
            full_name="proto.TokenUpdateTransactionBody.freezeKey",
            index=6,
            number=7,
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
            name="wipeKey",
            full_name="proto.TokenUpdateTransactionBody.wipeKey",
            index=7,
            number=8,
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
            name="supplyKey",
            full_name="proto.TokenUpdateTransactionBody.supplyKey",
            index=8,
            number=9,
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
            name="autoRenewAccount",
            full_name="proto.TokenUpdateTransactionBody.autoRenewAccount",
            index=9,
            number=10,
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
            name="autoRenewPeriod",
            full_name="proto.TokenUpdateTransactionBody.autoRenewPeriod",
            index=10,
            number=11,
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
            name="expiry",
            full_name="proto.TokenUpdateTransactionBody.expiry",
            index=11,
            number=12,
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
            name="memo",
            full_name="proto.TokenUpdateTransactionBody.memo",
            index=12,
            number=13,
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
            name="fee_schedule_key",
            full_name="proto.TokenUpdateTransactionBody.fee_schedule_key",
            index=13,
            number=14,
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
            name="pause_key",
            full_name="proto.TokenUpdateTransactionBody.pause_key",
            index=14,
            number=15,
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
    serialized_start=114,
    serialized_end=621,
)

_TOKENUPDATETRANSACTIONBODY.fields_by_name["token"].message_type = basic__types__pb2._TOKENID
_TOKENUPDATETRANSACTIONBODY.fields_by_name["treasury"].message_type = basic__types__pb2._ACCOUNTID
_TOKENUPDATETRANSACTIONBODY.fields_by_name["adminKey"].message_type = basic__types__pb2._KEY
_TOKENUPDATETRANSACTIONBODY.fields_by_name["kycKey"].message_type = basic__types__pb2._KEY
_TOKENUPDATETRANSACTIONBODY.fields_by_name["freezeKey"].message_type = basic__types__pb2._KEY
_TOKENUPDATETRANSACTIONBODY.fields_by_name["wipeKey"].message_type = basic__types__pb2._KEY
_TOKENUPDATETRANSACTIONBODY.fields_by_name["supplyKey"].message_type = basic__types__pb2._KEY
_TOKENUPDATETRANSACTIONBODY.fields_by_name["autoRenewAccount"].message_type = basic__types__pb2._ACCOUNTID
_TOKENUPDATETRANSACTIONBODY.fields_by_name["autoRenewPeriod"].message_type = duration__pb2._DURATION
_TOKENUPDATETRANSACTIONBODY.fields_by_name["expiry"].message_type = timestamp__pb2._TIMESTAMP
_TOKENUPDATETRANSACTIONBODY.fields_by_name["memo"].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_TOKENUPDATETRANSACTIONBODY.fields_by_name["fee_schedule_key"].message_type = basic__types__pb2._KEY
_TOKENUPDATETRANSACTIONBODY.fields_by_name["pause_key"].message_type = basic__types__pb2._KEY
DESCRIPTOR.message_types_by_name["TokenUpdateTransactionBody"] = _TOKENUPDATETRANSACTIONBODY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

TokenUpdateTransactionBody = _reflection.GeneratedProtocolMessageType(
    "TokenUpdateTransactionBody",
    (_message.Message,),
    {
        "DESCRIPTOR": _TOKENUPDATETRANSACTIONBODY,
        "__module__": "token_update_pb2"
        # @@protoc_insertion_point(class_scope:proto.TokenUpdateTransactionBody)
    },
)
_sym_db.RegisterMessage(TokenUpdateTransactionBody)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
