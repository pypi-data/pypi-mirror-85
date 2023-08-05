# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v4/proto/enums/ad_customizer_placeholder_field.proto

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
  name='google/ads/googleads_v4/proto/enums/ad_customizer_placeholder_field.proto',
  package='google.ads.googleads.v4.enums',
  syntax='proto3',
  serialized_options=_b('\n!com.google.ads.googleads.v4.enumsB!AdCustomizerPlaceholderFieldProtoP\001ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v4/enums;enums\242\002\003GAA\252\002\035Google.Ads.GoogleAds.V4.Enums\312\002\035Google\\Ads\\GoogleAds\\V4\\Enums\352\002!Google::Ads::GoogleAds::V4::Enums'),
  serialized_pb=_b('\nIgoogle/ads/googleads_v4/proto/enums/ad_customizer_placeholder_field.proto\x12\x1dgoogle.ads.googleads.v4.enums\x1a\x1cgoogle/api/annotations.proto\"\x8e\x01\n AdCustomizerPlaceholderFieldEnum\"j\n\x1c\x41\x64\x43ustomizerPlaceholderField\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x01\x12\x0b\n\x07INTEGER\x10\x02\x12\t\n\x05PRICE\x10\x03\x12\x08\n\x04\x44\x41TE\x10\x04\x12\n\n\x06STRING\x10\x05\x42\xf6\x01\n!com.google.ads.googleads.v4.enumsB!AdCustomizerPlaceholderFieldProtoP\x01ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v4/enums;enums\xa2\x02\x03GAA\xaa\x02\x1dGoogle.Ads.GoogleAds.V4.Enums\xca\x02\x1dGoogle\\Ads\\GoogleAds\\V4\\Enums\xea\x02!Google::Ads::GoogleAds::V4::Enumsb\x06proto3')
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,])



_ADCUSTOMIZERPLACEHOLDERFIELDENUM_ADCUSTOMIZERPLACEHOLDERFIELD = _descriptor.EnumDescriptor(
  name='AdCustomizerPlaceholderField',
  full_name='google.ads.googleads.v4.enums.AdCustomizerPlaceholderFieldEnum.AdCustomizerPlaceholderField',
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
      name='INTEGER', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PRICE', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DATE', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='STRING', index=5, number=5,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=175,
  serialized_end=281,
)
_sym_db.RegisterEnumDescriptor(_ADCUSTOMIZERPLACEHOLDERFIELDENUM_ADCUSTOMIZERPLACEHOLDERFIELD)


_ADCUSTOMIZERPLACEHOLDERFIELDENUM = _descriptor.Descriptor(
  name='AdCustomizerPlaceholderFieldEnum',
  full_name='google.ads.googleads.v4.enums.AdCustomizerPlaceholderFieldEnum',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _ADCUSTOMIZERPLACEHOLDERFIELDENUM_ADCUSTOMIZERPLACEHOLDERFIELD,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=139,
  serialized_end=281,
)

_ADCUSTOMIZERPLACEHOLDERFIELDENUM_ADCUSTOMIZERPLACEHOLDERFIELD.containing_type = _ADCUSTOMIZERPLACEHOLDERFIELDENUM
DESCRIPTOR.message_types_by_name['AdCustomizerPlaceholderFieldEnum'] = _ADCUSTOMIZERPLACEHOLDERFIELDENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

AdCustomizerPlaceholderFieldEnum = _reflection.GeneratedProtocolMessageType('AdCustomizerPlaceholderFieldEnum', (_message.Message,), dict(
  DESCRIPTOR = _ADCUSTOMIZERPLACEHOLDERFIELDENUM,
  __module__ = 'google.ads.googleads_v4.proto.enums.ad_customizer_placeholder_field_pb2'
  ,
  __doc__ = """Values for Ad Customizer placeholder fields.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v4.enums.AdCustomizerPlaceholderFieldEnum)
  ))
_sym_db.RegisterMessage(AdCustomizerPlaceholderFieldEnum)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
