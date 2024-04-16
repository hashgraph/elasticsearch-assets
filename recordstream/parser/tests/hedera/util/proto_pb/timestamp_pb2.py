# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: timestamp.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor.FileDescriptor(
    name="timestamp.proto",
    package="proto",
    syntax="proto3",
    serialized_options=b'\n"com.hederahashgraph.api.proto.javaP\001',
    serialized_pb=b'\n\x0ftimestamp.proto\x12\x05proto"+\n\tTimestamp\x12\x0f\n\x07seconds\x18\x01 \x01(\x03\x12\r\n\x05nanos\x18\x02 \x01(\x05"#\n\x10TimestampSeconds\x12\x0f\n\x07seconds\x18\x01 \x01(\x03\x42&\n"com.hederahashgraph.api.proto.javaP\x01\x62\x06proto3',
)


_TIMESTAMP = _descriptor.Descriptor(
    name="Timestamp",
    full_name="proto.Timestamp",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="seconds",
            full_name="proto.Timestamp.seconds",
            index=0,
            number=1,
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
            name="nanos",
            full_name="proto.Timestamp.nanos",
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
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=26,
    serialized_end=69,
)


_TIMESTAMPSECONDS = _descriptor.Descriptor(
    name="TimestampSeconds",
    full_name="proto.TimestampSeconds",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="seconds",
            full_name="proto.TimestampSeconds.seconds",
            index=0,
            number=1,
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
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=71,
    serialized_end=106,
)

DESCRIPTOR.message_types_by_name["Timestamp"] = _TIMESTAMP
DESCRIPTOR.message_types_by_name["TimestampSeconds"] = _TIMESTAMPSECONDS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Timestamp = _reflection.GeneratedProtocolMessageType(
    "Timestamp",
    (_message.Message,),
    {
        "DESCRIPTOR": _TIMESTAMP,
        "__module__": "timestamp_pb2"
        # @@protoc_insertion_point(class_scope:proto.Timestamp)
    },
)
_sym_db.RegisterMessage(Timestamp)

TimestampSeconds = _reflection.GeneratedProtocolMessageType(
    "TimestampSeconds",
    (_message.Message,),
    {
        "DESCRIPTOR": _TIMESTAMPSECONDS,
        "__module__": "timestamp_pb2"
        # @@protoc_insertion_point(class_scope:proto.TimestampSeconds)
    },
)
_sym_db.RegisterMessage(TimestampSeconds)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
