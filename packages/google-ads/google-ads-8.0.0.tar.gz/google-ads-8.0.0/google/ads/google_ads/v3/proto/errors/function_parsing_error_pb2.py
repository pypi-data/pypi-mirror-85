# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v3/proto/errors/function_parsing_error.proto

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
  name='google/ads/googleads_v3/proto/errors/function_parsing_error.proto',
  package='google.ads.googleads.v3.errors',
  syntax='proto3',
  serialized_options=_b('\n\"com.google.ads.googleads.v3.errorsB\031FunctionParsingErrorProtoP\001ZDgoogle.golang.org/genproto/googleapis/ads/googleads/v3/errors;errors\242\002\003GAA\252\002\036Google.Ads.GoogleAds.V3.Errors\312\002\036Google\\Ads\\GoogleAds\\V3\\Errors\352\002\"Google::Ads::GoogleAds::V3::Errors'),
  serialized_pb=_b('\nAgoogle/ads/googleads_v3/proto/errors/function_parsing_error.proto\x12\x1egoogle.ads.googleads.v3.errors\x1a\x1cgoogle/api/annotations.proto\"\x82\x03\n\x18\x46unctionParsingErrorEnum\"\xe5\x02\n\x14\x46unctionParsingError\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x01\x12\x11\n\rNO_MORE_INPUT\x10\x02\x12\x16\n\x12\x45XPECTED_CHARACTER\x10\x03\x12\x18\n\x14UNEXPECTED_SEPARATOR\x10\x04\x12\x1a\n\x16UNMATCHED_LEFT_BRACKET\x10\x05\x12\x1b\n\x17UNMATCHED_RIGHT_BRACKET\x10\x06\x12\x1d\n\x19TOO_MANY_NESTED_FUNCTIONS\x10\x07\x12\x1e\n\x1aMISSING_RIGHT_HAND_OPERAND\x10\x08\x12\x19\n\x15INVALID_OPERATOR_NAME\x10\t\x12/\n+FEED_ATTRIBUTE_OPERAND_ARGUMENT_NOT_INTEGER\x10\n\x12\x0f\n\x0bNO_OPERANDS\x10\x0b\x12\x15\n\x11TOO_MANY_OPERANDS\x10\x0c\x42\xf4\x01\n\"com.google.ads.googleads.v3.errorsB\x19\x46unctionParsingErrorProtoP\x01ZDgoogle.golang.org/genproto/googleapis/ads/googleads/v3/errors;errors\xa2\x02\x03GAA\xaa\x02\x1eGoogle.Ads.GoogleAds.V3.Errors\xca\x02\x1eGoogle\\Ads\\GoogleAds\\V3\\Errors\xea\x02\"Google::Ads::GoogleAds::V3::Errorsb\x06proto3')
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,])



_FUNCTIONPARSINGERRORENUM_FUNCTIONPARSINGERROR = _descriptor.EnumDescriptor(
  name='FunctionParsingError',
  full_name='google.ads.googleads.v3.errors.FunctionParsingErrorEnum.FunctionParsingError',
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
      name='NO_MORE_INPUT', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='EXPECTED_CHARACTER', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='UNEXPECTED_SEPARATOR', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='UNMATCHED_LEFT_BRACKET', index=5, number=5,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='UNMATCHED_RIGHT_BRACKET', index=6, number=6,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='TOO_MANY_NESTED_FUNCTIONS', index=7, number=7,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MISSING_RIGHT_HAND_OPERAND', index=8, number=8,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INVALID_OPERATOR_NAME', index=9, number=9,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FEED_ATTRIBUTE_OPERAND_ARGUMENT_NOT_INTEGER', index=10, number=10,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NO_OPERANDS', index=11, number=11,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='TOO_MANY_OPERANDS', index=12, number=12,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=161,
  serialized_end=518,
)
_sym_db.RegisterEnumDescriptor(_FUNCTIONPARSINGERRORENUM_FUNCTIONPARSINGERROR)


_FUNCTIONPARSINGERRORENUM = _descriptor.Descriptor(
  name='FunctionParsingErrorEnum',
  full_name='google.ads.googleads.v3.errors.FunctionParsingErrorEnum',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _FUNCTIONPARSINGERRORENUM_FUNCTIONPARSINGERROR,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=132,
  serialized_end=518,
)

_FUNCTIONPARSINGERRORENUM_FUNCTIONPARSINGERROR.containing_type = _FUNCTIONPARSINGERRORENUM
DESCRIPTOR.message_types_by_name['FunctionParsingErrorEnum'] = _FUNCTIONPARSINGERRORENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

FunctionParsingErrorEnum = _reflection.GeneratedProtocolMessageType('FunctionParsingErrorEnum', (_message.Message,), dict(
  DESCRIPTOR = _FUNCTIONPARSINGERRORENUM,
  __module__ = 'google.ads.googleads_v3.proto.errors.function_parsing_error_pb2'
  ,
  __doc__ = """Container for enum describing possible function parsing errors.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v3.errors.FunctionParsingErrorEnum)
  ))
_sym_db.RegisterMessage(FunctionParsingErrorEnum)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
