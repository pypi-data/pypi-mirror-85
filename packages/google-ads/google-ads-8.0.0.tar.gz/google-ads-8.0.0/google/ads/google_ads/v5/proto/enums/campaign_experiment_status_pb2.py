# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v5/proto/enums/campaign_experiment_status.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v5/proto/enums/campaign_experiment_status.proto',
  package='google.ads.googleads.v5.enums',
  syntax='proto3',
  serialized_options=b'\n!com.google.ads.googleads.v5.enumsB\035CampaignExperimentStatusProtoP\001ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v5/enums;enums\242\002\003GAA\252\002\035Google.Ads.GoogleAds.V5.Enums\312\002\035Google\\Ads\\GoogleAds\\V5\\Enums\352\002!Google::Ads::GoogleAds::V5::Enums',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\nDgoogle/ads/googleads_v5/proto/enums/campaign_experiment_status.proto\x12\x1dgoogle.ads.googleads.v5.enums\x1a\x1cgoogle/api/annotations.proto\"\xf6\x01\n\x1c\x43\x61mpaignExperimentStatusEnum\"\xd5\x01\n\x18\x43\x61mpaignExperimentStatus\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x01\x12\x10\n\x0cINITIALIZING\x10\x02\x12\x19\n\x15INITIALIZATION_FAILED\x10\x08\x12\x0b\n\x07\x45NABLED\x10\x03\x12\r\n\tGRADUATED\x10\x04\x12\x0b\n\x07REMOVED\x10\x05\x12\r\n\tPROMOTING\x10\x06\x12\x14\n\x10PROMOTION_FAILED\x10\t\x12\x0c\n\x08PROMOTED\x10\x07\x12\x12\n\x0e\x45NDED_MANUALLY\x10\nB\xf2\x01\n!com.google.ads.googleads.v5.enumsB\x1d\x43\x61mpaignExperimentStatusProtoP\x01ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v5/enums;enums\xa2\x02\x03GAA\xaa\x02\x1dGoogle.Ads.GoogleAds.V5.Enums\xca\x02\x1dGoogle\\Ads\\GoogleAds\\V5\\Enums\xea\x02!Google::Ads::GoogleAds::V5::Enumsb\x06proto3'
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,])



_CAMPAIGNEXPERIMENTSTATUSENUM_CAMPAIGNEXPERIMENTSTATUS = _descriptor.EnumDescriptor(
  name='CampaignExperimentStatus',
  full_name='google.ads.googleads.v5.enums.CampaignExperimentStatusEnum.CampaignExperimentStatus',
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
      name='INITIALIZING', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='INITIALIZATION_FAILED', index=3, number=8,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='ENABLED', index=4, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='GRADUATED', index=5, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='REMOVED', index=6, number=5,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='PROMOTING', index=7, number=6,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='PROMOTION_FAILED', index=8, number=9,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='PROMOTED', index=9, number=7,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='ENDED_MANUALLY', index=10, number=10,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=167,
  serialized_end=380,
)
_sym_db.RegisterEnumDescriptor(_CAMPAIGNEXPERIMENTSTATUSENUM_CAMPAIGNEXPERIMENTSTATUS)


_CAMPAIGNEXPERIMENTSTATUSENUM = _descriptor.Descriptor(
  name='CampaignExperimentStatusEnum',
  full_name='google.ads.googleads.v5.enums.CampaignExperimentStatusEnum',
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
    _CAMPAIGNEXPERIMENTSTATUSENUM_CAMPAIGNEXPERIMENTSTATUS,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=134,
  serialized_end=380,
)

_CAMPAIGNEXPERIMENTSTATUSENUM_CAMPAIGNEXPERIMENTSTATUS.containing_type = _CAMPAIGNEXPERIMENTSTATUSENUM
DESCRIPTOR.message_types_by_name['CampaignExperimentStatusEnum'] = _CAMPAIGNEXPERIMENTSTATUSENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

CampaignExperimentStatusEnum = _reflection.GeneratedProtocolMessageType('CampaignExperimentStatusEnum', (_message.Message,), {
  'DESCRIPTOR' : _CAMPAIGNEXPERIMENTSTATUSENUM,
  '__module__' : 'google.ads.googleads_v5.proto.enums.campaign_experiment_status_pb2'
  ,
  '__doc__': """Container for enum describing possible statuses of a campaign
  experiment.""",
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v5.enums.CampaignExperimentStatusEnum)
  })
_sym_db.RegisterMessage(CampaignExperimentStatusEnum)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
