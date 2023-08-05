# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v6/proto/resources/paid_organic_search_term_view.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from google.api import resource_pb2 as google_dot_api_dot_resource__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v6/proto/resources/paid_organic_search_term_view.proto',
  package='google.ads.googleads.v6.resources',
  syntax='proto3',
  serialized_options=b'\n%com.google.ads.googleads.v6.resourcesB\036PaidOrganicSearchTermViewProtoP\001ZJgoogle.golang.org/genproto/googleapis/ads/googleads/v6/resources;resources\242\002\003GAA\252\002!Google.Ads.GoogleAds.V6.Resources\312\002!Google\\Ads\\GoogleAds\\V6\\Resources\352\002%Google::Ads::GoogleAds::V6::Resources',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\nKgoogle/ads/googleads_v6/proto/resources/paid_organic_search_term_view.proto\x12!google.ads.googleads.v6.resources\x1a\x1fgoogle/api/field_behavior.proto\x1a\x19google/api/resource.proto\x1a\x1cgoogle/api/annotations.proto\"\xbd\x02\n\x19PaidOrganicSearchTermView\x12Q\n\rresource_name\x18\x01 \x01(\tB:\xe0\x41\x03\xfa\x41\x34\n2googleads.googleapis.com/PaidOrganicSearchTermView\x12\x1d\n\x0bsearch_term\x18\x03 \x01(\tB\x03\xe0\x41\x03H\x00\x88\x01\x01:\x9d\x01\xea\x41\x99\x01\n2googleads.googleapis.com/PaidOrganicSearchTermView\x12\x63\x63ustomers/{customer_id}/paidOrganicSearchTermViews/{campaign_id}~{ad_group_id}~{base64_search_term}B\x0e\n\x0c_search_termB\x8b\x02\n%com.google.ads.googleads.v6.resourcesB\x1ePaidOrganicSearchTermViewProtoP\x01ZJgoogle.golang.org/genproto/googleapis/ads/googleads/v6/resources;resources\xa2\x02\x03GAA\xaa\x02!Google.Ads.GoogleAds.V6.Resources\xca\x02!Google\\Ads\\GoogleAds\\V6\\Resources\xea\x02%Google::Ads::GoogleAds::V6::Resourcesb\x06proto3'
  ,
  dependencies=[google_dot_api_dot_field__behavior__pb2.DESCRIPTOR,google_dot_api_dot_resource__pb2.DESCRIPTOR,google_dot_api_dot_annotations__pb2.DESCRIPTOR,])




_PAIDORGANICSEARCHTERMVIEW = _descriptor.Descriptor(
  name='PaidOrganicSearchTermView',
  full_name='google.ads.googleads.v6.resources.PaidOrganicSearchTermView',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_name', full_name='google.ads.googleads.v6.resources.PaidOrganicSearchTermView.resource_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\340A\003\372A4\n2googleads.googleapis.com/PaidOrganicSearchTermView', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='search_term', full_name='google.ads.googleads.v6.resources.PaidOrganicSearchTermView.search_term', index=1,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\340A\003', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=b'\352A\231\001\n2googleads.googleapis.com/PaidOrganicSearchTermView\022ccustomers/{customer_id}/paidOrganicSearchTermViews/{campaign_id}~{ad_group_id}~{base64_search_term}',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='_search_term', full_name='google.ads.googleads.v6.resources.PaidOrganicSearchTermView._search_term',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=205,
  serialized_end=522,
)

_PAIDORGANICSEARCHTERMVIEW.oneofs_by_name['_search_term'].fields.append(
  _PAIDORGANICSEARCHTERMVIEW.fields_by_name['search_term'])
_PAIDORGANICSEARCHTERMVIEW.fields_by_name['search_term'].containing_oneof = _PAIDORGANICSEARCHTERMVIEW.oneofs_by_name['_search_term']
DESCRIPTOR.message_types_by_name['PaidOrganicSearchTermView'] = _PAIDORGANICSEARCHTERMVIEW
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

PaidOrganicSearchTermView = _reflection.GeneratedProtocolMessageType('PaidOrganicSearchTermView', (_message.Message,), {
  'DESCRIPTOR' : _PAIDORGANICSEARCHTERMVIEW,
  '__module__' : 'google.ads.googleads_v6.proto.resources.paid_organic_search_term_view_pb2'
  ,
  '__doc__': """A paid organic search term view providing a view of search stats
  across ads and organic listings aggregated by search term at the ad
  group level.
  
  Attributes:
      resource_name:
          Output only. The resource name of the search term view. Search
          term view resource names have the form:  ``customers/{customer
          _id}/paidOrganicSearchTermViews/{campaign_id}~
          {ad_group_id}~{URL-base64 search term}``
      search_term:
          Output only. The search term.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v6.resources.PaidOrganicSearchTermView)
  })
_sym_db.RegisterMessage(PaidOrganicSearchTermView)


DESCRIPTOR._options = None
_PAIDORGANICSEARCHTERMVIEW.fields_by_name['resource_name']._options = None
_PAIDORGANICSEARCHTERMVIEW.fields_by_name['search_term']._options = None
_PAIDORGANICSEARCHTERMVIEW._options = None
# @@protoc_insertion_point(module_scope)
