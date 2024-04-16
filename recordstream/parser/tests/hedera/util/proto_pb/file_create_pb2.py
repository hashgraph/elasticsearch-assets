# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: file_create.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from hedera.util.proto_pb import basic_types_pb2 as basic__types__pb2
from hedera.util.proto_pb import timestamp_pb2 as timestamp__pb2

DESCRIPTOR = _descriptor.FileDescriptor(
    name="file_create.proto",
    package="proto",
    syntax="proto3",
    serialized_options=b'\n"com.hederahashgraph.api.proto.javaP\001',
    serialized_pb=b'\n\x11\x66ile_create.proto\x12\x05proto\x1a\x11\x62\x61sic_types.proto\x1a\x0ftimestamp.proto"\xeb\x01\n\x19\x46ileCreateTransactionBody\x12(\n\x0e\x65xpirationTime\x18\x02 \x01(\x0b\x32\x10.proto.Timestamp\x12\x1c\n\x04keys\x18\x03 \x01(\x0b\x32\x0e.proto.KeyList\x12\x10\n\x08\x63ontents\x18\x04 \x01(\x0c\x12\x1f\n\x07shardID\x18\x05 \x01(\x0b\x32\x0e.proto.ShardID\x12\x1f\n\x07realmID\x18\x06 \x01(\x0b\x32\x0e.proto.RealmID\x12$\n\x10newRealmAdminKey\x18\x07 \x01(\x0b\x32\n.proto.Key\x12\x0c\n\x04memo\x18\x08 \x01(\tB&\n"com.hederahashgraph.api.proto.javaP\x01\x62\x06proto3',
    dependencies=[
        basic__types__pb2.DESCRIPTOR,
        timestamp__pb2.DESCRIPTOR,
    ],
)


_FILECREATETRANSACTIONBODY = _descriptor.Descriptor(
    name="FileCreateTransactionBody",
    full_name="proto.FileCreateTransactionBody",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="expirationTime",
            full_name="proto.FileCreateTransactionBody.expirationTime",
            index=0,
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
            name="keys",
            full_name="proto.FileCreateTransactionBody.keys",
            index=1,
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
            name="contents",
            full_name="proto.FileCreateTransactionBody.contents",
            index=2,
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
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="shardID",
            full_name="proto.FileCreateTransactionBody.shardID",
            index=3,
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
            name="realmID",
            full_name="proto.FileCreateTransactionBody.realmID",
            index=4,
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
            name="newRealmAdminKey",
            full_name="proto.FileCreateTransactionBody.newRealmAdminKey",
            index=5,
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
            name="memo",
            full_name="proto.FileCreateTransactionBody.memo",
            index=6,
            number=8,
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
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=65,
    serialized_end=300,
)

_FILECREATETRANSACTIONBODY.fields_by_name["expirationTime"].message_type = timestamp__pb2._TIMESTAMP
_FILECREATETRANSACTIONBODY.fields_by_name["keys"].message_type = basic__types__pb2._KEYLIST
_FILECREATETRANSACTIONBODY.fields_by_name["shardID"].message_type = basic__types__pb2._SHARDID
_FILECREATETRANSACTIONBODY.fields_by_name["realmID"].message_type = basic__types__pb2._REALMID
_FILECREATETRANSACTIONBODY.fields_by_name["newRealmAdminKey"].message_type = basic__types__pb2._KEY
DESCRIPTOR.message_types_by_name["FileCreateTransactionBody"] = _FILECREATETRANSACTIONBODY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

FileCreateTransactionBody = _reflection.GeneratedProtocolMessageType(
    "FileCreateTransactionBody",
    (_message.Message,),
    {
        "DESCRIPTOR": _FILECREATETRANSACTIONBODY,
        "__module__": "file_create_pb2"
        # @@protoc_insertion_point(class_scope:proto.FileCreateTransactionBody)
    },
)
_sym_db.RegisterMessage(FileCreateTransactionBody)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
