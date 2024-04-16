# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: record_stream_file.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import enum_type_wrapper

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from hedera.util.proto_pb import basic_types_pb2 as basic__types__pb2
from hedera.util.proto_pb import hash_object_pb2 as hash__object__pb2
from hedera.util.proto_pb import transaction_pb2 as transaction__pb2
from hedera.util.proto_pb import transaction_record_pb2 as transaction__record__pb2

DESCRIPTOR = _descriptor.FileDescriptor(
    name="record_stream_file.proto",
    package="proto",
    syntax="proto3",
    serialized_options=b"\n com.hedera.services.stream.protoP\001",
    serialized_pb=b'\n\x18record_stream_file.proto\x12\x05proto\x1a\x11\x62\x61sic_types.proto\x1a\x11transaction.proto\x1a\x18transaction_record.proto\x1a\x11hash_object.proto"\xa6\x02\n\x10RecordStreamFile\x12\x32\n\x12hapi_proto_version\x18\x01 \x01(\x0b\x32\x16.proto.SemanticVersion\x12\x34\n\x19start_object_running_hash\x18\x02 \x01(\x0b\x32\x11.proto.HashObject\x12\x34\n\x13record_stream_items\x18\x03 \x03(\x0b\x32\x17.proto.RecordStreamItem\x12\x32\n\x17\x65nd_object_running_hash\x18\x04 \x01(\x0b\x32\x11.proto.HashObject\x12\x14\n\x0c\x62lock_number\x18\x05 \x01(\x03\x12(\n\x08sidecars\x18\x06 \x03(\x0b\x32\x16.proto.SidecarMetadata"e\n\x10RecordStreamItem\x12\'\n\x0btransaction\x18\x01 \x01(\x0b\x32\x12.proto.Transaction\x12(\n\x06record\x18\x02 \x01(\x0b\x32\x18.proto.TransactionRecord"a\n\x0fSidecarMetadata\x12\x1f\n\x04hash\x18\x01 \x01(\x0b\x32\x11.proto.HashObject\x12\n\n\x02id\x18\x02 \x01(\x05\x12!\n\x05types\x18\x03 \x03(\x0e\x32\x12.proto.SidecarType*B\n\x0bSidecarType\x12\x18\n\x14SIDECAR_TYPE_UNKNOWN\x10\x00\x12\x19\n\x15\x43ONTRACT_STATE_CHANGE\x10\x01\x42$\n com.hedera.services.stream.protoP\x01\x62\x06proto3',
    dependencies=[
        basic__types__pb2.DESCRIPTOR,
        transaction__pb2.DESCRIPTOR,
        transaction__record__pb2.DESCRIPTOR,
        hash__object__pb2.DESCRIPTOR,
    ],
)

_SIDECARTYPE = _descriptor.EnumDescriptor(
    name="SidecarType",
    full_name="proto.SidecarType",
    filename=None,
    file=DESCRIPTOR,
    values=[
        _descriptor.EnumValueDescriptor(
            name="SIDECAR_TYPE_UNKNOWN",
            index=0,
            number=0,
            serialized_options=None,
            type=None,
        ),
        _descriptor.EnumValueDescriptor(
            name="CONTRACT_STATE_CHANGE",
            index=1,
            number=1,
            serialized_options=None,
            type=None,
        ),
    ],
    containing_type=None,
    serialized_options=None,
    serialized_start=617,
    serialized_end=683,
)
_sym_db.RegisterEnumDescriptor(_SIDECARTYPE)

SidecarType = enum_type_wrapper.EnumTypeWrapper(_SIDECARTYPE)
SIDECAR_TYPE_UNKNOWN = 0
CONTRACT_STATE_CHANGE = 1


