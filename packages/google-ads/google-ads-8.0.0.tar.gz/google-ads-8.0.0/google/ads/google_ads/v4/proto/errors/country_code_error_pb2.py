# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v4/proto/errors/country_code_error.proto

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
  name='google/ads/googleads_v4/proto/errors/country_code_error.proto',
  package='google.ads.googleads.v4.errors',
  syntax='proto3',
  serialized_options=_b('\n\"com.google.ads.googleads.v4.errorsB\025CountryCodeErrorProtoP\001ZDgoogle.golang.org/genproto/googleapis/ads/googleads/v4/errors;errors\242\002\003GAA\252\002\036Google.Ads.GoogleAds.V4.Errors\312\002\036Google\\Ads\\GoogleAds\\V4\\Errors\352\002\"Google::Ads::GoogleAds::V4::Errors'),
  serialized_pb=_b('\n=google/ads/googleads_v4/proto/errors/country_code_error.proto\x12\x1egoogle.ads.googleads.v4.errors\x1a\x1cgoogle/api/annotations.proto\"b\n\x14\x43ountryCodeErrorEnum\"J\n\x10\x43ountryCodeError\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x01\x12\x18\n\x14INVALID_COUNTRY_CODE\x10\x02\x42\xf0\x01\n\"com.google.ads.googleads.v4.errorsB\x15\x43ountryCodeErrorProtoP\x01ZDgoogle.golang.org/genproto/googleapis/ads/googleads/v4/errors;errors\xa2\x02\x03GAA\xaa\x02\x1eGoogle.Ads.GoogleAds.V4.Errors\xca\x02\x1eGoogle\\Ads\\GoogleAds\\V4\\Errors\xea\x02\"Google::Ads::GoogleAds::V4::Errorsb\x06proto3')
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,])



_COUNTRYCODEERRORENUM_COUNTRYCODEERROR = _descriptor.EnumDescriptor(
  name='CountryCodeError',
  full_name='google.ads.googleads.v4.errors.CountryCodeErrorEnum.CountryCodeError',
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
      name='INVALID_COUNTRY_CODE', index=2, number=2,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=151,
  serialized_end=225,
)
_sym_db.RegisterEnumDescriptor(_COUNTRYCODEERRORENUM_COUNTRYCODEERROR)


_COUNTRYCODEERRORENUM = _descriptor.Descriptor(
  name='CountryCodeErrorEnum',
  full_name='google.ads.googleads.v4.errors.CountryCodeErrorEnum',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _COUNTRYCODEERRORENUM_COUNTRYCODEERROR,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=127,
  serialized_end=225,
)

_COUNTRYCODEERRORENUM_COUNTRYCODEERROR.containing_type = _COUNTRYCODEERRORENUM
DESCRIPTOR.message_types_by_name['CountryCodeErrorEnum'] = _COUNTRYCODEERRORENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

CountryCodeErrorEnum = _reflection.GeneratedProtocolMessageType('CountryCodeErrorEnum', (_message.Message,), dict(
  DESCRIPTOR = _COUNTRYCODEERRORENUM,
  __module__ = 'google.ads.googleads_v4.proto.errors.country_code_error_pb2'
  ,
  __doc__ = """Container for enum describing country code errors.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v4.errors.CountryCodeErrorEnum)
  ))
_sym_db.RegisterMessage(CountryCodeErrorEnum)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
