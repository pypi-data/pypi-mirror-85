# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v6/proto/errors/offline_user_data_job_error.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v6/proto/errors/offline_user_data_job_error.proto',
  package='google.ads.googleads.v6.errors',
  syntax='proto3',
  serialized_options=b'\n\"com.google.ads.googleads.v6.errorsB\034OfflineUserDataJobErrorProtoP\001ZDgoogle.golang.org/genproto/googleapis/ads/googleads/v6/errors;errors\242\002\003GAA\252\002\036Google.Ads.GoogleAds.V6.Errors\312\002\036Google\\Ads\\GoogleAds\\V6\\Errors\352\002\"Google::Ads::GoogleAds::V6::Errors',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\nFgoogle/ads/googleads_v6/proto/errors/offline_user_data_job_error.proto\x12\x1egoogle.ads.googleads.v6.errors\x1a\x1cgoogle/api/annotations.proto\"\xa8\x08\n\x1bOfflineUserDataJobErrorEnum\"\x88\x08\n\x17OfflineUserDataJobError\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x01\x12\x18\n\x14INVALID_USER_LIST_ID\x10\x03\x12\x1a\n\x16INVALID_USER_LIST_TYPE\x10\x04\x12 \n\x1cNOT_ON_ALLOWLIST_FOR_USER_ID\x10!\x12 \n\x1cINCOMPATIBLE_UPLOAD_KEY_TYPE\x10\x06\x12\x1b\n\x17MISSING_USER_IDENTIFIER\x10\x07\x12\x1c\n\x18INVALID_MOBILE_ID_FORMAT\x10\x08\x12\x1d\n\x19TOO_MANY_USER_IDENTIFIERS\x10\t\x12+\n\'NOT_ON_ALLOWLIST_FOR_STORE_SALES_DIRECT\x10\x1f\x12,\n(NOT_ON_ALLOWLIST_FOR_UNIFIED_STORE_SALES\x10 \x12\x16\n\x12INVALID_PARTNER_ID\x10\x0b\x12\x14\n\x10INVALID_ENCODING\x10\x0c\x12\x18\n\x14INVALID_COUNTRY_CODE\x10\r\x12 \n\x1cINCOMPATIBLE_USER_IDENTIFIER\x10\x0e\x12\x1b\n\x17\x46UTURE_TRANSACTION_TIME\x10\x0f\x12\x1d\n\x19INVALID_CONVERSION_ACTION\x10\x10\x12\x1b\n\x17MOBILE_ID_NOT_SUPPORTED\x10\x11\x12\x1b\n\x17INVALID_OPERATION_ORDER\x10\x12\x12\x19\n\x15\x43ONFLICTING_OPERATION\x10\x13\x12%\n!EXTERNAL_UPDATE_ID_ALREADY_EXISTS\x10\x15\x12\x17\n\x13JOB_ALREADY_STARTED\x10\x16\x12\x18\n\x14REMOVE_NOT_SUPPORTED\x10\x17\x12\x1c\n\x18REMOVE_ALL_NOT_SUPPORTED\x10\x18\x12\x19\n\x15INVALID_SHA256_FORMAT\x10\x19\x12\x17\n\x13\x43USTOM_KEY_DISABLED\x10\x1a\x12\x1d\n\x19\x43USTOM_KEY_NOT_PREDEFINED\x10\x1b\x12\x16\n\x12\x43USTOM_KEY_NOT_SET\x10\x1d\x12-\n)CUSTOMER_NOT_ACCEPTED_CUSTOMER_DATA_TERMS\x10\x1e\x12:\n6ATTRIBUTES_NOT_APPLICABLE_FOR_CUSTOMER_MATCH_USER_LIST\x10\"\x12&\n\"LIFETIME_VALUE_BUCKET_NOT_IN_RANGE\x10#\x12/\n+INCOMPATIBLE_USER_IDENTIFIER_FOR_ATTRIBUTES\x10$B\xf7\x01\n\"com.google.ads.googleads.v6.errorsB\x1cOfflineUserDataJobErrorProtoP\x01ZDgoogle.golang.org/genproto/googleapis/ads/googleads/v6/errors;errors\xa2\x02\x03GAA\xaa\x02\x1eGoogle.Ads.GoogleAds.V6.Errors\xca\x02\x1eGoogle\\Ads\\GoogleAds\\V6\\Errors\xea\x02\"Google::Ads::GoogleAds::V6::Errorsb\x06proto3'
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,])



