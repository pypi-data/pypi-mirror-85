# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v6/proto/resources/product_bidding_category_constant.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.ads.google_ads.v6.proto.enums import product_bidding_category_level_pb2 as google_dot_ads_dot_googleads__v6_dot_proto_dot_enums_dot_product__bidding__category__level__pb2
from google.ads.google_ads.v6.proto.enums import product_bidding_category_status_pb2 as google_dot_ads_dot_googleads__v6_dot_proto_dot_enums_dot_product__bidding__category__status__pb2
from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from google.api import resource_pb2 as google_dot_api_dot_resource__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v6/proto/resources/product_bidding_category_constant.proto',
  package='google.ads.googleads.v6.resources',
  syntax='proto3',
  serialized_options=b'\n%com.google.ads.googleads.v6.resourcesB#ProductBiddingCategoryConstantProtoP\001ZJgoogle.golang.org/genproto/googleapis/ads/googleads/v6/resources;resources\242\002\003GAA\252\002!Google.Ads.GoogleAds.V6.Resources\312\002!Google\\Ads\\GoogleAds\\V6\\Resources\352\002%Google::Ads::GoogleAds::V6::Resources',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\nOgoogle/ads/googleads_v6/proto/resources/product_bidding_category_constant.proto\x12!google.ads.googleads.v6.resources\x1aHgoogle/ads/googleads_v6/proto/enums/product_bidding_category_level.proto\x1aIgoogle/ads/googleads_v6/proto/enums/product_bidding_category_status.proto\x1a\x1fgoogle/api/field_behavior.proto\x1a\x19google/api/resource.proto\x1a\x1cgoogle/api/annotations.proto\"\xb1\x06\n\x1eProductBiddingCategoryConstant\x12V\n\rresource_name\x18\x01 \x01(\tB?\xe0\x41\x03\xfa\x41\x39\n7googleads.googleapis.com/ProductBiddingCategoryConstant\x12\x14\n\x02id\x18\n \x01(\x03\x42\x03\xe0\x41\x03H\x00\x88\x01\x01\x12\x1e\n\x0c\x63ountry_code\x18\x0b \x01(\tB\x03\xe0\x41\x03H\x01\x88\x01\x01\x12v\n(product_bidding_category_constant_parent\x18\x0c \x01(\tB?\xe0\x41\x03\xfa\x41\x39\n7googleads.googleapis.com/ProductBiddingCategoryConstantH\x02\x88\x01\x01\x12n\n\x05level\x18\x05 \x01(\x0e\x32Z.google.ads.googleads.v6.enums.ProductBiddingCategoryLevelEnum.ProductBiddingCategoryLevelB\x03\xe0\x41\x03\x12q\n\x06status\x18\x06 \x01(\x0e\x32\\.google.ads.googleads.v6.enums.ProductBiddingCategoryStatusEnum.ProductBiddingCategoryStatusB\x03\xe0\x41\x03\x12\x1f\n\rlanguage_code\x18\r \x01(\tB\x03\xe0\x41\x03H\x03\x88\x01\x01\x12 \n\x0elocalized_name\x18\x0e \x01(\tB\x03\xe0\x41\x03H\x04\x88\x01\x01:y\xea\x41v\n7googleads.googleapis.com/ProductBiddingCategoryConstant\x12;productBiddingCategoryConstants/{country_code}~{level}~{id}B\x05\n\x03_idB\x0f\n\r_country_codeB+\n)_product_bidding_category_constant_parentB\x10\n\x0e_language_codeB\x11\n\x0f_localized_nameB\x90\x02\n%com.google.ads.googleads.v6.resourcesB#ProductBiddingCategoryConstantProtoP\x01ZJgoogle.golang.org/genproto/googleapis/ads/googleads/v6/resources;resources\xa2\x02\x03GAA\xaa\x02!Google.Ads.GoogleAds.V6.Resources\xca\x02!Google\\Ads\\GoogleAds\\V6\\Resources\xea\x02%Google::Ads::GoogleAds::V6::Resourcesb\x06proto3'
  ,
  dependencies=[google_dot_ads_dot_googleads__v6_dot_proto_dot_enums_dot_product__bidding__category__level__pb2.DESCRIPTOR,google_dot_ads_dot_googleads__v6_dot_proto_dot_enums_dot_product__bidding__category__status__pb2.DESCRIPTOR,google_dot_api_dot_field__behavior__pb2.DESCRIPTOR,google_dot_api_dot_resource__pb2.DESCRIPTOR,google_dot_api_dot_annotations__pb2.DESCRIPTOR,])




