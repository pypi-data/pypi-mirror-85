# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v5/proto/enums/conversion_action_counting_type.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v5/proto/enums/conversion_action_counting_type.proto',
  package='google.ads.googleads.v5.enums',
  syntax='proto3',
  serialized_options=b'\n!com.google.ads.googleads.v5.enumsB!ConversionActionCountingTypeProtoP\001ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v5/enums;enums\242\002\003GAA\252\002\035Google.Ads.GoogleAds.V5.Enums\312\002\035Google\\Ads\\GoogleAds\\V5\\Enums\352\002!Google::Ads::GoogleAds::V5::Enums',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\nIgoogle/ads/googleads_v5/proto/enums/conversion_action_counting_type.proto\x12\x1dgoogle.ads.googleads.v5.enums\x1a\x1cgoogle/api/annotations.proto\"\x87\x01\n ConversionActionCountingTypeEnum\"c\n\x1c\x43onversionActionCountingType\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x01\x12\x11\n\rONE_PER_CLICK\x10\x02\x12\x12\n\x0eMANY_PER_CLICK\x10\x03\x42\xf6\x01\n!com.google.ads.googleads.v5.enumsB!ConversionActionCountingTypeProtoP\x01ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v5/enums;enums\xa2\x02\x03GAA\xaa\x02\x1dGoogle.Ads.GoogleAds.V5.Enums\xca\x02\x1dGoogle\\Ads\\GoogleAds\\V5\\Enums\xea\x02!Google::Ads::GoogleAds::V5::Enumsb\x06proto3'
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,])



_CONVERSIONACTIONCOUNTINGTYPEENUM_CONVERSIONACTIONCOUNTINGTYPE = _descriptor.EnumDescriptor(
  name='ConversionActionCountingType',
  full_name='google.ads.googleads.v5.enums.ConversionActionCountingTypeEnum.ConversionActionCountingType',
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
      name='ONE_PER_CLICK', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='MANY_PER_CLICK', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=175,
  serialized_end=274,
)
_sym_db.RegisterEnumDescriptor(_CONVERSIONACTIONCOUNTINGTYPEENUM_CONVERSIONACTIONCOUNTINGTYPE)


_CONVERSIONACTIONCOUNTINGTYPEENUM = _descriptor.Descriptor(
  name='ConversionActionCountingTypeEnum',
  full_name='google.ads.googleads.v5.enums.ConversionActionCountingTypeEnum',
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
    _CONVERSIONACTIONCOUNTINGTYPEENUM_CONVERSIONACTIONCOUNTINGTYPE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=139,
  serialized_end=274,
)

_CONVERSIONACTIONCOUNTINGTYPEENUM_CONVERSIONACTIONCOUNTINGTYPE.containing_type = _CONVERSIONACTIONCOUNTINGTYPEENUM
DESCRIPTOR.message_types_by_name['ConversionActionCountingTypeEnum'] = _CONVERSIONACTIONCOUNTINGTYPEENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ConversionActionCountingTypeEnum = _reflection.GeneratedProtocolMessageType('ConversionActionCountingTypeEnum', (_message.Message,), {
  'DESCRIPTOR' : _CONVERSIONACTIONCOUNTINGTYPEENUM,
  '__module__' : 'google.ads.googleads_v5.proto.enums.conversion_action_counting_type_pb2'
  ,
  '__doc__': """Container for enum describing the conversion deduplication mode for
  conversion optimizer.""",
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v5.enums.ConversionActionCountingTypeEnum)
  })
_sym_db.RegisterMessage(ConversionActionCountingTypeEnum)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
