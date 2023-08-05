# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v3/proto/enums/distance_bucket.proto

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
  name='google/ads/googleads_v3/proto/enums/distance_bucket.proto',
  package='google.ads.googleads.v3.enums',
  syntax='proto3',
  serialized_options=_b('\n!com.google.ads.googleads.v3.enumsB\023DistanceBucketProtoP\001ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v3/enums;enums\242\002\003GAA\252\002\035Google.Ads.GoogleAds.V3.Enums\312\002\035Google\\Ads\\GoogleAds\\V3\\Enums\352\002!Google::Ads::GoogleAds::V3::Enums'),
  serialized_pb=_b('\n9google/ads/googleads_v3/proto/enums/distance_bucket.proto\x12\x1dgoogle.ads.googleads.v3.enums\x1a\x1cgoogle/api/annotations.proto\"\xad\x04\n\x12\x44istanceBucketEnum\"\x96\x04\n\x0e\x44istanceBucket\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x01\x12\x0f\n\x0bWITHIN_700M\x10\x02\x12\x0e\n\nWITHIN_1KM\x10\x03\x12\x0e\n\nWITHIN_5KM\x10\x04\x12\x0f\n\x0bWITHIN_10KM\x10\x05\x12\x0f\n\x0bWITHIN_15KM\x10\x06\x12\x0f\n\x0bWITHIN_20KM\x10\x07\x12\x0f\n\x0bWITHIN_25KM\x10\x08\x12\x0f\n\x0bWITHIN_30KM\x10\t\x12\x0f\n\x0bWITHIN_35KM\x10\n\x12\x0f\n\x0bWITHIN_40KM\x10\x0b\x12\x0f\n\x0bWITHIN_45KM\x10\x0c\x12\x0f\n\x0bWITHIN_50KM\x10\r\x12\x0f\n\x0bWITHIN_55KM\x10\x0e\x12\x0f\n\x0bWITHIN_60KM\x10\x0f\x12\x0f\n\x0bWITHIN_65KM\x10\x10\x12\x0f\n\x0b\x42\x45YOND_65KM\x10\x11\x12\x13\n\x0fWITHIN_0_7MILES\x10\x12\x12\x10\n\x0cWITHIN_1MILE\x10\x13\x12\x11\n\rWITHIN_5MILES\x10\x14\x12\x12\n\x0eWITHIN_10MILES\x10\x15\x12\x12\n\x0eWITHIN_15MILES\x10\x16\x12\x12\n\x0eWITHIN_20MILES\x10\x17\x12\x12\n\x0eWITHIN_25MILES\x10\x18\x12\x12\n\x0eWITHIN_30MILES\x10\x19\x12\x12\n\x0eWITHIN_35MILES\x10\x1a\x12\x12\n\x0eWITHIN_40MILES\x10\x1b\x12\x12\n\x0e\x42\x45YOND_40MILES\x10\x1c\x42\xe8\x01\n!com.google.ads.googleads.v3.enumsB\x13\x44istanceBucketProtoP\x01ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v3/enums;enums\xa2\x02\x03GAA\xaa\x02\x1dGoogle.Ads.GoogleAds.V3.Enums\xca\x02\x1dGoogle\\Ads\\GoogleAds\\V3\\Enums\xea\x02!Google::Ads::GoogleAds::V3::Enumsb\x06proto3')
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,])



_DISTANCEBUCKETENUM_DISTANCEBUCKET = _descriptor.EnumDescriptor(
  name='DistanceBucket',
  full_name='google.ads.googleads.v3.enums.DistanceBucketEnum.DistanceBucket',
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
      name='WITHIN_700M', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WITHIN_1KM', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WITHIN_5KM', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WITHIN_10KM', index=5, number=5,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WITHIN_15KM', index=6, number=6,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WITHIN_20KM', index=7, number=7,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WITHIN_25KM', index=8, number=8,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WITHIN_30KM', index=9, number=9,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WITHIN_35KM', index=10, number=10,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WITHIN_40KM', index=11, number=11,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WITHIN_45KM', index=12, number=12,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WITHIN_50KM', index=13, number=13,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WITHIN_55KM', index=14, number=14,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WITHIN_60KM', index=15, number=15,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WITHIN_65KM', index=16, number=16,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BEYOND_65KM', index=17, number=17,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WITHIN_0_7MILES', index=18, number=18,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WITHIN_1MILE', index=19, number=19,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WITHIN_5MILES', index=20, number=20,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WITHIN_10MILES', index=21, number=21,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WITHIN_15MILES', index=22, number=22,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WITHIN_20MILES', index=23, number=23,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WITHIN_25MILES', index=24, number=24,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WITHIN_30MILES', index=25, number=25,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WITHIN_35MILES', index=26, number=26,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WITHIN_40MILES', index=27, number=27,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BEYOND_40MILES', index=28, number=28,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=146,
  serialized_end=680,
)
_sym_db.RegisterEnumDescriptor(_DISTANCEBUCKETENUM_DISTANCEBUCKET)


_DISTANCEBUCKETENUM = _descriptor.Descriptor(
  name='DistanceBucketEnum',
  full_name='google.ads.googleads.v3.enums.DistanceBucketEnum',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _DISTANCEBUCKETENUM_DISTANCEBUCKET,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=123,
  serialized_end=680,
)

_DISTANCEBUCKETENUM_DISTANCEBUCKET.containing_type = _DISTANCEBUCKETENUM
DESCRIPTOR.message_types_by_name['DistanceBucketEnum'] = _DISTANCEBUCKETENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

DistanceBucketEnum = _reflection.GeneratedProtocolMessageType('DistanceBucketEnum', (_message.Message,), dict(
  DESCRIPTOR = _DISTANCEBUCKETENUM,
  __module__ = 'google.ads.googleads_v3.proto.enums.distance_bucket_pb2'
  ,
  __doc__ = """Container for distance buckets of a user’s distance from an advertiser’s
  location extension.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v3.enums.DistanceBucketEnum)
  ))
_sym_db.RegisterMessage(DistanceBucketEnum)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
