# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v6/proto/errors/mutate_error.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v6/proto/errors/mutate_error.proto',
  package='google.ads.googleads.v6.errors',
  syntax='proto3',
  serialized_options=b'\n\"com.google.ads.googleads.v6.errorsB\020MutateErrorProtoP\001ZDgoogle.golang.org/genproto/googleapis/ads/googleads/v6/errors;errors\242\002\003GAA\252\002\036Google.Ads.GoogleAds.V6.Errors\312\002\036Google\\Ads\\GoogleAds\\V6\\Errors\352\002\"Google::Ads::GoogleAds::V6::Errors',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n7google/ads/googleads_v6/proto/errors/mutate_error.proto\x12\x1egoogle.ads.googleads.v6.errors\x1a\x1cgoogle/api/annotations.proto\"\xb3\x02\n\x0fMutateErrorEnum\"\x9f\x02\n\x0bMutateError\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x01\x12\x16\n\x12RESOURCE_NOT_FOUND\x10\x03\x12!\n\x1dID_EXISTS_IN_MULTIPLE_MUTATES\x10\x07\x12\x1d\n\x19INCONSISTENT_FIELD_VALUES\x10\x08\x12\x16\n\x12MUTATE_NOT_ALLOWED\x10\t\x12\x1e\n\x1aRESOURCE_NOT_IN_GOOGLE_ADS\x10\n\x12\x1b\n\x17RESOURCE_ALREADY_EXISTS\x10\x0b\x12+\n\'RESOURCE_DOES_NOT_SUPPORT_VALIDATE_ONLY\x10\x0c\x12\x16\n\x12RESOURCE_READ_ONLY\x10\rB\xeb\x01\n\"com.google.ads.googleads.v6.errorsB\x10MutateErrorProtoP\x01ZDgoogle.golang.org/genproto/googleapis/ads/googleads/v6/errors;errors\xa2\x02\x03GAA\xaa\x02\x1eGoogle.Ads.GoogleAds.V6.Errors\xca\x02\x1eGoogle\\Ads\\GoogleAds\\V6\\Errors\xea\x02\"Google::Ads::GoogleAds::V6::Errorsb\x06proto3'
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,])



_MUTATEERRORENUM_MUTATEERROR = _descriptor.EnumDescriptor(
  name='MutateError',
  full_name='google.ads.googleads.v6.errors.MutateErrorEnum.MutateError',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNSPECIFIED', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='RESOURCE_NOT_FOUND', index=2, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='ID_EXISTS_IN_MULTIPLE_MUTATES', index=3, number=7,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='INCONSISTENT_FIELD_VALUES', index=4, number=8,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='MUTATE_NOT_ALLOWED', index=5, number=9,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='RESOURCE_NOT_IN_GOOGLE_ADS', index=6, number=10,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='RESOURCE_ALREADY_EXISTS', index=7, number=11,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='RESOURCE_DOES_NOT_SUPPORT_VALIDATE_ONLY', index=8, number=12,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='RESOURCE_READ_ONLY', index=9, number=13,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=142,
  serialized_end=429,
)
_sym_db.RegisterEnumDescriptor(_MUTATEERRORENUM_MUTATEERROR)


_MUTATEERRORENUM = _descriptor.Descriptor(
  name='MutateErrorEnum',
  full_name='google.ads.googleads.v6.errors.MutateErrorEnum',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _MUTATEERRORENUM_MUTATEERROR,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=122,
  serialized_end=429,
)

_MUTATEERRORENUM_MUTATEERROR.containing_type = _MUTATEERRORENUM
DESCRIPTOR.message_types_by_name['MutateErrorEnum'] = _MUTATEERRORENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

MutateErrorEnum = _reflection.GeneratedProtocolMessageType('MutateErrorEnum', (_message.Message,), {
  'DESCRIPTOR' : _MUTATEERRORENUM,
  '__module__' : 'google.ads.googleads_v6.proto.errors.mutate_error_pb2'
  ,
  '__doc__': """Container for enum describing possible mutate errors.""",
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v6.errors.MutateErrorEnum)
  })
_sym_db.RegisterMessage(MutateErrorEnum)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