_RECORDSTREAMFILE = _descriptor.Descriptor(
    name="RecordStreamFile",
    full_name="proto.RecordStreamFile",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="hapi_proto_version",
            full_name="proto.RecordStreamFile.hapi_proto_version",
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
            name="start_object_running_hash",
            full_name="proto.RecordStreamFile.start_object_running_hash",
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
            name="record_stream_items",
            full_name="proto.RecordStreamFile.record_stream_items",
            index=2,
            number=3,
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
        _descriptor.FieldDescriptor(
            name="end_object_running_hash",
            full_name="proto.RecordStreamFile.end_object_running_hash",
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
            name="block_number",
            full_name="proto.RecordStreamFile.block_number",
            index=4,
            number=5,
            type=3,
            cpp_type=2,
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
            name="sidecars",
            full_name="proto.RecordStreamFile.sidecars",
            index=5,
            number=6,
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
    serialized_start=119,
    serialized_end=413,
)


_RECORDSTREAMITEM = _descriptor.Descriptor(
    name="RecordStreamItem",
    full_name="proto.RecordStreamItem",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="transaction",
            full_name="proto.RecordStreamItem.transaction",
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
            name="record",
            full_name="proto.RecordStreamItem.record",
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
    serialized_start=415,
    serialized_end=516,
)


_SIDECARMETADATA = _descriptor.Descriptor(
    name="SidecarMetadata",
    full_name="proto.SidecarMetadata",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="hash",
            full_name="proto.SidecarMetadata.hash",
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
            name="id",
            full_name="proto.SidecarMetadata.id",
            index=1,
            number=2,
            type=5,
            cpp_type=1,
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
            name="types",
            full_name="proto.SidecarMetadata.types",
            index=2,
            number=3,
            type=14,
            cpp_type=8,
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
    serialized_start=518,
    serialized_end=615,
)

_RECORDSTREAMFILE.fields_by_name["hapi_proto_version"].message_type = basic__types__pb2._SEMANTICVERSION
_RECORDSTREAMFILE.fields_by_name["start_object_running_hash"].message_type = hash__object__pb2._HASHOBJECT
_RECORDSTREAMFILE.fields_by_name["record_stream_items"].message_type = _RECORDSTREAMITEM
_RECORDSTREAMFILE.fields_by_name["end_object_running_hash"].message_type = hash__object__pb2._HASHOBJECT
_RECORDSTREAMFILE.fields_by_name["sidecars"].message_type = _SIDECARMETADATA
_RECORDSTREAMITEM.fields_by_name["transaction"].message_type = transaction__pb2._TRANSACTION
_RECORDSTREAMITEM.fields_by_name["record"].message_type = transaction__record__pb2._TRANSACTIONRECORD
_SIDECARMETADATA.fields_by_name["hash"].message_type = hash__object__pb2._HASHOBJECT
_SIDECARMETADATA.fields_by_name["types"].enum_type = _SIDECARTYPE
DESCRIPTOR.message_types_by_name["RecordStreamFile"] = _RECORDSTREAMFILE
DESCRIPTOR.message_types_by_name["RecordStreamItem"] = _RECORDSTREAMITEM
DESCRIPTOR.message_types_by_name["SidecarMetadata"] = _SIDECARMETADATA
DESCRIPTOR.enum_types_by_name["SidecarType"] = _SIDECARTYPE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

RecordStreamFile = _reflection.GeneratedProtocolMessageType(
    "RecordStreamFile",
    (_message.Message,),
    {
        "DESCRIPTOR": _RECORDSTREAMFILE,
        "__module__": "record_stream_file_pb2"
        # @@protoc_insertion_point(class_scope:proto.RecordStreamFile)
    },
)
_sym_db.RegisterMessage(RecordStreamFile)

RecordStreamItem = _reflection.GeneratedProtocolMessageType(
    "RecordStreamItem",
    (_message.Message,),
    {
        "DESCRIPTOR": _RECORDSTREAMITEM,
        "__module__": "record_stream_file_pb2"
        # @@protoc_insertion_point(class_scope:proto.RecordStreamItem)
    },
)
_sym_db.RegisterMessage(RecordStreamItem)

SidecarMetadata = _reflection.GeneratedProtocolMessageType(
    "SidecarMetadata",
    (_message.Message,),
    {
        "DESCRIPTOR": _SIDECARMETADATA,
        "__module__": "record_stream_file_pb2"
        # @@protoc_insertion_point(class_scope:proto.SidecarMetadata)
    },
)
_sym_db.RegisterMessage(SidecarMetadata)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
