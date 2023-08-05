# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v4/proto/services/feed_placeholder_view_service.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.ads.google_ads.v4.proto.resources import feed_placeholder_view_pb2 as google_dot_ads_dot_googleads__v4_dot_proto_dot_resources_dot_feed__placeholder__view__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.api import client_pb2 as google_dot_api_dot_client__pb2
from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from google.api import resource_pb2 as google_dot_api_dot_resource__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v4/proto/services/feed_placeholder_view_service.proto',
  package='google.ads.googleads.v4.services',
  syntax='proto3',
  serialized_options=_b('\n$com.google.ads.googleads.v4.servicesB\037FeedPlaceholderViewServiceProtoP\001ZHgoogle.golang.org/genproto/googleapis/ads/googleads/v4/services;services\242\002\003GAA\252\002 Google.Ads.GoogleAds.V4.Services\312\002 Google\\Ads\\GoogleAds\\V4\\Services\352\002$Google::Ads::GoogleAds::V4::Services'),
  serialized_pb=_b('\nJgoogle/ads/googleads_v4/proto/services/feed_placeholder_view_service.proto\x12 google.ads.googleads.v4.services\x1a\x43google/ads/googleads_v4/proto/resources/feed_placeholder_view.proto\x1a\x1cgoogle/api/annotations.proto\x1a\x17google/api/client.proto\x1a\x1fgoogle/api/field_behavior.proto\x1a\x19google/api/resource.proto\"l\n\x1dGetFeedPlaceholderViewRequest\x12K\n\rresource_name\x18\x01 \x01(\tB4\xe0\x41\x02\xfa\x41.\n,googleads.googleapis.com/FeedPlaceholderView2\x9d\x02\n\x1a\x46\x65\x65\x64PlaceholderViewService\x12\xe1\x01\n\x16GetFeedPlaceholderView\x12?.google.ads.googleads.v4.services.GetFeedPlaceholderViewRequest\x1a\x36.google.ads.googleads.v4.resources.FeedPlaceholderView\"N\x82\xd3\xe4\x93\x02\x38\x12\x36/v4/{resource_name=customers/*/feedPlaceholderViews/*}\xda\x41\rresource_name\x1a\x1b\xca\x41\x18googleads.googleapis.comB\x86\x02\n$com.google.ads.googleads.v4.servicesB\x1f\x46\x65\x65\x64PlaceholderViewServiceProtoP\x01ZHgoogle.golang.org/genproto/googleapis/ads/googleads/v4/services;services\xa2\x02\x03GAA\xaa\x02 Google.Ads.GoogleAds.V4.Services\xca\x02 Google\\Ads\\GoogleAds\\V4\\Services\xea\x02$Google::Ads::GoogleAds::V4::Servicesb\x06proto3')
  ,
  dependencies=[google_dot_ads_dot_googleads__v4_dot_proto_dot_resources_dot_feed__placeholder__view__pb2.DESCRIPTOR,google_dot_api_dot_annotations__pb2.DESCRIPTOR,google_dot_api_dot_client__pb2.DESCRIPTOR,google_dot_api_dot_field__behavior__pb2.DESCRIPTOR,google_dot_api_dot_resource__pb2.DESCRIPTOR,])




_GETFEEDPLACEHOLDERVIEWREQUEST = _descriptor.Descriptor(
  name='GetFeedPlaceholderViewRequest',
  full_name='google.ads.googleads.v4.services.GetFeedPlaceholderViewRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_name', full_name='google.ads.googleads.v4.services.GetFeedPlaceholderViewRequest.resource_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\002\372A.\n,googleads.googleapis.com/FeedPlaceholderView'), file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=296,
  serialized_end=404,
)

DESCRIPTOR.message_types_by_name['GetFeedPlaceholderViewRequest'] = _GETFEEDPLACEHOLDERVIEWREQUEST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GetFeedPlaceholderViewRequest = _reflection.GeneratedProtocolMessageType('GetFeedPlaceholderViewRequest', (_message.Message,), dict(
  DESCRIPTOR = _GETFEEDPLACEHOLDERVIEWREQUEST,
  __module__ = 'google.ads.googleads_v4.proto.services.feed_placeholder_view_service_pb2'
  ,
  __doc__ = """Request message for
  [FeedPlaceholderViewService.GetFeedPlaceholderView][google.ads.googleads.v4.services.FeedPlaceholderViewService.GetFeedPlaceholderView].
  
  
  Attributes:
      resource_name:
          Required. The resource name of the feed placeholder view to
          fetch.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v4.services.GetFeedPlaceholderViewRequest)
  ))
_sym_db.RegisterMessage(GetFeedPlaceholderViewRequest)


DESCRIPTOR._options = None
_GETFEEDPLACEHOLDERVIEWREQUEST.fields_by_name['resource_name']._options = None

_FEEDPLACEHOLDERVIEWSERVICE = _descriptor.ServiceDescriptor(
  name='FeedPlaceholderViewService',
  full_name='google.ads.googleads.v4.services.FeedPlaceholderViewService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=_b('\312A\030googleads.googleapis.com'),
  serialized_start=407,
  serialized_end=692,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetFeedPlaceholderView',
    full_name='google.ads.googleads.v4.services.FeedPlaceholderViewService.GetFeedPlaceholderView',
    index=0,
    containing_service=None,
    input_type=_GETFEEDPLACEHOLDERVIEWREQUEST,
    output_type=google_dot_ads_dot_googleads__v4_dot_proto_dot_resources_dot_feed__placeholder__view__pb2._FEEDPLACEHOLDERVIEW,
    serialized_options=_b('\202\323\344\223\0028\0226/v4/{resource_name=customers/*/feedPlaceholderViews/*}\332A\rresource_name'),
  ),
])
_sym_db.RegisterServiceDescriptor(_FEEDPLACEHOLDERVIEWSERVICE)

DESCRIPTOR.services_by_name['FeedPlaceholderViewService'] = _FEEDPLACEHOLDERVIEWSERVICE

# @@protoc_insertion_point(module_scope)
