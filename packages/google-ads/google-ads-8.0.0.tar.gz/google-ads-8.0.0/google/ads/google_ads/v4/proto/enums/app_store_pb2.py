# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v4/proto/enums/app_store.proto

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
  name='google/ads/googleads_v4/proto/enums/app_store.proto',
  package='google.ads.googleads.v4.enums',
  syntax='proto3',
  serialized_options=_b('\n!com.google.ads.googleads.v4.enumsB\rAppStoreProtoP\001ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v4/enums;enums\242\002\003GAA\252\002\035Google.Ads.GoogleAds.V4.Enums\312\002\035Google\\Ads\\GoogleAds\\V4\\Enums\352\002!Google::Ads::GoogleAds::V4::Enums'),
  serialized_pb=_b('\n3google/ads/googleads_v4/proto/enums/app_store.proto\x12\x1dgoogle.ads.googleads.v4.enums\x1a\x1cgoogle/api/annotations.proto\"[\n\x0c\x41ppStoreEnum\"K\n\x08\x41ppStore\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x01\x12\x10\n\x0c\x41PPLE_ITUNES\x10\x02\x12\x0f\n\x0bGOOGLE_PLAY\x10\x03\x42\xe2\x01\n!com.google.ads.googleads.v4.enumsB\rAppStoreProtoP\x01ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v4/enums;enums\xa2\x02\x03GAA\xaa\x02\x1dGoogle.Ads.GoogleAds.V4.Enums\xca\x02\x1dGoogle\\Ads\\GoogleAds\\V4\\Enums\xea\x02!Google::Ads::GoogleAds::V4::Enumsb\x06proto3')
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,])



_APPSTOREENUM_APPSTORE = _descriptor.EnumDescriptor(
  name='AppStore',
  full_name='google.ads.googleads.v4.enums.AppStoreEnum.AppStore',
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
      name='APPLE_ITUNES', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='GOOGLE_PLAY', index=3, number=3,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=132,
  serialized_end=207,
)
_sym_db.RegisterEnumDescriptor(_APPSTOREENUM_APPSTORE)


_APPSTOREENUM = _descriptor.Descriptor(
  name='AppStoreEnum',
  full_name='google.ads.googleads.v4.enums.AppStoreEnum',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _APPSTOREENUM_APPSTORE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=116,
  serialized_end=207,
)

_APPSTOREENUM_APPSTORE.containing_type = _APPSTOREENUM
DESCRIPTOR.message_types_by_name['AppStoreEnum'] = _APPSTOREENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

AppStoreEnum = _reflection.GeneratedProtocolMessageType('AppStoreEnum', (_message.Message,), dict(
  DESCRIPTOR = _APPSTOREENUM,
  __module__ = 'google.ads.googleads_v4.proto.enums.app_store_pb2'
  ,
  __doc__ = """Container for enum describing app store type in an app extension.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v4.enums.AppStoreEnum)
  ))
_sym_db.RegisterMessage(AppStoreEnum)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
