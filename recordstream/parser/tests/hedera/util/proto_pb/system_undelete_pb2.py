# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: system_undelete.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from hedera.util.proto_pb import basic_types_pb2 as basic__types__pb2

DESCRIPTOR = _descriptor.FileDescriptor(
    name="system_undelete.proto",
    package="proto",
    syntax="proto3",
    serialized_options=b'\n"com.hederahashgraph.api.proto.javaP\001',
    serialized_pb=b'\n\x15system_undelete.proto\x12\x05proto\x1a\x11\x62\x61sic_types.proto"o\n\x1dSystemUndeleteTransactionBody\x12\x1f\n\x06\x66ileID\x18\x01 \x01(\x0b\x32\r.proto.FileIDH\x00\x12\'\n\ncontractID\x18\x02 \x01(\x0b\x32\x11.proto.ContractIDH\x00\x42\x04\n\x02idB&\n"com.hederahashgraph.api.proto.javaP\x01\x62\x06proto3',
    dependencies=[
        basic__types__pb2.DESCRIPTOR,
    ],
)


_SYSTEMUNDELETETRANSACTIONBODY = _descriptor.Descriptor(
    name="SystemUndeleteTransactionBody",
    full_name="proto.SystemUndeleteTransactionBody",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="fileID",
            full_name="proto.SystemUndeleteTransactionBody.fileID",
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
            name="contractID",
            full_name="proto.SystemUndeleteTransactionBody.contractID",
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
    oneofs=[
        _descriptor.OneofDescriptor(
            name="id",
            full_name="proto.SystemUndeleteTransactionBody.id",
            index=0,
            containing_type=None,
            fields=[],
        ),
    ],
    serialized_start=51,
    serialized_end=162,
)

_SYSTEMUNDELETETRANSACTIONBODY.fields_by_name["fileID"].message_type = basic__types__pb2._FILEID
_SYSTEMUNDELETETRANSACTIONBODY.fields_by_name["contractID"].message_type = basic__types__pb2._CONTRACTID
_SYSTEMUNDELETETRANSACTIONBODY.oneofs_by_name["id"].fields.append(
    _SYSTEMUNDELETETRANSACTIONBODY.fields_by_name["fileID"]
)
_SYSTEMUNDELETETRANSACTIONBODY.fields_by_name["fileID"].containing_oneof = _SYSTEMUNDELETETRANSACTIONBODY.oneofs_by_name[
    "id"
]
_SYSTEMUNDELETETRANSACTIONBODY.oneofs_by_name["id"].fields.append(
    _SYSTEMUNDELETETRANSACTIONBODY.fields_by_name["contractID"]
)
_SYSTEMUNDELETETRANSACTIONBODY.fields_by_name[
    "contractID"
].containing_oneof = _SYSTEMUNDELETETRANSACTIONBODY.oneofs_by_name["id"]
DESCRIPTOR.message_types_by_name["SystemUndeleteTransactionBody"] = _SYSTEMUNDELETETRANSACTIONBODY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

SystemUndeleteTransactionBody = _reflection.GeneratedProtocolMessageType(
    "SystemUndeleteTransactionBody",
    (_message.Message,),
    {
        "DESCRIPTOR": _SYSTEMUNDELETETRANSACTIONBODY,
        "__module__": "system_undelete_pb2"
        # @@protoc_insertion_point(class_scope:proto.SystemUndeleteTransactionBody)
    },
)
_sym_db.RegisterMessage(SystemUndeleteTransactionBody)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
