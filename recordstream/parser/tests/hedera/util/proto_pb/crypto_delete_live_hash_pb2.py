# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: crypto_delete_live_hash.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from hedera.util.proto_pb import basic_types_pb2 as basic__types__pb2

DESCRIPTOR = _descriptor.FileDescriptor(
    name="crypto_delete_live_hash.proto",
    package="proto",
    syntax="proto3",
    serialized_options=b'\n"com.hederahashgraph.api.proto.javaP\001',
    serialized_pb=b'\n\x1d\x63rypto_delete_live_hash.proto\x12\x05proto\x1a\x11\x62\x61sic_types.proto"l\n#CryptoDeleteLiveHashTransactionBody\x12+\n\x11\x61\x63\x63ountOfLiveHash\x18\x01 \x01(\x0b\x32\x10.proto.AccountID\x12\x18\n\x10liveHashToDelete\x18\x02 \x01(\x0c\x42&\n"com.hederahashgraph.api.proto.javaP\x01\x62\x06proto3',
    dependencies=[
        basic__types__pb2.DESCRIPTOR,
    ],
)


_CRYPTODELETELIVEHASHTRANSACTIONBODY = _descriptor.Descriptor(
    name="CryptoDeleteLiveHashTransactionBody",
    full_name="proto.CryptoDeleteLiveHashTransactionBody",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="accountOfLiveHash",
            full_name="proto.CryptoDeleteLiveHashTransactionBody.accountOfLiveHash",
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
            name="liveHashToDelete",
            full_name="proto.CryptoDeleteLiveHashTransactionBody.liveHashToDelete",
            index=1,
            number=2,
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
    serialized_start=59,
    serialized_end=167,
)

_CRYPTODELETELIVEHASHTRANSACTIONBODY.fields_by_name["accountOfLiveHash"].message_type = basic__types__pb2._ACCOUNTID
DESCRIPTOR.message_types_by_name["CryptoDeleteLiveHashTransactionBody"] = _CRYPTODELETELIVEHASHTRANSACTIONBODY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

CryptoDeleteLiveHashTransactionBody = _reflection.GeneratedProtocolMessageType(
    "CryptoDeleteLiveHashTransactionBody",
    (_message.Message,),
    {
        "DESCRIPTOR": _CRYPTODELETELIVEHASHTRANSACTIONBODY,
        "__module__": "crypto_delete_live_hash_pb2"
        # @@protoc_insertion_point(class_scope:proto.CryptoDeleteLiveHashTransactionBody)
    },
)
_sym_db.RegisterMessage(CryptoDeleteLiveHashTransactionBody)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
