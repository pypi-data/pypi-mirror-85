# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v3/proto/resources/customer_feed.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.ads.google_ads.v3.proto.common import matching_function_pb2 as google_dot_ads_dot_googleads__v3_dot_proto_dot_common_dot_matching__function__pb2
from google.ads.google_ads.v3.proto.enums import feed_link_status_pb2 as google_dot_ads_dot_googleads__v3_dot_proto_dot_enums_dot_feed__link__status__pb2
from google.ads.google_ads.v3.proto.enums import placeholder_type_pb2 as google_dot_ads_dot_googleads__v3_dot_proto_dot_enums_dot_placeholder__type__pb2
from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from google.api import resource_pb2 as google_dot_api_dot_resource__pb2
from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v3/proto/resources/customer_feed.proto',
  package='google.ads.googleads.v3.resources',
  syntax='proto3',
  serialized_options=_b('\n%com.google.ads.googleads.v3.resourcesB\021CustomerFeedProtoP\001ZJgoogle.golang.org/genproto/googleapis/ads/googleads/v3/resources;resources\242\002\003GAA\252\002!Google.Ads.GoogleAds.V3.Resources\312\002!Google\\Ads\\GoogleAds\\V3\\Resources\352\002%Google::Ads::GoogleAds::V3::Resources'),
  serialized_pb=_b('\n;google/ads/googleads_v3/proto/resources/customer_feed.proto\x12!google.ads.googleads.v3.resources\x1a<google/ads/googleads_v3/proto/common/matching_function.proto\x1a:google/ads/googleads_v3/proto/enums/feed_link_status.proto\x1a:google/ads/googleads_v3/proto/enums/placeholder_type.proto\x1a\x1fgoogle/api/field_behavior.proto\x1a\x19google/api/resource.proto\x1a\x1egoogle/protobuf/wrappers.proto\x1a\x1cgoogle/api/annotations.proto\"\x8a\x04\n\x0c\x43ustomerFeed\x12\x44\n\rresource_name\x18\x01 \x01(\tB-\xe0\x41\x05\xfa\x41\'\n%googleads.googleapis.com/CustomerFeed\x12Q\n\x04\x66\x65\x65\x64\x18\x02 \x01(\x0b\x32\x1c.google.protobuf.StringValueB%\xe0\x41\x05\xfa\x41\x1f\n\x1dgoogleads.googleapis.com/Feed\x12]\n\x11placeholder_types\x18\x03 \x03(\x0e\x32\x42.google.ads.googleads.v3.enums.PlaceholderTypeEnum.PlaceholderType\x12K\n\x11matching_function\x18\x04 \x01(\x0b\x32\x30.google.ads.googleads.v3.common.MatchingFunction\x12U\n\x06status\x18\x05 \x01(\x0e\x32@.google.ads.googleads.v3.enums.FeedLinkStatusEnum.FeedLinkStatusB\x03\xe0\x41\x03:^\xea\x41[\n%googleads.googleapis.com/CustomerFeed\x12\x32\x63ustomers/{customer}/customerFeeds/{customer_feed}B\xfe\x01\n%com.google.ads.googleads.v3.resourcesB\x11\x43ustomerFeedProtoP\x01ZJgoogle.golang.org/genproto/googleapis/ads/googleads/v3/resources;resources\xa2\x02\x03GAA\xaa\x02!Google.Ads.GoogleAds.V3.Resources\xca\x02!Google\\Ads\\GoogleAds\\V3\\Resources\xea\x02%Google::Ads::GoogleAds::V3::Resourcesb\x06proto3')
  ,
  dependencies=[google_dot_ads_dot_googleads__v3_dot_proto_dot_common_dot_matching__function__pb2.DESCRIPTOR,google_dot_ads_dot_googleads__v3_dot_proto_dot_enums_dot_feed__link__status__pb2.DESCRIPTOR,google_dot_ads_dot_googleads__v3_dot_proto_dot_enums_dot_placeholder__type__pb2.DESCRIPTOR,google_dot_api_dot_field__behavior__pb2.DESCRIPTOR,google_dot_api_dot_resource__pb2.DESCRIPTOR,google_dot_protobuf_dot_wrappers__pb2.DESCRIPTOR,google_dot_api_dot_annotations__pb2.DESCRIPTOR,])




_CUSTOMERFEED = _descriptor.Descriptor(
  name='CustomerFeed',
  full_name='google.ads.googleads.v3.resources.CustomerFeed',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_name', full_name='google.ads.googleads.v3.resources.CustomerFeed.resource_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\005\372A\'\n%googleads.googleapis.com/CustomerFeed'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='feed', full_name='google.ads.googleads.v3.resources.CustomerFeed.feed', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\005\372A\037\n\035googleads.googleapis.com/Feed'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='placeholder_types', full_name='google.ads.googleads.v3.resources.CustomerFeed.placeholder_types', index=2,
      number=3, type=14, cpp_type=8, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='matching_function', full_name='google.ads.googleads.v3.resources.CustomerFeed.matching_function', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='status', full_name='google.ads.googleads.v3.resources.CustomerFeed.status', index=4,
      number=5, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\003'), file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=_b('\352A[\n%googleads.googleapis.com/CustomerFeed\0222customers/{customer}/customerFeeds/{customer_feed}'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=403,
  serialized_end=925,
)

_CUSTOMERFEED.fields_by_name['feed'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_CUSTOMERFEED.fields_by_name['placeholder_types'].enum_type = google_dot_ads_dot_googleads__v3_dot_proto_dot_enums_dot_placeholder__type__pb2._PLACEHOLDERTYPEENUM_PLACEHOLDERTYPE
_CUSTOMERFEED.fields_by_name['matching_function'].message_type = google_dot_ads_dot_googleads__v3_dot_proto_dot_common_dot_matching__function__pb2._MATCHINGFUNCTION
_CUSTOMERFEED.fields_by_name['status'].enum_type = google_dot_ads_dot_googleads__v3_dot_proto_dot_enums_dot_feed__link__status__pb2._FEEDLINKSTATUSENUM_FEEDLINKSTATUS
DESCRIPTOR.message_types_by_name['CustomerFeed'] = _CUSTOMERFEED
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

CustomerFeed = _reflection.GeneratedProtocolMessageType('CustomerFeed', (_message.Message,), dict(
  DESCRIPTOR = _CUSTOMERFEED,
  __module__ = 'google.ads.googleads_v3.proto.resources.customer_feed_pb2'
  ,
  __doc__ = """A customer feed.
  
  
  Attributes:
      resource_name:
          Immutable. The resource name of the customer feed. Customer
          feed resource names have the form:
          ``customers/{customer_id}/customerFeeds/{feed_id}``
      feed:
          Immutable. The feed being linked to the customer.
      placeholder_types:
          Indicates which placeholder types the feed may populate under
          the connected customer. Required.
      matching_function:
          Matching function associated with the CustomerFeed. The
          matching function is used to filter the set of feed items
          selected. Required.
      status:
          Output only. Status of the customer feed. This field is read-
          only.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v3.resources.CustomerFeed)
  ))
_sym_db.RegisterMessage(CustomerFeed)


DESCRIPTOR._options = None
_CUSTOMERFEED.fields_by_name['resource_name']._options = None
_CUSTOMERFEED.fields_by_name['feed']._options = None
_CUSTOMERFEED.fields_by_name['status']._options = None
_CUSTOMERFEED._options = None
# @@protoc_insertion_point(module_scope)
