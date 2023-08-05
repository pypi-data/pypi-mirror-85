# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v3/proto/resources/expanded_landing_page_view.proto

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
  name='google/ads/googleads_v3/proto/resources/expanded_landing_page_view.proto',
  package='google.ads.googleads.v3.resources',
  syntax='proto3',
  serialized_options=_b('\n%com.google.ads.googleads.v3.resourcesB\034ExpandedLandingPageViewProtoP\001ZJgoogle.golang.org/genproto/googleapis/ads/googleads/v3/resources;resources\242\002\003GAA\252\002!Google.Ads.GoogleAds.V3.Resources\312\002!Google\\Ads\\GoogleAds\\V3\\Resources\352\002%Google::Ads::GoogleAds::V3::Resources'),
  serialized_pb=_b('\nHgoogle/ads/googleads_v3/proto/resources/expanded_landing_page_view.proto\x12!google.ads.googleads.v3.resources\x1a\x1fgoogle/api/field_behavior.proto\x1a\x19google/api/resource.proto\x1a\x1egoogle/protobuf/wrappers.proto\x1a\x1cgoogle/api/annotations.proto\"\xad\x02\n\x17\x45xpandedLandingPageView\x12O\n\rresource_name\x18\x01 \x01(\tB8\xe0\x41\x03\xfa\x41\x32\n0googleads.googleapis.com/ExpandedLandingPageView\x12=\n\x12\x65xpanded_final_url\x18\x02 \x01(\x0b\x32\x1c.google.protobuf.StringValueB\x03\xe0\x41\x03:\x81\x01\xea\x41~\n0googleads.googleapis.com/ExpandedLandingPageView\x12Jcustomers/{customer}/expandedLandingPageViews/{expanded_landing_page_view}B\x89\x02\n%com.google.ads.googleads.v3.resourcesB\x1c\x45xpandedLandingPageViewProtoP\x01ZJgoogle.golang.org/genproto/googleapis/ads/googleads/v3/resources;resources\xa2\x02\x03GAA\xaa\x02!Google.Ads.GoogleAds.V3.Resources\xca\x02!Google\\Ads\\GoogleAds\\V3\\Resources\xea\x02%Google::Ads::GoogleAds::V3::Resourcesb\x06proto3')
  ,
  dependencies=[google_dot_api_dot_field__behavior__pb2.DESCRIPTOR,google_dot_api_dot_resource__pb2.DESCRIPTOR,google_dot_protobuf_dot_wrappers__pb2.DESCRIPTOR,google_dot_api_dot_annotations__pb2.DESCRIPTOR,])




_EXPANDEDLANDINGPAGEVIEW = _descriptor.Descriptor(
  name='ExpandedLandingPageView',
  full_name='google.ads.googleads.v3.resources.ExpandedLandingPageView',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_name', full_name='google.ads.googleads.v3.resources.ExpandedLandingPageView.resource_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\003\372A2\n0googleads.googleapis.com/ExpandedLandingPageView'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='expanded_final_url', full_name='google.ads.googleads.v3.resources.ExpandedLandingPageView.expanded_final_url', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\003'), file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=_b('\352A~\n0googleads.googleapis.com/ExpandedLandingPageView\022Jcustomers/{customer}/expandedLandingPageViews/{expanded_landing_page_view}'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=234,
  serialized_end=535,
)

_EXPANDEDLANDINGPAGEVIEW.fields_by_name['expanded_final_url'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
DESCRIPTOR.message_types_by_name['ExpandedLandingPageView'] = _EXPANDEDLANDINGPAGEVIEW
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ExpandedLandingPageView = _reflection.GeneratedProtocolMessageType('ExpandedLandingPageView', (_message.Message,), dict(
  DESCRIPTOR = _EXPANDEDLANDINGPAGEVIEW,
  __module__ = 'google.ads.googleads_v3.proto.resources.expanded_landing_page_view_pb2'
  ,
  __doc__ = """A landing page view with metrics aggregated at the expanded final URL
  level.
  
  
  Attributes:
      resource_name:
          Output only. The resource name of the expanded landing page
          view. Expanded landing page view resource names have the form:
          ``customers/{customer_id}/expandedLandingPageViews/{expanded_f
          inal_url_fingerprint}``
      expanded_final_url:
          Output only. The final URL that clicks are directed to.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v3.resources.ExpandedLandingPageView)
  ))
_sym_db.RegisterMessage(ExpandedLandingPageView)


DESCRIPTOR._options = None
_EXPANDEDLANDINGPAGEVIEW.fields_by_name['resource_name']._options = None
_EXPANDEDLANDINGPAGEVIEW.fields_by_name['expanded_final_url']._options = None
_EXPANDEDLANDINGPAGEVIEW._options = None
# @@protoc_insertion_point(module_scope)
