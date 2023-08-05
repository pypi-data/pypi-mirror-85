# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: LaunchConfigurations.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='LaunchConfigurations.proto',
  package='geistt.rti',
  syntax='proto3',
  serialized_options=_b('\252\002\024GEISTT.Lab.RTI.Proto'),
  serialized_pb=_b('\n\x1aLaunchConfigurations.proto\x12\ngeistt.rti\x1a\x1bgoogle/protobuf/empty.proto\"\xce\x03\n\x14LaunchConfigurations\x12\x38\n\x16request_configurations\x18\x01 \x01(\x0b\x32\x16.google.protobuf.EmptyH\x00\x12M\n\rconfiguration\x18\x02 \x01(\x0b\x32\x34.geistt.rti.LaunchConfigurations.LaunchConfigurationH\x00\x12T\n\x14\x61\x63tive_configuration\x18\x03 \x01(\x0b\x32\x34.geistt.rti.LaunchConfigurations.LaunchConfigurationH\x00\x1ax\n\x13LaunchConfiguration\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t\x12>\n\nparameters\x18\x03 \x03(\x0b\x32*.geistt.rti.LaunchConfigurations.Parameter\x1aT\n\tParameter\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\r\n\x05label\x18\x02 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t\x12\x15\n\rdefault_value\x18\x04 \x01(\tB\x07\n\x05whichB\x17\xaa\x02\x14GEISTT.Lab.RTI.Protob\x06proto3')
  ,
  dependencies=[google_dot_protobuf_dot_empty__pb2.DESCRIPTOR,])




_LAUNCHCONFIGURATIONS_LAUNCHCONFIGURATION = _descriptor.Descriptor(
  name='LaunchConfiguration',
  full_name='geistt.rti.LaunchConfigurations.LaunchConfiguration',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='geistt.rti.LaunchConfigurations.LaunchConfiguration.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='description', full_name='geistt.rti.LaunchConfigurations.LaunchConfiguration.description', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='parameters', full_name='geistt.rti.LaunchConfigurations.LaunchConfiguration.parameters', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=319,
  serialized_end=439,
)

_LAUNCHCONFIGURATIONS_PARAMETER = _descriptor.Descriptor(
  name='Parameter',
  full_name='geistt.rti.LaunchConfigurations.Parameter',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='geistt.rti.LaunchConfigurations.Parameter.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='label', full_name='geistt.rti.LaunchConfigurations.Parameter.label', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='description', full_name='geistt.rti.LaunchConfigurations.Parameter.description', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='default_value', full_name='geistt.rti.LaunchConfigurations.Parameter.default_value', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=441,
  serialized_end=525,
)

_LAUNCHCONFIGURATIONS = _descriptor.Descriptor(
  name='LaunchConfigurations',
  full_name='geistt.rti.LaunchConfigurations',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='request_configurations', full_name='geistt.rti.LaunchConfigurations.request_configurations', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='configuration', full_name='geistt.rti.LaunchConfigurations.configuration', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='active_configuration', full_name='geistt.rti.LaunchConfigurations.active_configuration', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_LAUNCHCONFIGURATIONS_LAUNCHCONFIGURATION, _LAUNCHCONFIGURATIONS_PARAMETER, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='which', full_name='geistt.rti.LaunchConfigurations.which',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=72,
  serialized_end=534,
)

_LAUNCHCONFIGURATIONS_LAUNCHCONFIGURATION.fields_by_name['parameters'].message_type = _LAUNCHCONFIGURATIONS_PARAMETER
_LAUNCHCONFIGURATIONS_LAUNCHCONFIGURATION.containing_type = _LAUNCHCONFIGURATIONS
_LAUNCHCONFIGURATIONS_PARAMETER.containing_type = _LAUNCHCONFIGURATIONS
_LAUNCHCONFIGURATIONS.fields_by_name['request_configurations'].message_type = google_dot_protobuf_dot_empty__pb2._EMPTY
_LAUNCHCONFIGURATIONS.fields_by_name['configuration'].message_type = _LAUNCHCONFIGURATIONS_LAUNCHCONFIGURATION
_LAUNCHCONFIGURATIONS.fields_by_name['active_configuration'].message_type = _LAUNCHCONFIGURATIONS_LAUNCHCONFIGURATION
_LAUNCHCONFIGURATIONS.oneofs_by_name['which'].fields.append(
  _LAUNCHCONFIGURATIONS.fields_by_name['request_configurations'])
_LAUNCHCONFIGURATIONS.fields_by_name['request_configurations'].containing_oneof = _LAUNCHCONFIGURATIONS.oneofs_by_name['which']
_LAUNCHCONFIGURATIONS.oneofs_by_name['which'].fields.append(
  _LAUNCHCONFIGURATIONS.fields_by_name['configuration'])
_LAUNCHCONFIGURATIONS.fields_by_name['configuration'].containing_oneof = _LAUNCHCONFIGURATIONS.oneofs_by_name['which']
_LAUNCHCONFIGURATIONS.oneofs_by_name['which'].fields.append(
  _LAUNCHCONFIGURATIONS.fields_by_name['active_configuration'])
_LAUNCHCONFIGURATIONS.fields_by_name['active_configuration'].containing_oneof = _LAUNCHCONFIGURATIONS.oneofs_by_name['which']
DESCRIPTOR.message_types_by_name['LaunchConfigurations'] = _LAUNCHCONFIGURATIONS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

LaunchConfigurations = _reflection.GeneratedProtocolMessageType('LaunchConfigurations', (_message.Message,), dict(

  LaunchConfiguration = _reflection.GeneratedProtocolMessageType('LaunchConfiguration', (_message.Message,), dict(
    DESCRIPTOR = _LAUNCHCONFIGURATIONS_LAUNCHCONFIGURATION,
    __module__ = 'LaunchConfigurations_pb2'
    # @@protoc_insertion_point(class_scope:geistt.rti.LaunchConfigurations.LaunchConfiguration)
    ))
  ,

  Parameter = _reflection.GeneratedProtocolMessageType('Parameter', (_message.Message,), dict(
    DESCRIPTOR = _LAUNCHCONFIGURATIONS_PARAMETER,
    __module__ = 'LaunchConfigurations_pb2'
    # @@protoc_insertion_point(class_scope:geistt.rti.LaunchConfigurations.Parameter)
    ))
  ,
  DESCRIPTOR = _LAUNCHCONFIGURATIONS,
  __module__ = 'LaunchConfigurations_pb2'
  # @@protoc_insertion_point(class_scope:geistt.rti.LaunchConfigurations)
  ))
_sym_db.RegisterMessage(LaunchConfigurations)
_sym_db.RegisterMessage(LaunchConfigurations.LaunchConfiguration)
_sym_db.RegisterMessage(LaunchConfigurations.Parameter)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
