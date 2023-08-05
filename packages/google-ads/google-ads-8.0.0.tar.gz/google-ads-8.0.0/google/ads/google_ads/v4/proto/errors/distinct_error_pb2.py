# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v4/proto/errors/distinct_error.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v4/proto/errors/distinct_error.proto',
  package='google.ads.googleads.v4.errors',
  syntax='proto3',
  serialized_options=_b('\n\"com.google.ads.googleads.v4.errorsB\022DistinctErrorProtoP\001ZDgoogle.golang.org/genproto/googleapis/ads/googleads/v4/errors;errors\242\002\003GAA\252\002\036Google.Ads.GoogleAds.V4.Errors\312\002\036Google\\Ads\\GoogleAds\\V4\\Errors\352\002\"Google::Ads::GoogleAds::V4::Errors'),
  serialized_pb=_b('\n9google/ads/googleads_v4/proto/errors/distinct_error.proto\x12\x1egoogle.ads.googleads.v4.errors\x1a\x1cgoogle/api/annotations.proto\"m\n\x11\x44istinctErrorEnum\"X\n\rDistinctError\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x01\x12\x15\n\x11\x44UPLICATE_ELEMENT\x10\x02\x12\x12\n\x0e\x44UPLICATE_TYPE\x10\x03\x42\xed\x01\n\"com.google.ads.googleads.v4.errorsB\x12\x44istinctErrorProtoP\x01ZDgoogle.golang.org/genproto/googleapis/ads/googleads/v4/errors;errors\xa2\x02\x03GAA\xaa\x02\x1eGoogle.Ads.GoogleAds.V4.Errors\xca\x02\x1eGoogle\\Ads\\GoogleAds\\V4\\Errors\xea\x02\"Google::Ads::GoogleAds::V4::Errorsb\x06proto3')
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,])



_DISTINCTERRORENUM_DISTINCTERROR = _descriptor.EnumDescriptor(
  name='DistinctError',
  full_name='google.ads.googleads.v4.errors.DistinctErrorEnum.DistinctError',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNSPECIFIED', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DUPLICATE_ELEMENT', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DUPLICATE_TYPE', index=3, number=3,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=144,
  serialized_end=232,
)
_sym_db.RegisterEnumDescriptor(_DISTINCTERRORENUM_DISTINCTERROR)


_DISTINCTERRORENUM = _descriptor.Descriptor(
  name='DistinctErrorEnum',
  full_name='google.ads.googleads.v4.errors.DistinctErrorEnum',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _DISTINCTERRORENUM_DISTINCTERROR,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=123,
  serialized_end=232,
)

_DISTINCTERRORENUM_DISTINCTERROR.containing_type = _DISTINCTERRORENUM
DESCRIPTOR.message_types_by_name['DistinctErrorEnum'] = _DISTINCTERRORENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

DistinctErrorEnum = _reflection.GeneratedProtocolMessageType('DistinctErrorEnum', (_message.Message,), dict(
  DESCRIPTOR = _DISTINCTERRORENUM,
  __module__ = 'google.ads.googleads_v4.proto.errors.distinct_error_pb2'
  ,
  __doc__ = """Container for enum describing possible distinct errors.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v4.errors.DistinctErrorEnum)
  ))
_sym_db.RegisterMessage(DistinctErrorEnum)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
