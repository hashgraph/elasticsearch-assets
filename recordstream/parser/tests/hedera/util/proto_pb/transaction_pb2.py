# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: transaction.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from hedera.util.proto_pb import basic_types_pb2 as basic__types__pb2
from hedera.util.proto_pb import duration_pb2 as duration__pb2
from hedera.util.proto_pb import transaction_body_pb2 as transaction__body__pb2

DESCRIPTOR = _descriptor.FileDescriptor(
    name="transaction.proto",
    package="proto",
    syntax="proto3",
    serialized_options=b'\n"com.hederahashgraph.api.proto.javaP\001',
    serialized_pb=b'\n\x11transaction.proto\x12\x05proto\x1a\x0e\x64uration.proto\x1a\x11\x62\x61sic_types.proto\x1a\x16transaction_body.proto"\xbf\x01\n\x0bTransaction\x12(\n\x04\x62ody\x18\x01 \x01(\x0b\x32\x16.proto.TransactionBodyB\x02\x18\x01\x12&\n\x04sigs\x18\x02 \x01(\x0b\x32\x14.proto.SignatureListB\x02\x18\x01\x12\'\n\x06sigMap\x18\x03 \x01(\x0b\x32\x13.proto.SignatureMapB\x02\x18\x01\x12\x15\n\tbodyBytes\x18\x04 \x01(\x0c\x42\x02\x18\x01\x12\x1e\n\x16signedTransactionBytes\x18\x05 \x01(\x0c\x42&\n"com.hederahashgraph.api.proto.javaP\x01\x62\x06proto3',
    dependencies=[
        duration__pb2.DESCRIPTOR,
        basic__types__pb2.DESCRIPTOR,
        transaction__body__pb2.DESCRIPTOR,
    ],
)


_TRANSACTION = _descriptor.Descriptor(
    name="Transaction",
    full_name="proto.Transaction",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="body",
            full_name="proto.Transaction.body",
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
            serialized_options=b"\030\001",
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="sigs",
            full_name="proto.Transaction.sigs",
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
            serialized_options=b"\030\001",
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="sigMap",
            full_name="proto.Transaction.sigMap",
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
            serialized_options=b"\030\001",
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="bodyBytes",
            full_name="proto.Transaction.bodyBytes",
            index=3,
            number=4,
            type=12,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"",
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=b"\030\001",
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="signedTransactionBytes",
            full_name="proto.Transaction.signedTransactionBytes",
            index=4,
            number=5,
            type=12,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"",
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
    serialized_start=88,
    serialized_end=279,
)

_TRANSACTION.fields_by_name["body"].message_type = transaction__body__pb2._TRANSACTIONBODY
_TRANSACTION.fields_by_name["sigs"].message_type = basic__types__pb2._SIGNATURELIST
_TRANSACTION.fields_by_name["sigMap"].message_type = basic__types__pb2._SIGNATUREMAP
DESCRIPTOR.message_types_by_name["Transaction"] = _TRANSACTION
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Transaction = _reflection.GeneratedProtocolMessageType(
    "Transaction",
    (_message.Message,),
    {
        "DESCRIPTOR": _TRANSACTION,
        "__module__": "transaction_pb2"
        # @@protoc_insertion_point(class_scope:proto.Transaction)
    },
)
_sym_db.RegisterMessage(Transaction)


DESCRIPTOR._options = None
_TRANSACTION.fields_by_name["body"]._options = None
_TRANSACTION.fields_by_name["sigs"]._options = None
_TRANSACTION.fields_by_name["sigMap"]._options = None
_TRANSACTION.fields_by_name["bodyBytes"]._options = None
# @@protoc_insertion_point(module_scope)
