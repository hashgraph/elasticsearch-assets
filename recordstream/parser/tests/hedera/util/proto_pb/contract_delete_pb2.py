# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: contract_delete.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from hedera.util.proto_pb import basic_types_pb2 as basic__types__pb2

DESCRIPTOR = _descriptor.FileDescriptor(
    name="contract_delete.proto",
    package="proto",
    syntax="proto3",
    serialized_options=b'\n"com.hederahashgraph.api.proto.javaP\001',
    serialized_pb=b'\n\x15\x63ontract_delete.proto\x12\x05proto\x1a\x11\x62\x61sic_types.proto"\xce\x01\n\x1d\x43ontractDeleteTransactionBody\x12%\n\ncontractID\x18\x01 \x01(\x0b\x32\x11.proto.ContractID\x12-\n\x11transferAccountID\x18\x02 \x01(\x0b\x32\x10.proto.AccountIDH\x00\x12/\n\x12transferContractID\x18\x03 \x01(\x0b\x32\x11.proto.ContractIDH\x00\x12\x19\n\x11permanent_removal\x18\x04 \x01(\x08\x42\x0b\n\tobtainersB&\n"com.hederahashgraph.api.proto.javaP\x01\x62\x06proto3',
    dependencies=[
        basic__types__pb2.DESCRIPTOR,
    ],
)


_CONTRACTDELETETRANSACTIONBODY = _descriptor.Descriptor(
    name="ContractDeleteTransactionBody",
    full_name="proto.ContractDeleteTransactionBody",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="contractID",
            full_name="proto.ContractDeleteTransactionBody.contractID",
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
            name="transferAccountID",
            full_name="proto.ContractDeleteTransactionBody.transferAccountID",
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
            name="transferContractID",
            full_name="proto.ContractDeleteTransactionBody.transferContractID",
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
            name="permanent_removal",
            full_name="proto.ContractDeleteTransactionBody.permanent_removal",
            index=3,
            number=4,
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
    oneofs=[
        _descriptor.OneofDescriptor(
            name="obtainers",
            full_name="proto.ContractDeleteTransactionBody.obtainers",
            index=0,
            containing_type=None,
            fields=[],
        ),
    ],
    serialized_start=52,
    serialized_end=258,
)

_CONTRACTDELETETRANSACTIONBODY.fields_by_name["contractID"].message_type = basic__types__pb2._CONTRACTID
_CONTRACTDELETETRANSACTIONBODY.fields_by_name["transferAccountID"].message_type = basic__types__pb2._ACCOUNTID
_CONTRACTDELETETRANSACTIONBODY.fields_by_name["transferContractID"].message_type = basic__types__pb2._CONTRACTID
_CONTRACTDELETETRANSACTIONBODY.oneofs_by_name["obtainers"].fields.append(
    _CONTRACTDELETETRANSACTIONBODY.fields_by_name["transferAccountID"]
)
_CONTRACTDELETETRANSACTIONBODY.fields_by_name[
    "transferAccountID"
].containing_oneof = _CONTRACTDELETETRANSACTIONBODY.oneofs_by_name["obtainers"]
_CONTRACTDELETETRANSACTIONBODY.oneofs_by_name["obtainers"].fields.append(
    _CONTRACTDELETETRANSACTIONBODY.fields_by_name["transferContractID"]
)
_CONTRACTDELETETRANSACTIONBODY.fields_by_name[
    "transferContractID"
].containing_oneof = _CONTRACTDELETETRANSACTIONBODY.oneofs_by_name["obtainers"]
DESCRIPTOR.message_types_by_name["ContractDeleteTransactionBody"] = _CONTRACTDELETETRANSACTIONBODY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ContractDeleteTransactionBody = _reflection.GeneratedProtocolMessageType(
    "ContractDeleteTransactionBody",
    (_message.Message,),
    {
        "DESCRIPTOR": _CONTRACTDELETETRANSACTIONBODY,
        "__module__": "contract_delete_pb2"
        # @@protoc_insertion_point(class_scope:proto.ContractDeleteTransactionBody)
    },
)
_sym_db.RegisterMessage(ContractDeleteTransactionBody)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