_OFFLINEUSERDATAJOBERRORENUM_OFFLINEUSERDATAJOBERROR = _descriptor.EnumDescriptor(
  name='OfflineUserDataJobError',
  full_name='google.ads.googleads.v6.errors.OfflineUserDataJobErrorEnum.OfflineUserDataJobError',
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
      name='INVALID_USER_LIST_ID', index=2, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='INVALID_USER_LIST_TYPE', index=3, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='NOT_ON_ALLOWLIST_FOR_USER_ID', index=4, number=33,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='INCOMPATIBLE_UPLOAD_KEY_TYPE', index=5, number=6,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='MISSING_USER_IDENTIFIER', index=6, number=7,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='INVALID_MOBILE_ID_FORMAT', index=7, number=8,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='TOO_MANY_USER_IDENTIFIERS', index=8, number=9,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='NOT_ON_ALLOWLIST_FOR_STORE_SALES_DIRECT', index=9, number=31,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='NOT_ON_ALLOWLIST_FOR_UNIFIED_STORE_SALES', index=10, number=32,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='INVALID_PARTNER_ID', index=11, number=11,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='INVALID_ENCODING', index=12, number=12,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='INVALID_COUNTRY_CODE', index=13, number=13,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='INCOMPATIBLE_USER_IDENTIFIER', index=14, number=14,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='FUTURE_TRANSACTION_TIME', index=15, number=15,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='INVALID_CONVERSION_ACTION', index=16, number=16,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='MOBILE_ID_NOT_SUPPORTED', index=17, number=17,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='INVALID_OPERATION_ORDER', index=18, number=18,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='CONFLICTING_OPERATION', index=19, number=19,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='EXTERNAL_UPDATE_ID_ALREADY_EXISTS', index=20, number=21,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='JOB_ALREADY_STARTED', index=21, number=22,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='REMOVE_NOT_SUPPORTED', index=22, number=23,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='REMOVE_ALL_NOT_SUPPORTED', index=23, number=24,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='INVALID_SHA256_FORMAT', index=24, number=25,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='CUSTOM_KEY_DISABLED', index=25, number=26,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='CUSTOM_KEY_NOT_PREDEFINED', index=26, number=27,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='CUSTOM_KEY_NOT_SET', index=27, number=29,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='CUSTOMER_NOT_ACCEPTED_CUSTOMER_DATA_TERMS', index=28, number=30,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='ATTRIBUTES_NOT_APPLICABLE_FOR_CUSTOMER_MATCH_USER_LIST', index=29, number=34,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='LIFETIME_VALUE_BUCKET_NOT_IN_RANGE', index=30, number=35,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='INCOMPATIBLE_USER_IDENTIFIER_FOR_ATTRIBUTES', index=31, number=36,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=169,
  serialized_end=1201,
)
_sym_db.RegisterEnumDescriptor(_OFFLINEUSERDATAJOBERRORENUM_OFFLINEUSERDATAJOBERROR)


_OFFLINEUSERDATAJOBERRORENUM = _descriptor.Descriptor(
  name='OfflineUserDataJobErrorEnum',
  full_name='google.ads.googleads.v6.errors.OfflineUserDataJobErrorEnum',
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
    _OFFLINEUSERDATAJOBERRORENUM_OFFLINEUSERDATAJOBERROR,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=137,
  serialized_end=1201,
)

_OFFLINEUSERDATAJOBERRORENUM_OFFLINEUSERDATAJOBERROR.containing_type = _OFFLINEUSERDATAJOBERRORENUM
DESCRIPTOR.message_types_by_name['OfflineUserDataJobErrorEnum'] = _OFFLINEUSERDATAJOBERRORENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

OfflineUserDataJobErrorEnum = _reflection.GeneratedProtocolMessageType('OfflineUserDataJobErrorEnum', (_message.Message,), {
  'DESCRIPTOR' : _OFFLINEUSERDATAJOBERRORENUM,
  '__module__' : 'google.ads.googleads_v6.proto.errors.offline_user_data_job_error_pb2'
  ,
  '__doc__': """Container for enum describing possible offline user data job errors.""",
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v6.errors.OfflineUserDataJobErrorEnum)
  })
_sym_db.RegisterMessage(OfflineUserDataJobErrorEnum)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
