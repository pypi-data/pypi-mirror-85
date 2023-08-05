# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v5/proto/enums/user_list_crm_data_source_type.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v5/proto/enums/user_list_crm_data_source_type.proto',
  package='google.ads.googleads.v5.enums',
  syntax='proto3',
  serialized_options=b'\n!com.google.ads.googleads.v5.enumsB\036UserListCrmDataSourceTypeProtoP\001ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v5/enums;enums\242\002\003GAA\252\002\035Google.Ads.GoogleAds.V5.Enums\312\002\035Google\\Ads\\GoogleAds\\V5\\Enums\352\002!Google::Ads::GoogleAds::V5::Enums',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\nHgoogle/ads/googleads_v5/proto/enums/user_list_crm_data_source_type.proto\x12\x1dgoogle.ads.googleads.v5.enums\x1a\x1cgoogle/api/annotations.proto\"\xa7\x01\n\x1dUserListCrmDataSourceTypeEnum\"\x85\x01\n\x19UserListCrmDataSourceType\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x01\x12\x0f\n\x0b\x46IRST_PARTY\x10\x02\x12\x1d\n\x19THIRD_PARTY_CREDIT_BUREAU\x10\x03\x12\x1a\n\x16THIRD_PARTY_VOTER_FILE\x10\x04\x42\xf3\x01\n!com.google.ads.googleads.v5.enumsB\x1eUserListCrmDataSourceTypeProtoP\x01ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v5/enums;enums\xa2\x02\x03GAA\xaa\x02\x1dGoogle.Ads.GoogleAds.V5.Enums\xca\x02\x1dGoogle\\Ads\\GoogleAds\\V5\\Enums\xea\x02!Google::Ads::GoogleAds::V5::Enumsb\x06proto3'
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,])



_USERLISTCRMDATASOURCETYPEENUM_USERLISTCRMDATASOURCETYPE = _descriptor.EnumDescriptor(
  name='UserListCrmDataSourceType',
  full_name='google.ads.googleads.v5.enums.UserListCrmDataSourceTypeEnum.UserListCrmDataSourceType',
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
      name='FIRST_PARTY', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='THIRD_PARTY_CREDIT_BUREAU', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='THIRD_PARTY_VOTER_FILE', index=4, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=172,
  serialized_end=305,
)
_sym_db.RegisterEnumDescriptor(_USERLISTCRMDATASOURCETYPEENUM_USERLISTCRMDATASOURCETYPE)


_USERLISTCRMDATASOURCETYPEENUM = _descriptor.Descriptor(
  name='UserListCrmDataSourceTypeEnum',
  full_name='google.ads.googleads.v5.enums.UserListCrmDataSourceTypeEnum',
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
    _USERLISTCRMDATASOURCETYPEENUM_USERLISTCRMDATASOURCETYPE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=138,
  serialized_end=305,
)

_USERLISTCRMDATASOURCETYPEENUM_USERLISTCRMDATASOURCETYPE.containing_type = _USERLISTCRMDATASOURCETYPEENUM
DESCRIPTOR.message_types_by_name['UserListCrmDataSourceTypeEnum'] = _USERLISTCRMDATASOURCETYPEENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

UserListCrmDataSourceTypeEnum = _reflection.GeneratedProtocolMessageType('UserListCrmDataSourceTypeEnum', (_message.Message,), {
  'DESCRIPTOR' : _USERLISTCRMDATASOURCETYPEENUM,
  '__module__' : 'google.ads.googleads_v5.proto.enums.user_list_crm_data_source_type_pb2'
  ,
  '__doc__': """Indicates source of Crm upload data.""",
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v5.enums.UserListCrmDataSourceTypeEnum)
  })
_sym_db.RegisterMessage(UserListCrmDataSourceTypeEnum)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
