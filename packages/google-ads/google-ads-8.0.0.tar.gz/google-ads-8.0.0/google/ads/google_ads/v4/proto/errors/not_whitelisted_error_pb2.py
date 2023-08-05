# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v4/proto/errors/not_whitelisted_error.proto

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
  name='google/ads/googleads_v4/proto/errors/not_whitelisted_error.proto',
  package='google.ads.googleads.v4.errors',
  syntax='proto3',
  serialized_options=_b('\n\"com.google.ads.googleads.v4.errorsB\030NotWhitelistedErrorProtoP\001ZDgoogle.golang.org/genproto/googleapis/ads/googleads/v4/errors;errors\242\002\003GAA\252\002\036Google.Ads.GoogleAds.V4.Errors\312\002\036Google\\Ads\\GoogleAds\\V4\\Errors\352\002\"Google::Ads::GoogleAds::V4::Errors'),
  serialized_pb=_b('\n@google/ads/googleads_v4/proto/errors/not_whitelisted_error.proto\x12\x1egoogle.ads.googleads.v4.errors\x1a\x1cgoogle/api/annotations.proto\"}\n\x17NotWhitelistedErrorEnum\"b\n\x13NotWhitelistedError\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x01\x12-\n)CUSTOMER_NOT_WHITELISTED_FOR_THIS_FEATURE\x10\x02\x42\xf3\x01\n\"com.google.ads.googleads.v4.errorsB\x18NotWhitelistedErrorProtoP\x01ZDgoogle.golang.org/genproto/googleapis/ads/googleads/v4/errors;errors\xa2\x02\x03GAA\xaa\x02\x1eGoogle.Ads.GoogleAds.V4.Errors\xca\x02\x1eGoogle\\Ads\\GoogleAds\\V4\\Errors\xea\x02\"Google::Ads::GoogleAds::V4::Errorsb\x06proto3')
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,])



_NOTWHITELISTEDERRORENUM_NOTWHITELISTEDERROR = _descriptor.EnumDescriptor(
  name='NotWhitelistedError',
  full_name='google.ads.googleads.v4.errors.NotWhitelistedErrorEnum.NotWhitelistedError',
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
      name='CUSTOMER_NOT_WHITELISTED_FOR_THIS_FEATURE', index=2, number=2,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=157,
  serialized_end=255,
)
_sym_db.RegisterEnumDescriptor(_NOTWHITELISTEDERRORENUM_NOTWHITELISTEDERROR)


_NOTWHITELISTEDERRORENUM = _descriptor.Descriptor(
  name='NotWhitelistedErrorEnum',
  full_name='google.ads.googleads.v4.errors.NotWhitelistedErrorEnum',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _NOTWHITELISTEDERRORENUM_NOTWHITELISTEDERROR,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=130,
  serialized_end=255,
)

_NOTWHITELISTEDERRORENUM_NOTWHITELISTEDERROR.containing_type = _NOTWHITELISTEDERRORENUM
DESCRIPTOR.message_types_by_name['NotWhitelistedErrorEnum'] = _NOTWHITELISTEDERRORENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

NotWhitelistedErrorEnum = _reflection.GeneratedProtocolMessageType('NotWhitelistedErrorEnum', (_message.Message,), dict(
  DESCRIPTOR = _NOTWHITELISTEDERRORENUM,
  __module__ = 'google.ads.googleads_v4.proto.errors.not_whitelisted_error_pb2'
  ,
  __doc__ = """Container for enum describing possible not whitelisted errors.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v4.errors.NotWhitelistedErrorEnum)
  ))
_sym_db.RegisterMessage(NotWhitelistedErrorEnum)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
