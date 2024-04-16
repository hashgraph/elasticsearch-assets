# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: schedule_create.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from hedera.util.proto_pb import basic_types_pb2 as basic__types__pb2
from hedera.util.proto_pb import (
    schedulable_transaction_body_pb2 as schedulable__transaction__body__pb2,
)
from hedera.util.proto_pb import timestamp_pb2 as timestamp__pb2

DESCRIPTOR = _descriptor.FileDescriptor(
    name="schedule_create.proto",
    package="proto",
    syntax="proto3",
    serialized_options=b'\n"com.hederahashgraph.api.proto.javaP\001',
    serialized_pb=b'\n\x15schedule_create.proto\x12\x05proto\x1a\x11\x62\x61sic_types.proto\x1a\x0ftimestamp.proto\x1a"schedulable_transaction_body.proto"\xfe\x01\n\x1dScheduleCreateTransactionBody\x12\x43\n\x18scheduledTransactionBody\x18\x01 \x01(\x0b\x32!.proto.SchedulableTransactionBody\x12\x0c\n\x04memo\x18\x02 \x01(\t\x12\x1c\n\x08\x61\x64minKey\x18\x03 \x01(\x0b\x32\n.proto.Key\x12(\n\x0epayerAccountID\x18\x04 \x01(\x0b\x32\x10.proto.AccountID\x12)\n\x0f\x65xpiration_time\x18\x05 \x01(\x0b\x32\x10.proto.Timestamp\x12\x17\n\x0fwait_for_expiry\x18\r \x01(\x08\x42&\n"com.hederahashgraph.api.proto.javaP\x01\x62\x06proto3',
    dependencies=[
        basic__types__pb2.DESCRIPTOR,
        timestamp__pb2.DESCRIPTOR,
        schedulable__transaction__body__pb2.DESCRIPTOR,
    ],
)


_SCHEDULECREATETRANSACTIONBODY = _descriptor.Descriptor(
    name="ScheduleCreateTransactionBody",
    full_name="proto.ScheduleCreateTransactionBody",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="scheduledTransactionBody",
            full_name="proto.ScheduleCreateTransactionBody.scheduledTransactionBody",
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
            name="memo",
            full_name="proto.ScheduleCreateTransactionBody.memo",
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
            name="adminKey",
            full_name="proto.ScheduleCreateTransactionBody.adminKey",
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
        _descriptor.FieldDescriptor(
            name="payerAccountID",
            full_name="proto.ScheduleCreateTransactionBody.payerAccountID",
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
            name="expiration_time",
            full_name="proto.ScheduleCreateTransactionBody.expiration_time",
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
            name="wait_for_expiry",
            full_name="proto.ScheduleCreateTransactionBody.wait_for_expiry",
            index=5,
            number=13,
            type=8,
            cpp_type=7,
            label=1,
            has_default_value=False,
            default_value=False,
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
    serialized_start=105,
    serialized_end=359,
)

_SCHEDULECREATETRANSACTIONBODY.fields_by_name[
    "scheduledTransactionBody"
].message_type = schedulable__transaction__body__pb2._SCHEDULABLETRANSACTIONBODY
_SCHEDULECREATETRANSACTIONBODY.fields_by_name["adminKey"].message_type = basic__types__pb2._KEY
_SCHEDULECREATETRANSACTIONBODY.fields_by_name["payerAccountID"].message_type = basic__types__pb2._ACCOUNTID
_SCHEDULECREATETRANSACTIONBODY.fields_by_name["expiration_time"].message_type = timestamp__pb2._TIMESTAMP
DESCRIPTOR.message_types_by_name["ScheduleCreateTransactionBody"] = _SCHEDULECREATETRANSACTIONBODY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ScheduleCreateTransactionBody = _reflection.GeneratedProtocolMessageType(
    "ScheduleCreateTransactionBody",
    (_message.Message,),
    {
        "DESCRIPTOR": _SCHEDULECREATETRANSACTIONBODY,
        "__module__": "schedule_create_pb2"
        # @@protoc_insertion_point(class_scope:proto.ScheduleCreateTransactionBody)
    },
)
_sym_db.RegisterMessage(ScheduleCreateTransactionBody)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
