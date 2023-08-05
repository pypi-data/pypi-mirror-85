# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v4/proto/errors/media_bundle_error.proto

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
  name='google/ads/googleads_v4/proto/errors/media_bundle_error.proto',
  package='google.ads.googleads.v4.errors',
  syntax='proto3',
  serialized_options=_b('\n\"com.google.ads.googleads.v4.errorsB\025MediaBundleErrorProtoP\001ZDgoogle.golang.org/genproto/googleapis/ads/googleads/v4/errors;errors\242\002\003GAA\252\002\036Google.Ads.GoogleAds.V4.Errors\312\002\036Google\\Ads\\GoogleAds\\V4\\Errors\352\002\"Google::Ads::GoogleAds::V4::Errors'),
  serialized_pb=_b('\n=google/ads/googleads_v4/proto/errors/media_bundle_error.proto\x12\x1egoogle.ads.googleads.v4.errors\x1a\x1cgoogle/api/annotations.proto\"\xb8\x05\n\x14MediaBundleErrorEnum\"\x9f\x05\n\x10MediaBundleError\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x01\x12\x0f\n\x0b\x42\x41\x44_REQUEST\x10\x03\x12\"\n\x1e\x44OUBLECLICK_BUNDLE_NOT_ALLOWED\x10\x04\x12\x1c\n\x18\x45XTERNAL_URL_NOT_ALLOWED\x10\x05\x12\x12\n\x0e\x46ILE_TOO_LARGE\x10\x06\x12.\n*GOOGLE_WEB_DESIGNER_ZIP_FILE_NOT_PUBLISHED\x10\x07\x12\x11\n\rINVALID_INPUT\x10\x08\x12\x18\n\x14INVALID_MEDIA_BUNDLE\x10\t\x12\x1e\n\x1aINVALID_MEDIA_BUNDLE_ENTRY\x10\n\x12\x15\n\x11INVALID_MIME_TYPE\x10\x0b\x12\x10\n\x0cINVALID_PATH\x10\x0c\x12\x19\n\x15INVALID_URL_REFERENCE\x10\r\x12\x18\n\x14MEDIA_DATA_TOO_LARGE\x10\x0e\x12&\n\"MISSING_PRIMARY_MEDIA_BUNDLE_ENTRY\x10\x0f\x12\x10\n\x0cSERVER_ERROR\x10\x10\x12\x11\n\rSTORAGE_ERROR\x10\x11\x12\x1d\n\x19SWIFFY_BUNDLE_NOT_ALLOWED\x10\x12\x12\x12\n\x0eTOO_MANY_FILES\x10\x13\x12\x13\n\x0fUNEXPECTED_SIZE\x10\x14\x12/\n+UNSUPPORTED_GOOGLE_WEB_DESIGNER_ENVIRONMENT\x10\x15\x12\x1d\n\x19UNSUPPORTED_HTML5_FEATURE\x10\x16\x12)\n%URL_IN_MEDIA_BUNDLE_NOT_SSL_COMPLIANT\x10\x17\x12\x1b\n\x17\x43USTOM_EXIT_NOT_ALLOWED\x10\x18\x42\xf0\x01\n\"com.google.ads.googleads.v4.errorsB\x15MediaBundleErrorProtoP\x01ZDgoogle.golang.org/genproto/googleapis/ads/googleads/v4/errors;errors\xa2\x02\x03GAA\xaa\x02\x1eGoogle.Ads.GoogleAds.V4.Errors\xca\x02\x1eGoogle\\Ads\\GoogleAds\\V4\\Errors\xea\x02\"Google::Ads::GoogleAds::V4::Errorsb\x06proto3')
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,])



_MEDIABUNDLEERRORENUM_MEDIABUNDLEERROR = _descriptor.EnumDescriptor(
  name='MediaBundleError',
  full_name='google.ads.googleads.v4.errors.MediaBundleErrorEnum.MediaBundleError',
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
      name='BAD_REQUEST', index=2, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DOUBLECLICK_BUNDLE_NOT_ALLOWED', index=3, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='EXTERNAL_URL_NOT_ALLOWED', index=4, number=5,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FILE_TOO_LARGE', index=5, number=6,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='GOOGLE_WEB_DESIGNER_ZIP_FILE_NOT_PUBLISHED', index=6, number=7,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INVALID_INPUT', index=7, number=8,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INVALID_MEDIA_BUNDLE', index=8, number=9,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INVALID_MEDIA_BUNDLE_ENTRY', index=9, number=10,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INVALID_MIME_TYPE', index=10, number=11,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INVALID_PATH', index=11, number=12,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INVALID_URL_REFERENCE', index=12, number=13,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MEDIA_DATA_TOO_LARGE', index=13, number=14,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MISSING_PRIMARY_MEDIA_BUNDLE_ENTRY', index=14, number=15,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SERVER_ERROR', index=15, number=16,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='STORAGE_ERROR', index=16, number=17,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SWIFFY_BUNDLE_NOT_ALLOWED', index=17, number=18,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='TOO_MANY_FILES', index=18, number=19,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='UNEXPECTED_SIZE', index=19, number=20,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='UNSUPPORTED_GOOGLE_WEB_DESIGNER_ENVIRONMENT', index=20, number=21,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='UNSUPPORTED_HTML5_FEATURE', index=21, number=22,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='URL_IN_MEDIA_BUNDLE_NOT_SSL_COMPLIANT', index=22, number=23,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CUSTOM_EXIT_NOT_ALLOWED', index=23, number=24,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=153,
  serialized_end=824,
)
_sym_db.RegisterEnumDescriptor(_MEDIABUNDLEERRORENUM_MEDIABUNDLEERROR)


_MEDIABUNDLEERRORENUM = _descriptor.Descriptor(
  name='MediaBundleErrorEnum',
  full_name='google.ads.googleads.v4.errors.MediaBundleErrorEnum',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _MEDIABUNDLEERRORENUM_MEDIABUNDLEERROR,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=128,
  serialized_end=824,
)

_MEDIABUNDLEERRORENUM_MEDIABUNDLEERROR.containing_type = _MEDIABUNDLEERRORENUM
DESCRIPTOR.message_types_by_name['MediaBundleErrorEnum'] = _MEDIABUNDLEERRORENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

MediaBundleErrorEnum = _reflection.GeneratedProtocolMessageType('MediaBundleErrorEnum', (_message.Message,), dict(
  DESCRIPTOR = _MEDIABUNDLEERRORENUM,
  __module__ = 'google.ads.googleads_v4.proto.errors.media_bundle_error_pb2'
  ,
  __doc__ = """Container for enum describing possible media bundle errors.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v4.errors.MediaBundleErrorEnum)
  ))
_sym_db.RegisterMessage(MediaBundleErrorEnum)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
