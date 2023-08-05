# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v3/proto/resources/product_group_view.proto

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
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v3/proto/resources/product_group_view.proto',
  package='google.ads.googleads.v3.resources',
  syntax='proto3',
  serialized_options=_b('\n%com.google.ads.googleads.v3.resourcesB\025ProductGroupViewProtoP\001ZJgoogle.golang.org/genproto/googleapis/ads/googleads/v3/resources;resources\242\002\003GAA\252\002!Google.Ads.GoogleAds.V3.Resources\312\002!Google\\Ads\\GoogleAds\\V3\\Resources\352\002%Google::Ads::GoogleAds::V3::Resources'),
  serialized_pb=_b('\n@google/ads/googleads_v3/proto/resources/product_group_view.proto\x12!google.ads.googleads.v3.resources\x1a\x1fgoogle/api/field_behavior.proto\x1a\x19google/api/resource.proto\x1a\x1cgoogle/api/annotations.proto\"\xc9\x01\n\x10ProductGroupView\x12H\n\rresource_name\x18\x01 \x01(\tB1\xe0\x41\x03\xfa\x41+\n)googleads.googleapis.com/ProductGroupView:k\xea\x41h\n)googleads.googleapis.com/ProductGroupView\x12;customers/{customer}/productGroupViews/{product_group_view}B\x82\x02\n%com.google.ads.googleads.v3.resourcesB\x15ProductGroupViewProtoP\x01ZJgoogle.golang.org/genproto/googleapis/ads/googleads/v3/resources;resources\xa2\x02\x03GAA\xaa\x02!Google.Ads.GoogleAds.V3.Resources\xca\x02!Google\\Ads\\GoogleAds\\V3\\Resources\xea\x02%Google::Ads::GoogleAds::V3::Resourcesb\x06proto3')
  ,
  dependencies=[google_dot_api_dot_field__behavior__pb2.DESCRIPTOR,google_dot_api_dot_resource__pb2.DESCRIPTOR,google_dot_api_dot_annotations__pb2.DESCRIPTOR,])




_PRODUCTGROUPVIEW = _descriptor.Descriptor(
  name='ProductGroupView',
  full_name='google.ads.googleads.v3.resources.ProductGroupView',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_name', full_name='google.ads.googleads.v3.resources.ProductGroupView.resource_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\003\372A+\n)googleads.googleapis.com/ProductGroupView'), file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=_b('\352Ah\n)googleads.googleapis.com/ProductGroupView\022;customers/{customer}/productGroupViews/{product_group_view}'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=194,
  serialized_end=395,
)

DESCRIPTOR.message_types_by_name['ProductGroupView'] = _PRODUCTGROUPVIEW
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ProductGroupView = _reflection.GeneratedProtocolMessageType('ProductGroupView', (_message.Message,), dict(
  DESCRIPTOR = _PRODUCTGROUPVIEW,
  __module__ = 'google.ads.googleads_v3.proto.resources.product_group_view_pb2'
  ,
  __doc__ = """A product group view.
  
  
  Attributes:
      resource_name:
          Output only. The resource name of the product group view.
          Product group view resource names have the form:  ``customers/
          {customer_id}/productGroupViews/{ad_group_id}~{criterion_id}``
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v3.resources.ProductGroupView)
  ))
_sym_db.RegisterMessage(ProductGroupView)


DESCRIPTOR._options = None
_PRODUCTGROUPVIEW.fields_by_name['resource_name']._options = None
_PRODUCTGROUPVIEW._options = None
# @@protoc_insertion_point(module_scope)
