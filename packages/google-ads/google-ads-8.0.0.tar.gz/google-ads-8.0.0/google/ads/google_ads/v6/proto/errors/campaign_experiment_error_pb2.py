# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v6/proto/errors/campaign_experiment_error.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v6/proto/errors/campaign_experiment_error.proto',
  package='google.ads.googleads.v6.errors',
  syntax='proto3',
  serialized_options=b'\n\"com.google.ads.googleads.v6.errorsB\034CampaignExperimentErrorProtoP\001ZDgoogle.golang.org/genproto/googleapis/ads/googleads/v6/errors;errors\242\002\003GAA\252\002\036Google.Ads.GoogleAds.V6.Errors\312\002\036Google\\Ads\\GoogleAds\\V6\\Errors\352\002\"Google::Ads::GoogleAds::V6::Errors',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\nDgoogle/ads/googleads_v6/proto/errors/campaign_experiment_error.proto\x12\x1egoogle.ads.googleads.v6.errors\x1a\x1cgoogle/api/annotations.proto\"\x80\x04\n\x1b\x43\x61mpaignExperimentErrorEnum\"\xe0\x03\n\x17\x43\x61mpaignExperimentError\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x01\x12\x12\n\x0e\x44UPLICATE_NAME\x10\x02\x12\x16\n\x12INVALID_TRANSITION\x10\x03\x12/\n+CANNOT_CREATE_EXPERIMENT_WITH_SHARED_BUDGET\x10\x04\x12\x36\n2CANNOT_CREATE_EXPERIMENT_FOR_REMOVED_BASE_CAMPAIGN\x10\x05\x12\x33\n/CANNOT_CREATE_EXPERIMENT_FOR_NON_PROPOSED_DRAFT\x10\x06\x12%\n!CUSTOMER_CANNOT_CREATE_EXPERIMENT\x10\x07\x12%\n!CAMPAIGN_CANNOT_CREATE_EXPERIMENT\x10\x08\x12)\n%EXPERIMENT_DURATIONS_MUST_NOT_OVERLAP\x10\t\x12\x38\n4EXPERIMENT_DURATION_MUST_BE_WITHIN_CAMPAIGN_DURATION\x10\n\x12*\n&CANNOT_MUTATE_EXPERIMENT_DUE_TO_STATUS\x10\x0b\x42\xf7\x01\n\"com.google.ads.googleads.v6.errorsB\x1c\x43\x61mpaignExperimentErrorProtoP\x01ZDgoogle.golang.org/genproto/googleapis/ads/googleads/v6/errors;errors\xa2\x02\x03GAA\xaa\x02\x1eGoogle.Ads.GoogleAds.V6.Errors\xca\x02\x1eGoogle\\Ads\\GoogleAds\\V6\\Errors\xea\x02\"Google::Ads::GoogleAds::V6::Errorsb\x06proto3'
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,])



_CAMPAIGNEXPERIMENTERRORENUM_CAMPAIGNEXPERIMENTERROR = _descriptor.EnumDescriptor(
  name='CampaignExperimentError',
  full_name='google.ads.googleads.v6.errors.CampaignExperimentErrorEnum.CampaignExperimentError',
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
      name='DUPLICATE_NAME', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='INVALID_TRANSITION', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='CANNOT_CREATE_EXPERIMENT_WITH_SHARED_BUDGET', index=4, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='CANNOT_CREATE_EXPERIMENT_FOR_REMOVED_BASE_CAMPAIGN', index=5, number=5,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='CANNOT_CREATE_EXPERIMENT_FOR_NON_PROPOSED_DRAFT', index=6, number=6,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='CUSTOMER_CANNOT_CREATE_EXPERIMENT', index=7, number=7,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='CAMPAIGN_CANNOT_CREATE_EXPERIMENT', index=8, number=8,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='EXPERIMENT_DURATIONS_MUST_NOT_OVERLAP', index=9, number=9,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='EXPERIMENT_DURATION_MUST_BE_WITHIN_CAMPAIGN_DURATION', index=10, number=10,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='CANNOT_MUTATE_EXPERIMENT_DUE_TO_STATUS', index=11, number=11,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=167,
  serialized_end=647,
)
_sym_db.RegisterEnumDescriptor(_CAMPAIGNEXPERIMENTERRORENUM_CAMPAIGNEXPERIMENTERROR)


_CAMPAIGNEXPERIMENTERRORENUM = _descriptor.Descriptor(
  name='CampaignExperimentErrorEnum',
  full_name='google.ads.googleads.v6.errors.CampaignExperimentErrorEnum',
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
    _CAMPAIGNEXPERIMENTERRORENUM_CAMPAIGNEXPERIMENTERROR,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=135,
  serialized_end=647,
)

_CAMPAIGNEXPERIMENTERRORENUM_CAMPAIGNEXPERIMENTERROR.containing_type = _CAMPAIGNEXPERIMENTERRORENUM
DESCRIPTOR.message_types_by_name['CampaignExperimentErrorEnum'] = _CAMPAIGNEXPERIMENTERRORENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

CampaignExperimentErrorEnum = _reflection.GeneratedProtocolMessageType('CampaignExperimentErrorEnum', (_message.Message,), {
  'DESCRIPTOR' : _CAMPAIGNEXPERIMENTERRORENUM,
  '__module__' : 'google.ads.googleads_v6.proto.errors.campaign_experiment_error_pb2'
  ,
  '__doc__': """Container for enum describing possible campaign experiment errors.""",
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v6.errors.CampaignExperimentErrorEnum)
  })
_sym_db.RegisterMessage(CampaignExperimentErrorEnum)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
