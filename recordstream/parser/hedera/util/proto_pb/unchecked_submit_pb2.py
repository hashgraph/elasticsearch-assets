# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: unchecked_submit.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor.FileDescriptor(
    name="unchecked_submit.proto",
    package="proto",
    syntax="proto3",
    serialized_options=b'\n"com.hederahashgraph.api.proto.javaP\001',
    serialized_pb=b'\n\x16unchecked_submit.proto\x12\x05proto"/\n\x13UncheckedSubmitBody\x12\x18\n\x10transactionBytes\x18\x01 \x01(\x0c\x42&\n"com.hederahashgraph.api.proto.javaP\x01\x62\x06proto3',
)


_UNCHECKEDSUBMITBODY = _descriptor.Descriptor(
    name="UncheckedSubmitBody",
    full_name="proto.UncheckedSubmitBody",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="transactionBytes",
            full_name="proto.UncheckedSubmitBody.transactionBytes",
            index=0,
            number=1,
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
    serialized_start=33,
    serialized_end=80,
)

DESCRIPTOR.message_types_by_name["UncheckedSubmitBody"] = _UNCHECKEDSUBMITBODY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

UncheckedSubmitBody = _reflection.GeneratedProtocolMessageType(
    "UncheckedSubmitBody",
    (_message.Message,),
    {
        "DESCRIPTOR": _UNCHECKEDSUBMITBODY,
        "__module__": "unchecked_submit_pb2"
        # @@protoc_insertion_point(class_scope:proto.UncheckedSubmitBody)
    },
)
_sym_db.RegisterMessage(UncheckedSubmitBody)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
