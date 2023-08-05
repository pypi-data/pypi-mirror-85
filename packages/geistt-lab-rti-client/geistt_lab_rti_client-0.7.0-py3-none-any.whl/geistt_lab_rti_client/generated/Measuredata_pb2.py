# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: Measuredata.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import Measures_pb2 as Measures__pb2
from . import Measurement_pb2 as Measurement__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='Measuredata.proto',
  package='geistt.rti',
  syntax='proto3',
  serialized_options=_b('\252\002\024GEISTT.Lab.RTI.Proto'),
  serialized_pb=_b('\n\x11Measuredata.proto\x12\ngeistt.rti\x1a\x0eMeasures.proto\x1a\x11Measurement.proto\"\xe4\x04\n\x0bMeasuredata\x12\x32\n\x07request\x18\x01 \x01(\x0b\x32\x1f.geistt.rti.Measuredata.RequestH\x00\x12\x34\n\x08response\x18\x02 \x01(\x0b\x32 .geistt.rti.Measuredata.ResponseH\x00\x1a\x96\x01\n\x07Request\x12\x18\n\x10response_channel\x18\x01 \x01(\t\x12\x10\n\x08measures\x18\x02 \x03(\t\x12\x11\n\tinstances\x18\x03 \x03(\t\x12\x14\n\x0c\x61pplications\x18\x04 \x03(\t\x12\x11\n\tfrom_time\x18\x08 \x01(\x01\x12\x0f\n\x07to_time\x18\t \x01(\x01\x12\x12\n\nresolution\x18\n \x01(\x01\x1a\x45\n\x08Response\x12\x39\n\x08measures\x18\x01 \x03(\x0b\x32\'.geistt.rti.Measuredata.MeasureResponse\x1a\x94\x01\n\x0fMeasureResponse\x12-\n\x07measure\x18\x01 \x01(\x0b\x32\x1c.geistt.rti.Measures.Measure\x12\x13\n\x0binstance_id\x18\x02 \x01(\t\x12=\n\x0cmeasurements\x18\x03 \x03(\x0b\x32\'.geistt.rti.Measuredata.MeasurementData\x1ak\n\x0fMeasurementData\x12\x0c\n\x04time\x18\x01 \x01(\x01\x12\x0f\n\x05value\x18\x03 \x01(\x02H\x00\x12\x30\n\x06window\x18\x04 \x01(\x0b\x32\x1e.geistt.rti.Measurement.WindowH\x00\x42\x07\n\x05whichB\x07\n\x05whichB\x17\xaa\x02\x14GEISTT.Lab.RTI.Protob\x06proto3')
  ,
  dependencies=[Measures__pb2.DESCRIPTOR,Measurement__pb2.DESCRIPTOR,])




_MEASUREDATA_REQUEST = _descriptor.Descriptor(
  name='Request',
  full_name='geistt.rti.Measuredata.Request',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='response_channel', full_name='geistt.rti.Measuredata.Request.response_channel', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='measures', full_name='geistt.rti.Measuredata.Request.measures', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='instances', full_name='geistt.rti.Measuredata.Request.instances', index=2,
      number=3, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='applications', full_name='geistt.rti.Measuredata.Request.applications', index=3,
      number=4, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='from_time', full_name='geistt.rti.Measuredata.Request.from_time', index=4,
      number=8, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='to_time', full_name='geistt.rti.Measuredata.Request.to_time', index=5,
      number=9, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='resolution', full_name='geistt.rti.Measuredata.Request.resolution', index=6,
      number=10, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
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
  serialized_start=191,
  serialized_end=341,
)

_MEASUREDATA_RESPONSE = _descriptor.Descriptor(
  name='Response',
  full_name='geistt.rti.Measuredata.Response',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='measures', full_name='geistt.rti.Measuredata.Response.measures', index=0,
      number=1, type=11, cpp_type=10, label=3,
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
  serialized_start=343,
  serialized_end=412,
)

_MEASUREDATA_MEASURERESPONSE = _descriptor.Descriptor(
  name='MeasureResponse',
  full_name='geistt.rti.Measuredata.MeasureResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='measure', full_name='geistt.rti.Measuredata.MeasureResponse.measure', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='instance_id', full_name='geistt.rti.Measuredata.MeasureResponse.instance_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='measurements', full_name='geistt.rti.Measuredata.MeasureResponse.measurements', index=2,
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
  serialized_start=415,
  serialized_end=563,
)

