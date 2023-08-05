# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v4/proto/enums/ad_group_ad_status.proto

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
  name='google/ads/googleads_v4/proto/enums/ad_group_ad_status.proto',
  package='google.ads.googleads.v4.enums',
  syntax='proto3',
  serialized_options=_b('\n!com.google.ads.googleads.v4.enumsB\024AdGroupAdStatusProtoP\001ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v4/enums;enums\242\002\003GAA\252\002\035Google.Ads.GoogleAds.V4.Enums\312\002\035Google\\Ads\\GoogleAds\\V4\\Enums\352\002!Google::Ads::GoogleAds::V4::Enums'),
  serialized_pb=_b('\n<google/ads/googleads_v4/proto/enums/ad_group_ad_status.proto\x12\x1dgoogle.ads.googleads.v4.enums\x1a\x1cgoogle/api/annotations.proto\"l\n\x13\x41\x64GroupAdStatusEnum\"U\n\x0f\x41\x64GroupAdStatus\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x01\x12\x0b\n\x07\x45NABLED\x10\x02\x12\n\n\x06PAUSED\x10\x03\x12\x0b\n\x07REMOVED\x10\x04\x42\xe9\x01\n!com.google.ads.googleads.v4.enumsB\x14\x41\x64GroupAdStatusProtoP\x01ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v4/enums;enums\xa2\x02\x03GAA\xaa\x02\x1dGoogle.Ads.GoogleAds.V4.Enums\xca\x02\x1dGoogle\\Ads\\GoogleAds\\V4\\Enums\xea\x02!Google::Ads::GoogleAds::V4::Enumsb\x06proto3')
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,])



_ADGROUPADSTATUSENUM_ADGROUPADSTATUS = _descriptor.EnumDescriptor(
  name='AdGroupAdStatus',
  full_name='google.ads.googleads.v4.enums.AdGroupAdStatusEnum.AdGroupAdStatus',
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
      name='ENABLED', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PAUSED', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='REMOVED', index=4, number=4,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=148,
  serialized_end=233,
)
_sym_db.RegisterEnumDescriptor(_ADGROUPADSTATUSENUM_ADGROUPADSTATUS)


_ADGROUPADSTATUSENUM = _descriptor.Descriptor(
  name='AdGroupAdStatusEnum',
  full_name='google.ads.googleads.v4.enums.AdGroupAdStatusEnum',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _ADGROUPADSTATUSENUM_ADGROUPADSTATUS,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=125,
  serialized_end=233,
)

_ADGROUPADSTATUSENUM_ADGROUPADSTATUS.containing_type = _ADGROUPADSTATUSENUM
DESCRIPTOR.message_types_by_name['AdGroupAdStatusEnum'] = _ADGROUPADSTATUSENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

AdGroupAdStatusEnum = _reflection.GeneratedProtocolMessageType('AdGroupAdStatusEnum', (_message.Message,), dict(
  DESCRIPTOR = _ADGROUPADSTATUSENUM,
  __module__ = 'google.ads.googleads_v4.proto.enums.ad_group_ad_status_pb2'
  ,
  __doc__ = """Container for enum describing possible statuses of an AdGroupAd.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v4.enums.AdGroupAdStatusEnum)
  ))
_sym_db.RegisterMessage(AdGroupAdStatusEnum)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
