# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v3/proto/enums/feed_item_quality_approval_status.proto

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
  name='google/ads/googleads_v3/proto/enums/feed_item_quality_approval_status.proto',
  package='google.ads.googleads.v3.enums',
  syntax='proto3',
  serialized_options=_b('\n!com.google.ads.googleads.v3.enumsB\"FeedItemQualityApprovalStatusProtoP\001ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v3/enums;enums\242\002\003GAA\252\002\035Google.Ads.GoogleAds.V3.Enums\312\002\035Google\\Ads\\GoogleAds\\V3\\Enums\352\002!Google::Ads::GoogleAds::V3::Enums'),
  serialized_pb=_b('\nKgoogle/ads/googleads_v3/proto/enums/feed_item_quality_approval_status.proto\x12\x1dgoogle.ads.googleads.v3.enums\x1a\x1cgoogle/api/annotations.proto\"\x81\x01\n!FeedItemQualityApprovalStatusEnum\"\\\n\x1d\x46\x65\x65\x64ItemQualityApprovalStatus\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x01\x12\x0c\n\x08\x41PPROVED\x10\x02\x12\x0f\n\x0b\x44ISAPPROVED\x10\x03\x42\xf7\x01\n!com.google.ads.googleads.v3.enumsB\"FeedItemQualityApprovalStatusProtoP\x01ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v3/enums;enums\xa2\x02\x03GAA\xaa\x02\x1dGoogle.Ads.GoogleAds.V3.Enums\xca\x02\x1dGoogle\\Ads\\GoogleAds\\V3\\Enums\xea\x02!Google::Ads::GoogleAds::V3::Enumsb\x06proto3')
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,])



_FEEDITEMQUALITYAPPROVALSTATUSENUM_FEEDITEMQUALITYAPPROVALSTATUS = _descriptor.EnumDescriptor(
  name='FeedItemQualityApprovalStatus',
  full_name='google.ads.googleads.v3.enums.FeedItemQualityApprovalStatusEnum.FeedItemQualityApprovalStatus',
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
      name='APPROVED', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DISAPPROVED', index=3, number=3,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=178,
  serialized_end=270,
)
_sym_db.RegisterEnumDescriptor(_FEEDITEMQUALITYAPPROVALSTATUSENUM_FEEDITEMQUALITYAPPROVALSTATUS)


_FEEDITEMQUALITYAPPROVALSTATUSENUM = _descriptor.Descriptor(
  name='FeedItemQualityApprovalStatusEnum',
  full_name='google.ads.googleads.v3.enums.FeedItemQualityApprovalStatusEnum',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _FEEDITEMQUALITYAPPROVALSTATUSENUM_FEEDITEMQUALITYAPPROVALSTATUS,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=141,
  serialized_end=270,
)

_FEEDITEMQUALITYAPPROVALSTATUSENUM_FEEDITEMQUALITYAPPROVALSTATUS.containing_type = _FEEDITEMQUALITYAPPROVALSTATUSENUM
DESCRIPTOR.message_types_by_name['FeedItemQualityApprovalStatusEnum'] = _FEEDITEMQUALITYAPPROVALSTATUSENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

FeedItemQualityApprovalStatusEnum = _reflection.GeneratedProtocolMessageType('FeedItemQualityApprovalStatusEnum', (_message.Message,), dict(
  DESCRIPTOR = _FEEDITEMQUALITYAPPROVALSTATUSENUM,
  __module__ = 'google.ads.googleads_v3.proto.enums.feed_item_quality_approval_status_pb2'
  ,
  __doc__ = """Container for enum describing possible quality evaluation approval
  statuses of a feed item.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v3.enums.FeedItemQualityApprovalStatusEnum)
  ))
_sym_db.RegisterMessage(FeedItemQualityApprovalStatusEnum)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
