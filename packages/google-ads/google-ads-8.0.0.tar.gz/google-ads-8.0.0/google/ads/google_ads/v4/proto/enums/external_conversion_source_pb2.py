# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v4/proto/enums/external_conversion_source.proto

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
  name='google/ads/googleads_v4/proto/enums/external_conversion_source.proto',
  package='google.ads.googleads.v4.enums',
  syntax='proto3',
  serialized_options=_b('\n!com.google.ads.googleads.v4.enumsB\035ExternalConversionSourceProtoP\001ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v4/enums;enums\242\002\003GAA\252\002\035Google.Ads.GoogleAds.V4.Enums\312\002\035Google\\Ads\\GoogleAds\\V4\\Enums\352\002!Google::Ads::GoogleAds::V4::Enums'),
  serialized_pb=_b('\nDgoogle/ads/googleads_v4/proto/enums/external_conversion_source.proto\x12\x1dgoogle.ads.googleads.v4.enums\x1a\x1cgoogle/api/annotations.proto\"\x98\x04\n\x1c\x45xternalConversionSourceEnum\"\xf7\x03\n\x18\x45xternalConversionSource\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x01\x12\x0b\n\x07WEBPAGE\x10\x02\x12\r\n\tANALYTICS\x10\x03\x12\n\n\x06UPLOAD\x10\x04\x12\x13\n\x0f\x41\x44_CALL_METRICS\x10\x05\x12\x18\n\x14WEBSITE_CALL_METRICS\x10\x06\x12\x10\n\x0cSTORE_VISITS\x10\x07\x12\x12\n\x0e\x41NDROID_IN_APP\x10\x08\x12\x0e\n\nIOS_IN_APP\x10\t\x12\x12\n\x0eIOS_FIRST_OPEN\x10\n\x12\x13\n\x0f\x41PP_UNSPECIFIED\x10\x0b\x12\x16\n\x12\x41NDROID_FIRST_OPEN\x10\x0c\x12\x10\n\x0cUPLOAD_CALLS\x10\r\x12\x0c\n\x08\x46IREBASE\x10\x0e\x12\x11\n\rCLICK_TO_CALL\x10\x0f\x12\x0e\n\nSALESFORCE\x10\x10\x12\x13\n\x0fSTORE_SALES_CRM\x10\x11\x12\x1f\n\x1bSTORE_SALES_PAYMENT_NETWORK\x10\x12\x12\x0f\n\x0bGOOGLE_PLAY\x10\x13\x12\x1d\n\x19THIRD_PARTY_APP_ANALYTICS\x10\x14\x12\x16\n\x12GOOGLE_ATTRIBUTION\x10\x15\x12\x1d\n\x19STORE_SALES_DIRECT_UPLOAD\x10\x17\x12\x0f\n\x0bSTORE_SALES\x10\x18\x42\xf2\x01\n!com.google.ads.googleads.v4.enumsB\x1d\x45xternalConversionSourceProtoP\x01ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v4/enums;enums\xa2\x02\x03GAA\xaa\x02\x1dGoogle.Ads.GoogleAds.V4.Enums\xca\x02\x1dGoogle\\Ads\\GoogleAds\\V4\\Enums\xea\x02!Google::Ads::GoogleAds::V4::Enumsb\x06proto3')
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,])



_EXTERNALCONVERSIONSOURCEENUM_EXTERNALCONVERSIONSOURCE = _descriptor.EnumDescriptor(
  name='ExternalConversionSource',
  full_name='google.ads.googleads.v4.enums.ExternalConversionSourceEnum.ExternalConversionSource',
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
      name='WEBPAGE', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ANALYTICS', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='UPLOAD', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='AD_CALL_METRICS', index=5, number=5,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WEBSITE_CALL_METRICS', index=6, number=6,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='STORE_VISITS', index=7, number=7,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ANDROID_IN_APP', index=8, number=8,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='IOS_IN_APP', index=9, number=9,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='IOS_FIRST_OPEN', index=10, number=10,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='APP_UNSPECIFIED', index=11, number=11,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ANDROID_FIRST_OPEN', index=12, number=12,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='UPLOAD_CALLS', index=13, number=13,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FIREBASE', index=14, number=14,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CLICK_TO_CALL', index=15, number=15,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SALESFORCE', index=16, number=16,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='STORE_SALES_CRM', index=17, number=17,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='STORE_SALES_PAYMENT_NETWORK', index=18, number=18,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='GOOGLE_PLAY', index=19, number=19,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='THIRD_PARTY_APP_ANALYTICS', index=20, number=20,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='GOOGLE_ATTRIBUTION', index=21, number=21,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='STORE_SALES_DIRECT_UPLOAD', index=22, number=23,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='STORE_SALES', index=23, number=24,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=167,
  serialized_end=670,
)
_sym_db.RegisterEnumDescriptor(_EXTERNALCONVERSIONSOURCEENUM_EXTERNALCONVERSIONSOURCE)


_EXTERNALCONVERSIONSOURCEENUM = _descriptor.Descriptor(
  name='ExternalConversionSourceEnum',
  full_name='google.ads.googleads.v4.enums.ExternalConversionSourceEnum',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _EXTERNALCONVERSIONSOURCEENUM_EXTERNALCONVERSIONSOURCE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=134,
  serialized_end=670,
)

_EXTERNALCONVERSIONSOURCEENUM_EXTERNALCONVERSIONSOURCE.containing_type = _EXTERNALCONVERSIONSOURCEENUM
DESCRIPTOR.message_types_by_name['ExternalConversionSourceEnum'] = _EXTERNALCONVERSIONSOURCEENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ExternalConversionSourceEnum = _reflection.GeneratedProtocolMessageType('ExternalConversionSourceEnum', (_message.Message,), dict(
  DESCRIPTOR = _EXTERNALCONVERSIONSOURCEENUM,
  __module__ = 'google.ads.googleads_v4.proto.enums.external_conversion_source_pb2'
  ,
  __doc__ = """Container for enum describing the external conversion source that is
  associated with a ConversionAction.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v4.enums.ExternalConversionSourceEnum)
  ))
_sym_db.RegisterMessage(ExternalConversionSourceEnum)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
