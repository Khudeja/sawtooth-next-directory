# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proposal_transaction.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='proposal_transaction.proto',
  package='',
  syntax='proto3',
  serialized_pb=_b('\n\x1aproposal_transaction.proto\"X\n\x0eUpdateProposal\x12\x13\n\x0bproposal_id\x18\x01 \x01(\t\x12\x1b\n\x13old_metadata_sha512\x18\x02 \x01(\t\x12\x14\n\x0cnew_metadata\x18\x03 \x01(\tb\x06proto3')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_UPDATEPROPOSAL = _descriptor.Descriptor(
  name='UpdateProposal',
  full_name='UpdateProposal',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='proposal_id', full_name='UpdateProposal.proposal_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='old_metadata_sha512', full_name='UpdateProposal.old_metadata_sha512', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='new_metadata', full_name='UpdateProposal.new_metadata', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=30,
  serialized_end=118,
)

DESCRIPTOR.message_types_by_name['UpdateProposal'] = _UPDATEPROPOSAL

UpdateProposal = _reflection.GeneratedProtocolMessageType('UpdateProposal', (_message.Message,), dict(
  DESCRIPTOR = _UPDATEPROPOSAL,
  __module__ = 'proposal_transaction_pb2'
  # @@protoc_insertion_point(class_scope:UpdateProposal)
  ))
_sym_db.RegisterMessage(UpdateProposal)


# @@protoc_insertion_point(module_scope)