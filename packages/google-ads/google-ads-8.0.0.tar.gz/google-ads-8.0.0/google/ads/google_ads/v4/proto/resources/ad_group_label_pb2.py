# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v4/proto/resources/ad_group_label.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from google.api import resource_pb2 as google_dot_api_dot_resource__pb2
from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v4/proto/resources/ad_group_label.proto',
  package='google.ads.googleads.v4.resources',
  syntax='proto3',
  serialized_options=_b('\n%com.google.ads.googleads.v4.resourcesB\021AdGroupLabelProtoP\001ZJgoogle.golang.org/genproto/googleapis/ads/googleads/v4/resources;resources\242\002\003GAA\252\002!Google.Ads.GoogleAds.V4.Resources\312\002!Google\\Ads\\GoogleAds\\V4\\Resources\352\002%Google::Ads::GoogleAds::V4::Resources'),
  serialized_pb=_b('\n<google/ads/googleads_v4/proto/resources/ad_group_label.proto\x12!google.ads.googleads.v4.resources\x1a\x1fgoogle/api/field_behavior.proto\x1a\x19google/api/resource.proto\x1a\x1egoogle/protobuf/wrappers.proto\x1a\x1cgoogle/api/annotations.proto\"\xe4\x02\n\x0c\x41\x64GroupLabel\x12\x44\n\rresource_name\x18\x01 \x01(\tB-\xe0\x41\x05\xfa\x41\'\n%googleads.googleapis.com/AdGroupLabel\x12X\n\x08\x61\x64_group\x18\x02 \x01(\x0b\x32\x1c.google.protobuf.StringValueB(\xe0\x41\x05\xfa\x41\"\n googleads.googleapis.com/AdGroup\x12S\n\x05label\x18\x03 \x01(\x0b\x32\x1c.google.protobuf.StringValueB&\xe0\x41\x05\xfa\x41 \n\x1egoogleads.googleapis.com/Label:_\xea\x41\\\n%googleads.googleapis.com/AdGroupLabel\x12\x33\x63ustomers/{customer}/adGroupLabels/{ad_group_label}B\xfe\x01\n%com.google.ads.googleads.v4.resourcesB\x11\x41\x64GroupLabelProtoP\x01ZJgoogle.golang.org/genproto/googleapis/ads/googleads/v4/resources;resources\xa2\x02\x03GAA\xaa\x02!Google.Ads.GoogleAds.V4.Resources\xca\x02!Google\\Ads\\GoogleAds\\V4\\Resources\xea\x02%Google::Ads::GoogleAds::V4::Resourcesb\x06proto3')
  ,
  dependencies=[google_dot_api_dot_field__behavior__pb2.DESCRIPTOR,google_dot_api_dot_resource__pb2.DESCRIPTOR,google_dot_protobuf_dot_wrappers__pb2.DESCRIPTOR,google_dot_api_dot_annotations__pb2.DESCRIPTOR,])




_ADGROUPLABEL = _descriptor.Descriptor(
  name='AdGroupLabel',
  full_name='google.ads.googleads.v4.resources.AdGroupLabel',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_name', full_name='google.ads.googleads.v4.resources.AdGroupLabel.resource_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\005\372A\'\n%googleads.googleapis.com/AdGroupLabel'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ad_group', full_name='google.ads.googleads.v4.resources.AdGroupLabel.ad_group', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\005\372A\"\n googleads.googleapis.com/AdGroup'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='label', full_name='google.ads.googleads.v4.resources.AdGroupLabel.label', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\005\372A \n\036googleads.googleapis.com/Label'), file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=_b('\352A\\\n%googleads.googleapis.com/AdGroupLabel\0223customers/{customer}/adGroupLabels/{ad_group_label}'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=222,
  serialized_end=578,
)

_ADGROUPLABEL.fields_by_name['ad_group'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_ADGROUPLABEL.fields_by_name['label'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
DESCRIPTOR.message_types_by_name['AdGroupLabel'] = _ADGROUPLABEL
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

AdGroupLabel = _reflection.GeneratedProtocolMessageType('AdGroupLabel', (_message.Message,), dict(
  DESCRIPTOR = _ADGROUPLABEL,
  __module__ = 'google.ads.googleads_v4.proto.resources.ad_group_label_pb2'
  ,
  __doc__ = """A relationship between an ad group and a label.
  
  
  Attributes:
      resource_name:
          Immutable. The resource name of the ad group label. Ad group
          label resource names have the form: ``customers/{customer_id}/
          adGroupLabels/{ad_group_id}~{label_id}``
      ad_group:
          Immutable. The ad group to which the label is attached.
      label:
          Immutable. The label assigned to the ad group.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v4.resources.AdGroupLabel)
  ))
_sym_db.RegisterMessage(AdGroupLabel)


DESCRIPTOR._options = None
_ADGROUPLABEL.fields_by_name['resource_name']._options = None
_ADGROUPLABEL.fields_by_name['ad_group']._options = None
_ADGROUPLABEL.fields_by_name['label']._options = None
_ADGROUPLABEL._options = None
# @@protoc_insertion_point(module_scope)
