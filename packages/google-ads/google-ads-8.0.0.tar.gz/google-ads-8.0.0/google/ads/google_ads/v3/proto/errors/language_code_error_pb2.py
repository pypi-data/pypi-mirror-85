# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v3/proto/errors/language_code_error.proto

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
  name='google/ads/googleads_v3/proto/errors/language_code_error.proto',
  package='google.ads.googleads.v3.errors',
  syntax='proto3',
  serialized_options=_b('\n\"com.google.ads.googleads.v3.errorsB\026LanguageCodeErrorProtoP\001ZDgoogle.golang.org/genproto/googleapis/ads/googleads/v3/errors;errors\242\002\003GAA\252\002\036Google.Ads.GoogleAds.V3.Errors\312\002\036Google\\Ads\\GoogleAds\\V3\\Errors\352\002\"Google::Ads::GoogleAds::V3::Errors'),
  serialized_pb=_b('\n>google/ads/googleads_v3/proto/errors/language_code_error.proto\x12\x1egoogle.ads.googleads.v3.errors\x1a\x1cgoogle/api/annotations.proto\"\x82\x01\n\x15LanguageCodeErrorEnum\"i\n\x11LanguageCodeError\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x01\x12\x1b\n\x17LANGUAGE_CODE_NOT_FOUND\x10\x02\x12\x19\n\x15INVALID_LANGUAGE_CODE\x10\x03\x42\xf1\x01\n\"com.google.ads.googleads.v3.errorsB\x16LanguageCodeErrorProtoP\x01ZDgoogle.golang.org/genproto/googleapis/ads/googleads/v3/errors;errors\xa2\x02\x03GAA\xaa\x02\x1eGoogle.Ads.GoogleAds.V3.Errors\xca\x02\x1eGoogle\\Ads\\GoogleAds\\V3\\Errors\xea\x02\"Google::Ads::GoogleAds::V3::Errorsb\x06proto3')
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,])



_LANGUAGECODEERRORENUM_LANGUAGECODEERROR = _descriptor.EnumDescriptor(
  name='LanguageCodeError',
  full_name='google.ads.googleads.v3.errors.LanguageCodeErrorEnum.LanguageCodeError',
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
      name='LANGUAGE_CODE_NOT_FOUND', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INVALID_LANGUAGE_CODE', index=3, number=3,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=154,
  serialized_end=259,
)
_sym_db.RegisterEnumDescriptor(_LANGUAGECODEERRORENUM_LANGUAGECODEERROR)


_LANGUAGECODEERRORENUM = _descriptor.Descriptor(
  name='LanguageCodeErrorEnum',
  full_name='google.ads.googleads.v3.errors.LanguageCodeErrorEnum',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _LANGUAGECODEERRORENUM_LANGUAGECODEERROR,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=129,
  serialized_end=259,
)

_LANGUAGECODEERRORENUM_LANGUAGECODEERROR.containing_type = _LANGUAGECODEERRORENUM
DESCRIPTOR.message_types_by_name['LanguageCodeErrorEnum'] = _LANGUAGECODEERRORENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

LanguageCodeErrorEnum = _reflection.GeneratedProtocolMessageType('LanguageCodeErrorEnum', (_message.Message,), dict(
  DESCRIPTOR = _LANGUAGECODEERRORENUM,
  __module__ = 'google.ads.googleads_v3.proto.errors.language_code_error_pb2'
  ,
  __doc__ = """Container for enum describing language code errors.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v3.errors.LanguageCodeErrorEnum)
  ))
_sym_db.RegisterMessage(LanguageCodeErrorEnum)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
