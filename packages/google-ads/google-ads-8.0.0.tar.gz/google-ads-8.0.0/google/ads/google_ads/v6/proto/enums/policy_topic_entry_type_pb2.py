# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v6/proto/enums/policy_topic_entry_type.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v6/proto/enums/policy_topic_entry_type.proto',
  package='google.ads.googleads.v6.enums',
  syntax='proto3',
  serialized_options=b'\n!com.google.ads.googleads.v6.enumsB\031PolicyTopicEntryTypeProtoP\001ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v6/enums;enums\242\002\003GAA\252\002\035Google.Ads.GoogleAds.V6.Enums\312\002\035Google\\Ads\\GoogleAds\\V6\\Enums\352\002!Google::Ads::GoogleAds::V6::Enums',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\nAgoogle/ads/googleads_v6/proto/enums/policy_topic_entry_type.proto\x12\x1dgoogle.ads.googleads.v6.enums\x1a\x1cgoogle/api/annotations.proto\"\xbd\x01\n\x18PolicyTopicEntryTypeEnum\"\xa0\x01\n\x14PolicyTopicEntryType\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x01\x12\x0e\n\nPROHIBITED\x10\x02\x12\x0b\n\x07LIMITED\x10\x04\x12\x11\n\rFULLY_LIMITED\x10\x08\x12\x0f\n\x0b\x44\x45SCRIPTIVE\x10\x05\x12\x0e\n\nBROADENING\x10\x06\x12\x19\n\x15\x41REA_OF_INTEREST_ONLY\x10\x07\x42\xee\x01\n!com.google.ads.googleads.v6.enumsB\x19PolicyTopicEntryTypeProtoP\x01ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v6/enums;enums\xa2\x02\x03GAA\xaa\x02\x1dGoogle.Ads.GoogleAds.V6.Enums\xca\x02\x1dGoogle\\Ads\\GoogleAds\\V6\\Enums\xea\x02!Google::Ads::GoogleAds::V6::Enumsb\x06proto3'
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,])



_POLICYTOPICENTRYTYPEENUM_POLICYTOPICENTRYTYPE = _descriptor.EnumDescriptor(
  name='PolicyTopicEntryType',
  full_name='google.ads.googleads.v6.enums.PolicyTopicEntryTypeEnum.PolicyTopicEntryType',
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
      name='PROHIBITED', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='LIMITED', index=3, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='FULLY_LIMITED', index=4, number=8,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DESCRIPTIVE', index=5, number=5,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='BROADENING', index=6, number=6,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='AREA_OF_INTEREST_ONLY', index=7, number=7,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=160,
  serialized_end=320,
)
_sym_db.RegisterEnumDescriptor(_POLICYTOPICENTRYTYPEENUM_POLICYTOPICENTRYTYPE)


_POLICYTOPICENTRYTYPEENUM = _descriptor.Descriptor(
  name='PolicyTopicEntryTypeEnum',
  full_name='google.ads.googleads.v6.enums.PolicyTopicEntryTypeEnum',
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
    _POLICYTOPICENTRYTYPEENUM_POLICYTOPICENTRYTYPE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=131,
  serialized_end=320,
)

_POLICYTOPICENTRYTYPEENUM_POLICYTOPICENTRYTYPE.containing_type = _POLICYTOPICENTRYTYPEENUM
DESCRIPTOR.message_types_by_name['PolicyTopicEntryTypeEnum'] = _POLICYTOPICENTRYTYPEENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

PolicyTopicEntryTypeEnum = _reflection.GeneratedProtocolMessageType('PolicyTopicEntryTypeEnum', (_message.Message,), {
  'DESCRIPTOR' : _POLICYTOPICENTRYTYPEENUM,
  '__module__' : 'google.ads.googleads_v6.proto.enums.policy_topic_entry_type_pb2'
  ,
  '__doc__': """Container for enum describing possible policy topic entry types.""",
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v6.enums.PolicyTopicEntryTypeEnum)
  })
_sym_db.RegisterMessage(PolicyTopicEntryTypeEnum)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
