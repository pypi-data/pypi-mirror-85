# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v5/proto/enums/account_budget_proposal_status.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v5/proto/enums/account_budget_proposal_status.proto',
  package='google.ads.googleads.v5.enums',
  syntax='proto3',
  serialized_options=b'\n!com.google.ads.googleads.v5.enumsB AccountBudgetProposalStatusProtoP\001ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v5/enums;enums\242\002\003GAA\252\002\035Google.Ads.GoogleAds.V5.Enums\312\002\035Google\\Ads\\GoogleAds\\V5\\Enums\352\002!Google::Ads::GoogleAds::V5::Enums',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\nHgoogle/ads/googleads_v5/proto/enums/account_budget_proposal_status.proto\x12\x1dgoogle.ads.googleads.v5.enums\x1a\x1cgoogle/api/annotations.proto\"\xaa\x01\n\x1f\x41\x63\x63ountBudgetProposalStatusEnum\"\x86\x01\n\x1b\x41\x63\x63ountBudgetProposalStatus\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x01\x12\x0b\n\x07PENDING\x10\x02\x12\x11\n\rAPPROVED_HELD\x10\x03\x12\x0c\n\x08\x41PPROVED\x10\x04\x12\r\n\tCANCELLED\x10\x05\x12\x0c\n\x08REJECTED\x10\x06\x42\xf5\x01\n!com.google.ads.googleads.v5.enumsB AccountBudgetProposalStatusProtoP\x01ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v5/enums;enums\xa2\x02\x03GAA\xaa\x02\x1dGoogle.Ads.GoogleAds.V5.Enums\xca\x02\x1dGoogle\\Ads\\GoogleAds\\V5\\Enums\xea\x02!Google::Ads::GoogleAds::V5::Enumsb\x06proto3'
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,])



_ACCOUNTBUDGETPROPOSALSTATUSENUM_ACCOUNTBUDGETPROPOSALSTATUS = _descriptor.EnumDescriptor(
  name='AccountBudgetProposalStatus',
  full_name='google.ads.googleads.v5.enums.AccountBudgetProposalStatusEnum.AccountBudgetProposalStatus',
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
      name='PENDING', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='APPROVED_HELD', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='APPROVED', index=4, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='CANCELLED', index=5, number=5,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='REJECTED', index=6, number=6,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=174,
  serialized_end=308,
)
_sym_db.RegisterEnumDescriptor(_ACCOUNTBUDGETPROPOSALSTATUSENUM_ACCOUNTBUDGETPROPOSALSTATUS)


_ACCOUNTBUDGETPROPOSALSTATUSENUM = _descriptor.Descriptor(
  name='AccountBudgetProposalStatusEnum',
  full_name='google.ads.googleads.v5.enums.AccountBudgetProposalStatusEnum',
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
    _ACCOUNTBUDGETPROPOSALSTATUSENUM_ACCOUNTBUDGETPROPOSALSTATUS,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=138,
  serialized_end=308,
)

_ACCOUNTBUDGETPROPOSALSTATUSENUM_ACCOUNTBUDGETPROPOSALSTATUS.containing_type = _ACCOUNTBUDGETPROPOSALSTATUSENUM
DESCRIPTOR.message_types_by_name['AccountBudgetProposalStatusEnum'] = _ACCOUNTBUDGETPROPOSALSTATUSENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

AccountBudgetProposalStatusEnum = _reflection.GeneratedProtocolMessageType('AccountBudgetProposalStatusEnum', (_message.Message,), {
  'DESCRIPTOR' : _ACCOUNTBUDGETPROPOSALSTATUSENUM,
  '__module__' : 'google.ads.googleads_v5.proto.enums.account_budget_proposal_status_pb2'
  ,
  '__doc__': """Message describing AccountBudgetProposal statuses.""",
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v5.enums.AccountBudgetProposalStatusEnum)
  })
_sym_db.RegisterMessage(AccountBudgetProposalStatusEnum)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
