# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v4/proto/enums/customer_match_upload_key_type.proto

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
  name='google/ads/googleads_v4/proto/enums/customer_match_upload_key_type.proto',
  package='google.ads.googleads.v4.enums',
  syntax='proto3',
  serialized_options=_b('\n!com.google.ads.googleads.v4.enumsB\037CustomerMatchUploadKeyTypeProtoP\001ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v4/enums;enums\242\002\003GAA\252\002\035Google.Ads.GoogleAds.V4.Enums\312\002\035Google\\Ads\\GoogleAds\\V4\\Enums\352\002!Google::Ads::GoogleAds::V4::Enums'),
  serialized_pb=_b('\nHgoogle/ads/googleads_v4/proto/enums/customer_match_upload_key_type.proto\x12\x1dgoogle.ads.googleads.v4.enums\x1a\x1cgoogle/api/annotations.proto\"\x95\x01\n\x1e\x43ustomerMatchUploadKeyTypeEnum\"s\n\x1a\x43ustomerMatchUploadKeyType\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x01\x12\x10\n\x0c\x43ONTACT_INFO\x10\x02\x12\n\n\x06\x43RM_ID\x10\x03\x12\x19\n\x15MOBILE_ADVERTISING_ID\x10\x04\x42\xf4\x01\n!com.google.ads.googleads.v4.enumsB\x1f\x43ustomerMatchUploadKeyTypeProtoP\x01ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v4/enums;enums\xa2\x02\x03GAA\xaa\x02\x1dGoogle.Ads.GoogleAds.V4.Enums\xca\x02\x1dGoogle\\Ads\\GoogleAds\\V4\\Enums\xea\x02!Google::Ads::GoogleAds::V4::Enumsb\x06proto3')
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,])



_CUSTOMERMATCHUPLOADKEYTYPEENUM_CUSTOMERMATCHUPLOADKEYTYPE = _descriptor.EnumDescriptor(
  name='CustomerMatchUploadKeyType',
  full_name='google.ads.googleads.v4.enums.CustomerMatchUploadKeyTypeEnum.CustomerMatchUploadKeyType',
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
      name='CONTACT_INFO', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CRM_ID', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MOBILE_ADVERTISING_ID', index=4, number=4,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=172,
  serialized_end=287,
)
_sym_db.RegisterEnumDescriptor(_CUSTOMERMATCHUPLOADKEYTYPEENUM_CUSTOMERMATCHUPLOADKEYTYPE)


_CUSTOMERMATCHUPLOADKEYTYPEENUM = _descriptor.Descriptor(
  name='CustomerMatchUploadKeyTypeEnum',
  full_name='google.ads.googleads.v4.enums.CustomerMatchUploadKeyTypeEnum',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _CUSTOMERMATCHUPLOADKEYTYPEENUM_CUSTOMERMATCHUPLOADKEYTYPE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=138,
  serialized_end=287,
)

_CUSTOMERMATCHUPLOADKEYTYPEENUM_CUSTOMERMATCHUPLOADKEYTYPE.containing_type = _CUSTOMERMATCHUPLOADKEYTYPEENUM
DESCRIPTOR.message_types_by_name['CustomerMatchUploadKeyTypeEnum'] = _CUSTOMERMATCHUPLOADKEYTYPEENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

CustomerMatchUploadKeyTypeEnum = _reflection.GeneratedProtocolMessageType('CustomerMatchUploadKeyTypeEnum', (_message.Message,), dict(
  DESCRIPTOR = _CUSTOMERMATCHUPLOADKEYTYPEENUM,
  __module__ = 'google.ads.googleads_v4.proto.enums.customer_match_upload_key_type_pb2'
  ,
  __doc__ = """Indicates what type of data are the user list's members matched from.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v4.enums.CustomerMatchUploadKeyTypeEnum)
  ))
_sym_db.RegisterMessage(CustomerMatchUploadKeyTypeEnum)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