_MEASUREDATA_MEASUREMENTDATA = _descriptor.Descriptor(
  name='MeasurementData',
  full_name='geistt.rti.Measuredata.MeasurementData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='time', full_name='geistt.rti.Measuredata.MeasurementData.time', index=0,
      number=1, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='geistt.rti.Measuredata.MeasurementData.value', index=1,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='window', full_name='geistt.rti.Measuredata.MeasurementData.window', index=2,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
    _descriptor.OneofDescriptor(
      name='which', full_name='geistt.rti.Measuredata.MeasurementData.which',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=565,
  serialized_end=672,
)

_MEASUREDATA = _descriptor.Descriptor(
  name='Measuredata',
  full_name='geistt.rti.Measuredata',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='request', full_name='geistt.rti.Measuredata.request', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='response', full_name='geistt.rti.Measuredata.response', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_MEASUREDATA_REQUEST, _MEASUREDATA_RESPONSE, _MEASUREDATA_MEASURERESPONSE, _MEASUREDATA_MEASUREMENTDATA, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='which', full_name='geistt.rti.Measuredata.which',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=69,
  serialized_end=681,
)

_MEASUREDATA_REQUEST.containing_type = _MEASUREDATA
_MEASUREDATA_RESPONSE.fields_by_name['measures'].message_type = _MEASUREDATA_MEASURERESPONSE
_MEASUREDATA_RESPONSE.containing_type = _MEASUREDATA
_MEASUREDATA_MEASURERESPONSE.fields_by_name['measure'].message_type = Measures__pb2._MEASURES_MEASURE
_MEASUREDATA_MEASURERESPONSE.fields_by_name['measurements'].message_type = _MEASUREDATA_MEASUREMENTDATA
_MEASUREDATA_MEASURERESPONSE.containing_type = _MEASUREDATA
_MEASUREDATA_MEASUREMENTDATA.fields_by_name['window'].message_type = Measurement__pb2._MEASUREMENT_WINDOW
_MEASUREDATA_MEASUREMENTDATA.containing_type = _MEASUREDATA
_MEASUREDATA_MEASUREMENTDATA.oneofs_by_name['which'].fields.append(
  _MEASUREDATA_MEASUREMENTDATA.fields_by_name['value'])
_MEASUREDATA_MEASUREMENTDATA.fields_by_name['value'].containing_oneof = _MEASUREDATA_MEASUREMENTDATA.oneofs_by_name['which']
_MEASUREDATA_MEASUREMENTDATA.oneofs_by_name['which'].fields.append(
  _MEASUREDATA_MEASUREMENTDATA.fields_by_name['window'])
_MEASUREDATA_MEASUREMENTDATA.fields_by_name['window'].containing_oneof = _MEASUREDATA_MEASUREMENTDATA.oneofs_by_name['which']
_MEASUREDATA.fields_by_name['request'].message_type = _MEASUREDATA_REQUEST
_MEASUREDATA.fields_by_name['response'].message_type = _MEASUREDATA_RESPONSE
_MEASUREDATA.oneofs_by_name['which'].fields.append(
  _MEASUREDATA.fields_by_name['request'])
_MEASUREDATA.fields_by_name['request'].containing_oneof = _MEASUREDATA.oneofs_by_name['which']
_MEASUREDATA.oneofs_by_name['which'].fields.append(
  _MEASUREDATA.fields_by_name['response'])
_MEASUREDATA.fields_by_name['response'].containing_oneof = _MEASUREDATA.oneofs_by_name['which']
DESCRIPTOR.message_types_by_name['Measuredata'] = _MEASUREDATA
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Measuredata = _reflection.GeneratedProtocolMessageType('Measuredata', (_message.Message,), dict(

  Request = _reflection.GeneratedProtocolMessageType('Request', (_message.Message,), dict(
    DESCRIPTOR = _MEASUREDATA_REQUEST,
    __module__ = 'Measuredata_pb2'
    # @@protoc_insertion_point(class_scope:geistt.rti.Measuredata.Request)
    ))
  ,

  Response = _reflection.GeneratedProtocolMessageType('Response', (_message.Message,), dict(
    DESCRIPTOR = _MEASUREDATA_RESPONSE,
    __module__ = 'Measuredata_pb2'
    # @@protoc_insertion_point(class_scope:geistt.rti.Measuredata.Response)
    ))
  ,

  MeasureResponse = _reflection.GeneratedProtocolMessageType('MeasureResponse', (_message.Message,), dict(
    DESCRIPTOR = _MEASUREDATA_MEASURERESPONSE,
    __module__ = 'Measuredata_pb2'
    # @@protoc_insertion_point(class_scope:geistt.rti.Measuredata.MeasureResponse)
    ))
  ,

  MeasurementData = _reflection.GeneratedProtocolMessageType('MeasurementData', (_message.Message,), dict(
    DESCRIPTOR = _MEASUREDATA_MEASUREMENTDATA,
    __module__ = 'Measuredata_pb2'
    # @@protoc_insertion_point(class_scope:geistt.rti.Measuredata.MeasurementData)
    ))
  ,
  DESCRIPTOR = _MEASUREDATA,
  __module__ = 'Measuredata_pb2'
  # @@protoc_insertion_point(class_scope:geistt.rti.Measuredata)
  ))
_sym_db.RegisterMessage(Measuredata)
_sym_db.RegisterMessage(Measuredata.Request)
_sym_db.RegisterMessage(Measuredata.Response)
_sym_db.RegisterMessage(Measuredata.MeasureResponse)
_sym_db.RegisterMessage(Measuredata.MeasurementData)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
