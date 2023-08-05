# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v4/proto/enums/brand_safety_suitability.proto

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
  name='google/ads/googleads_v4/proto/enums/brand_safety_suitability.proto',
  package='google.ads.googleads.v4.enums',
  syntax='proto3',
  serialized_options=_b('\n!com.google.ads.googleads.v4.enumsB\033BrandSafetySuitabilityProtoP\001ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v4/enums;enums\242\002\003GAA\252\002\035Google.Ads.GoogleAds.V4.Enums\312\002\035Google\\Ads\\GoogleAds\\V4\\Enums\352\002!Google::Ads::GoogleAds::V4::Enums'),
  serialized_pb=_b('\nBgoogle/ads/googleads_v4/proto/enums/brand_safety_suitability.proto\x12\x1dgoogle.ads.googleads.v4.enums\x1a\x1cgoogle/api/annotations.proto\"\x9b\x01\n\x1a\x42randSafetySuitabilityEnum\"}\n\x16\x42randSafetySuitability\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x01\x12\x16\n\x12\x45XPANDED_INVENTORY\x10\x02\x12\x16\n\x12STANDARD_INVENTORY\x10\x03\x12\x15\n\x11LIMITED_INVENTORY\x10\x04\x42\xf0\x01\n!com.google.ads.googleads.v4.enumsB\x1b\x42randSafetySuitabilityProtoP\x01ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v4/enums;enums\xa2\x02\x03GAA\xaa\x02\x1dGoogle.Ads.GoogleAds.V4.Enums\xca\x02\x1dGoogle\\Ads\\GoogleAds\\V4\\Enums\xea\x02!Google::Ads::GoogleAds::V4::Enumsb\x06proto3')
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,])



_BRANDSAFETYSUITABILITYENUM_BRANDSAFETYSUITABILITY = _descriptor.EnumDescriptor(
  name='BrandSafetySuitability',
  full_name='google.ads.googleads.v4.enums.BrandSafetySuitabilityEnum.BrandSafetySuitability',
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
      name='EXPANDED_INVENTORY', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='STANDARD_INVENTORY', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='LIMITED_INVENTORY', index=4, number=4,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=162,
  serialized_end=287,
)
_sym_db.RegisterEnumDescriptor(_BRANDSAFETYSUITABILITYENUM_BRANDSAFETYSUITABILITY)


_BRANDSAFETYSUITABILITYENUM = _descriptor.Descriptor(
  name='BrandSafetySuitabilityEnum',
  full_name='google.ads.googleads.v4.enums.BrandSafetySuitabilityEnum',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _BRANDSAFETYSUITABILITYENUM_BRANDSAFETYSUITABILITY,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=132,
  serialized_end=287,
)

_BRANDSAFETYSUITABILITYENUM_BRANDSAFETYSUITABILITY.containing_type = _BRANDSAFETYSUITABILITYENUM
DESCRIPTOR.message_types_by_name['BrandSafetySuitabilityEnum'] = _BRANDSAFETYSUITABILITYENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

BrandSafetySuitabilityEnum = _reflection.GeneratedProtocolMessageType('BrandSafetySuitabilityEnum', (_message.Message,), dict(
  DESCRIPTOR = _BRANDSAFETYSUITABILITYENUM,
  __module__ = 'google.ads.googleads_v4.proto.enums.brand_safety_suitability_pb2'
  ,
  __doc__ = """Container for enum with 3-Tier brand safety suitability control.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v4.enums.BrandSafetySuitabilityEnum)
  ))
_sym_db.RegisterMessage(BrandSafetySuitabilityEnum)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