_PRODUCTBIDDINGCATEGORYCONSTANT = _descriptor.Descriptor(
  name='ProductBiddingCategoryConstant',
  full_name='google.ads.googleads.v6.resources.ProductBiddingCategoryConstant',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_name', full_name='google.ads.googleads.v6.resources.ProductBiddingCategoryConstant.resource_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\340A\003\372A9\n7googleads.googleapis.com/ProductBiddingCategoryConstant', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='id', full_name='google.ads.googleads.v6.resources.ProductBiddingCategoryConstant.id', index=1,
      number=10, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\340A\003', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='country_code', full_name='google.ads.googleads.v6.resources.ProductBiddingCategoryConstant.country_code', index=2,
      number=11, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\340A\003', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='product_bidding_category_constant_parent', full_name='google.ads.googleads.v6.resources.ProductBiddingCategoryConstant.product_bidding_category_constant_parent', index=3,
      number=12, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\340A\003\372A9\n7googleads.googleapis.com/ProductBiddingCategoryConstant', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='level', full_name='google.ads.googleads.v6.resources.ProductBiddingCategoryConstant.level', index=4,
      number=5, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\340A\003', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='status', full_name='google.ads.googleads.v6.resources.ProductBiddingCategoryConstant.status', index=5,
      number=6, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\340A\003', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='language_code', full_name='google.ads.googleads.v6.resources.ProductBiddingCategoryConstant.language_code', index=6,
      number=13, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\340A\003', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='localized_name', full_name='google.ads.googleads.v6.resources.ProductBiddingCategoryConstant.localized_name', index=7,
      number=14, type=9, cpp_type=9, label=1,
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
  serialized_options=b'\352Av\n7googleads.googleapis.com/ProductBiddingCategoryConstant\022;productBiddingCategoryConstants/{country_code}~{level}~{id}',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='_id', full_name='google.ads.googleads.v6.resources.ProductBiddingCategoryConstant._id',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
    _descriptor.OneofDescriptor(
      name='_country_code', full_name='google.ads.googleads.v6.resources.ProductBiddingCategoryConstant._country_code',
      index=1, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
    _descriptor.OneofDescriptor(
      name='_product_bidding_category_constant_parent', full_name='google.ads.googleads.v6.resources.ProductBiddingCategoryConstant._product_bidding_category_constant_parent',
      index=2, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
    _descriptor.OneofDescriptor(
      name='_language_code', full_name='google.ads.googleads.v6.resources.ProductBiddingCategoryConstant._language_code',
      index=3, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
    _descriptor.OneofDescriptor(
      name='_localized_name', full_name='google.ads.googleads.v6.resources.ProductBiddingCategoryConstant._localized_name',
      index=4, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=358,
  serialized_end=1175,
)

_PRODUCTBIDDINGCATEGORYCONSTANT.fields_by_name['level'].enum_type = google_dot_ads_dot_googleads__v6_dot_proto_dot_enums_dot_product__bidding__category__level__pb2._PRODUCTBIDDINGCATEGORYLEVELENUM_PRODUCTBIDDINGCATEGORYLEVEL
_PRODUCTBIDDINGCATEGORYCONSTANT.fields_by_name['status'].enum_type = google_dot_ads_dot_googleads__v6_dot_proto_dot_enums_dot_product__bidding__category__status__pb2._PRODUCTBIDDINGCATEGORYSTATUSENUM_PRODUCTBIDDINGCATEGORYSTATUS
_PRODUCTBIDDINGCATEGORYCONSTANT.oneofs_by_name['_id'].fields.append(
  _PRODUCTBIDDINGCATEGORYCONSTANT.fields_by_name['id'])
_PRODUCTBIDDINGCATEGORYCONSTANT.fields_by_name['id'].containing_oneof = _PRODUCTBIDDINGCATEGORYCONSTANT.oneofs_by_name['_id']
_PRODUCTBIDDINGCATEGORYCONSTANT.oneofs_by_name['_country_code'].fields.append(
  _PRODUCTBIDDINGCATEGORYCONSTANT.fields_by_name['country_code'])
_PRODUCTBIDDINGCATEGORYCONSTANT.fields_by_name['country_code'].containing_oneof = _PRODUCTBIDDINGCATEGORYCONSTANT.oneofs_by_name['_country_code']
_PRODUCTBIDDINGCATEGORYCONSTANT.oneofs_by_name['_product_bidding_category_constant_parent'].fields.append(
  _PRODUCTBIDDINGCATEGORYCONSTANT.fields_by_name['product_bidding_category_constant_parent'])
_PRODUCTBIDDINGCATEGORYCONSTANT.fields_by_name['product_bidding_category_constant_parent'].containing_oneof = _PRODUCTBIDDINGCATEGORYCONSTANT.oneofs_by_name['_product_bidding_category_constant_parent']
_PRODUCTBIDDINGCATEGORYCONSTANT.oneofs_by_name['_language_code'].fields.append(
  _PRODUCTBIDDINGCATEGORYCONSTANT.fields_by_name['language_code'])
_PRODUCTBIDDINGCATEGORYCONSTANT.fields_by_name['language_code'].containing_oneof = _PRODUCTBIDDINGCATEGORYCONSTANT.oneofs_by_name['_language_code']
_PRODUCTBIDDINGCATEGORYCONSTANT.oneofs_by_name['_localized_name'].fields.append(
  _PRODUCTBIDDINGCATEGORYCONSTANT.fields_by_name['localized_name'])
_PRODUCTBIDDINGCATEGORYCONSTANT.fields_by_name['localized_name'].containing_oneof = _PRODUCTBIDDINGCATEGORYCONSTANT.oneofs_by_name['_localized_name']
DESCRIPTOR.message_types_by_name['ProductBiddingCategoryConstant'] = _PRODUCTBIDDINGCATEGORYCONSTANT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ProductBiddingCategoryConstant = _reflection.GeneratedProtocolMessageType('ProductBiddingCategoryConstant', (_message.Message,), {
  'DESCRIPTOR' : _PRODUCTBIDDINGCATEGORYCONSTANT,
  '__module__' : 'google.ads.googleads_v6.proto.resources.product_bidding_category_constant_pb2'
  ,
  '__doc__': """A Product Bidding Category.
  
  Attributes:
      resource_name:
          Output only. The resource name of the product bidding
          category. Product bidding category resource names have the
          form:  ``productBiddingCategoryConstants/{country_code}~{level
          }~{id}``
      id:
          Output only. ID of the product bidding category.  This ID is
          equivalent to the google\_product\_category ID as described in
          this article:
          https://support.google.com/merchants/answer/6324436.
      country_code:
          Output only. Two-letter upper-case country code of the product
          bidding category.
      product_bidding_category_constant_parent:
          Output only. Resource name of the parent product bidding
          category.
      level:
          Output only. Level of the product bidding category.
      status:
          Output only. Status of the product bidding category.
      language_code:
          Output only. Language code of the product bidding category.
      localized_name:
          Output only. Display value of the product bidding category
          localized according to language\_code.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v6.resources.ProductBiddingCategoryConstant)
  })
_sym_db.RegisterMessage(ProductBiddingCategoryConstant)


DESCRIPTOR._options = None
_PRODUCTBIDDINGCATEGORYCONSTANT.fields_by_name['resource_name']._options = None
_PRODUCTBIDDINGCATEGORYCONSTANT.fields_by_name['id']._options = None
_PRODUCTBIDDINGCATEGORYCONSTANT.fields_by_name['country_code']._options = None
_PRODUCTBIDDINGCATEGORYCONSTANT.fields_by_name['product_bidding_category_constant_parent']._options = None
_PRODUCTBIDDINGCATEGORYCONSTANT.fields_by_name['level']._options = None
_PRODUCTBIDDINGCATEGORYCONSTANT.fields_by_name['status']._options = None
_PRODUCTBIDDINGCATEGORYCONSTANT.fields_by_name['language_code']._options = None
_PRODUCTBIDDINGCATEGORYCONSTANT.fields_by_name['localized_name']._options = None
_PRODUCTBIDDINGCATEGORYCONSTANT._options = None
# @@protoc_insertion_point(module_scope)
