# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v4/proto/resources/google_ads_field.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.ads.google_ads.v4.proto.enums import google_ads_field_category_pb2 as google_dot_ads_dot_googleads__v4_dot_proto_dot_enums_dot_google__ads__field__category__pb2
from google.ads.google_ads.v4.proto.enums import google_ads_field_data_type_pb2 as google_dot_ads_dot_googleads__v4_dot_proto_dot_enums_dot_google__ads__field__data__type__pb2
from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from google.api import resource_pb2 as google_dot_api_dot_resource__pb2
from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v4/proto/resources/google_ads_field.proto',
  package='google.ads.googleads.v4.resources',
  syntax='proto3',
  serialized_options=_b('\n%com.google.ads.googleads.v4.resourcesB\023GoogleAdsFieldProtoP\001ZJgoogle.golang.org/genproto/googleapis/ads/googleads/v4/resources;resources\242\002\003GAA\252\002!Google.Ads.GoogleAds.V4.Resources\312\002!Google\\Ads\\GoogleAds\\V4\\Resources\352\002%Google::Ads::GoogleAds::V4::Resources'),
  serialized_pb=_b('\n>google/ads/googleads_v4/proto/resources/google_ads_field.proto\x12!google.ads.googleads.v4.resources\x1a\x43google/ads/googleads_v4/proto/enums/google_ads_field_category.proto\x1a\x44google/ads/googleads_v4/proto/enums/google_ads_field_data_type.proto\x1a\x1fgoogle/api/field_behavior.proto\x1a\x19google/api/resource.proto\x1a\x1egoogle/protobuf/wrappers.proto\x1a\x1cgoogle/api/annotations.proto\"\xd3\x07\n\x0eGoogleAdsField\x12\x46\n\rresource_name\x18\x01 \x01(\tB/\xe0\x41\x03\xfa\x41)\n\'googleads.googleapis.com/GoogleAdsField\x12/\n\x04name\x18\x02 \x01(\x0b\x32\x1c.google.protobuf.StringValueB\x03\xe0\x41\x03\x12g\n\x08\x63\x61tegory\x18\x03 \x01(\x0e\x32P.google.ads.googleads.v4.enums.GoogleAdsFieldCategoryEnum.GoogleAdsFieldCategoryB\x03\xe0\x41\x03\x12\x33\n\nselectable\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.BoolValueB\x03\xe0\x41\x03\x12\x33\n\nfilterable\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.BoolValueB\x03\xe0\x41\x03\x12\x31\n\x08sortable\x18\x06 \x01(\x0b\x32\x1a.google.protobuf.BoolValueB\x03\xe0\x41\x03\x12:\n\x0fselectable_with\x18\x07 \x03(\x0b\x32\x1c.google.protobuf.StringValueB\x03\xe0\x41\x03\x12>\n\x13\x61ttribute_resources\x18\x08 \x03(\x0b\x32\x1c.google.protobuf.StringValueB\x03\xe0\x41\x03\x12\x32\n\x07metrics\x18\t \x03(\x0b\x32\x1c.google.protobuf.StringValueB\x03\xe0\x41\x03\x12\x33\n\x08segments\x18\n \x03(\x0b\x32\x1c.google.protobuf.StringValueB\x03\xe0\x41\x03\x12\x36\n\x0b\x65num_values\x18\x0b \x03(\x0b\x32\x1c.google.protobuf.StringValueB\x03\xe0\x41\x03\x12h\n\tdata_type\x18\x0c \x01(\x0e\x32P.google.ads.googleads.v4.enums.GoogleAdsFieldDataTypeEnum.GoogleAdsFieldDataTypeB\x03\xe0\x41\x03\x12\x33\n\x08type_url\x18\r \x01(\x0b\x32\x1c.google.protobuf.StringValueB\x03\xe0\x41\x03\x12\x34\n\x0bis_repeated\x18\x0e \x01(\x0b\x32\x1a.google.protobuf.BoolValueB\x03\xe0\x41\x03:P\xea\x41M\n\'googleads.googleapis.com/GoogleAdsField\x12\"googleAdsFields/{google_ads_field}B\x80\x02\n%com.google.ads.googleads.v4.resourcesB\x13GoogleAdsFieldProtoP\x01ZJgoogle.golang.org/genproto/googleapis/ads/googleads/v4/resources;resources\xa2\x02\x03GAA\xaa\x02!Google.Ads.GoogleAds.V4.Resources\xca\x02!Google\\Ads\\GoogleAds\\V4\\Resources\xea\x02%Google::Ads::GoogleAds::V4::Resourcesb\x06proto3')
  ,
  dependencies=[google_dot_ads_dot_googleads__v4_dot_proto_dot_enums_dot_google__ads__field__category__pb2.DESCRIPTOR,google_dot_ads_dot_googleads__v4_dot_proto_dot_enums_dot_google__ads__field__data__type__pb2.DESCRIPTOR,google_dot_api_dot_field__behavior__pb2.DESCRIPTOR,google_dot_api_dot_resource__pb2.DESCRIPTOR,google_dot_protobuf_dot_wrappers__pb2.DESCRIPTOR,google_dot_api_dot_annotations__pb2.DESCRIPTOR,])




_GOOGLEADSFIELD = _descriptor.Descriptor(
  name='GoogleAdsField',
  full_name='google.ads.googleads.v4.resources.GoogleAdsField',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_name', full_name='google.ads.googleads.v4.resources.GoogleAdsField.resource_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\003\372A)\n\'googleads.googleapis.com/GoogleAdsField'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='google.ads.googleads.v4.resources.GoogleAdsField.name', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\003'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='category', full_name='google.ads.googleads.v4.resources.GoogleAdsField.category', index=2,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\003'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='selectable', full_name='google.ads.googleads.v4.resources.GoogleAdsField.selectable', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\003'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='filterable', full_name='google.ads.googleads.v4.resources.GoogleAdsField.filterable', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\003'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sortable', full_name='google.ads.googleads.v4.resources.GoogleAdsField.sortable', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\003'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='selectable_with', full_name='google.ads.googleads.v4.resources.GoogleAdsField.selectable_with', index=6,
      number=7, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\003'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='attribute_resources', full_name='google.ads.googleads.v4.resources.GoogleAdsField.attribute_resources', index=7,
      number=8, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\003'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='metrics', full_name='google.ads.googleads.v4.resources.GoogleAdsField.metrics', index=8,
      number=9, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\003'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='segments', full_name='google.ads.googleads.v4.resources.GoogleAdsField.segments', index=9,
      number=10, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\003'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='enum_values', full_name='google.ads.googleads.v4.resources.GoogleAdsField.enum_values', index=10,
      number=11, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\003'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='data_type', full_name='google.ads.googleads.v4.resources.GoogleAdsField.data_type', index=11,
      number=12, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\003'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='type_url', full_name='google.ads.googleads.v4.resources.GoogleAdsField.type_url', index=12,
      number=13, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\003'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='is_repeated', full_name='google.ads.googleads.v4.resources.GoogleAdsField.is_repeated', index=13,
      number=14, type=11, cpp_type=10, label=1,
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
  serialized_options=_b('\352AM\n\'googleads.googleapis.com/GoogleAdsField\022\"googleAdsFields/{google_ads_field}'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=363,
  serialized_end=1342,
)

_GOOGLEADSFIELD.fields_by_name['name'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_GOOGLEADSFIELD.fields_by_name['category'].enum_type = google_dot_ads_dot_googleads__v4_dot_proto_dot_enums_dot_google__ads__field__category__pb2._GOOGLEADSFIELDCATEGORYENUM_GOOGLEADSFIELDCATEGORY
_GOOGLEADSFIELD.fields_by_name['selectable'].message_type = google_dot_protobuf_dot_wrappers__pb2._BOOLVALUE
_GOOGLEADSFIELD.fields_by_name['filterable'].message_type = google_dot_protobuf_dot_wrappers__pb2._BOOLVALUE
_GOOGLEADSFIELD.fields_by_name['sortable'].message_type = google_dot_protobuf_dot_wrappers__pb2._BOOLVALUE
_GOOGLEADSFIELD.fields_by_name['selectable_with'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_GOOGLEADSFIELD.fields_by_name['attribute_resources'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_GOOGLEADSFIELD.fields_by_name['metrics'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_GOOGLEADSFIELD.fields_by_name['segments'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_GOOGLEADSFIELD.fields_by_name['enum_values'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_GOOGLEADSFIELD.fields_by_name['data_type'].enum_type = google_dot_ads_dot_googleads__v4_dot_proto_dot_enums_dot_google__ads__field__data__type__pb2._GOOGLEADSFIELDDATATYPEENUM_GOOGLEADSFIELDDATATYPE
_GOOGLEADSFIELD.fields_by_name['type_url'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_GOOGLEADSFIELD.fields_by_name['is_repeated'].message_type = google_dot_protobuf_dot_wrappers__pb2._BOOLVALUE
DESCRIPTOR.message_types_by_name['GoogleAdsField'] = _GOOGLEADSFIELD
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GoogleAdsField = _reflection.GeneratedProtocolMessageType('GoogleAdsField', (_message.Message,), dict(
  DESCRIPTOR = _GOOGLEADSFIELD,
  __module__ = 'google.ads.googleads_v4.proto.resources.google_ads_field_pb2'
  ,
  __doc__ = """A field or resource (artifact) used by GoogleAdsService.
  
  
  Attributes:
      resource_name:
          Output only. The resource name of the artifact. Artifact
          resource names have the form:  ``googleAdsFields/{name}``
      name:
          Output only. The name of the artifact.
      category:
          Output only. The category of the artifact.
      selectable:
          Output only. Whether the artifact can be used in a SELECT
          clause in search queries.
      filterable:
          Output only. Whether the artifact can be used in a WHERE
          clause in search queries.
      sortable:
          Output only. Whether the artifact can be used in a ORDER BY
          clause in search queries.
      selectable_with:
          Output only. The names of all resources, segments, and metrics
          that are selectable with the described artifact.
      attribute_resources:
          Output only. The names of all resources that are selectable
          with the described artifact. Fields from these resources do
          not segment metrics when included in search queries.  This
          field is only set for artifacts whose category is RESOURCE.
      metrics:
          Output only. At and beyond version V1 this field lists the
          names of all metrics that are selectable with the described
          artifact when it is used in the FROM clause. It is only set
          for artifacts whose category is RESOURCE.  Before version V1
          this field lists the names of all metrics that are selectable
          with the described artifact. It is only set for artifacts
          whose category is either RESOURCE or SEGMENT
      segments:
          Output only. At and beyond version V1 this field lists the
          names of all artifacts, whether a segment or another resource,
          that segment metrics when included in search queries and when
          the described artifact is used in the FROM clause. It is only
          set for artifacts whose category is RESOURCE.  Before version
          V1 this field lists the names of all artifacts, whether a
          segment or another resource, that segment metrics when
          included in search queries. It is only set for artifacts of
          category RESOURCE, SEGMENT or METRIC.
      enum_values:
          Output only. Values the artifact can assume if it is a field
          of type ENUM.  This field is only set for artifacts of
          category SEGMENT or ATTRIBUTE.
      data_type:
          Output only. This field determines the operators that can be
          used with the artifact in WHERE clauses.
      type_url:
          Output only. The URL of proto describing the artifact's data
          type.
      is_repeated:
          Output only. Whether the field artifact is repeated.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v4.resources.GoogleAdsField)
  ))
_sym_db.RegisterMessage(GoogleAdsField)


DESCRIPTOR._options = None
_GOOGLEADSFIELD.fields_by_name['resource_name']._options = None
_GOOGLEADSFIELD.fields_by_name['name']._options = None
_GOOGLEADSFIELD.fields_by_name['category']._options = None
_GOOGLEADSFIELD.fields_by_name['selectable']._options = None
_GOOGLEADSFIELD.fields_by_name['filterable']._options = None
_GOOGLEADSFIELD.fields_by_name['sortable']._options = None
_GOOGLEADSFIELD.fields_by_name['selectable_with']._options = None
_GOOGLEADSFIELD.fields_by_name['attribute_resources']._options = None
_GOOGLEADSFIELD.fields_by_name['metrics']._options = None
_GOOGLEADSFIELD.fields_by_name['segments']._options = None
_GOOGLEADSFIELD.fields_by_name['enum_values']._options = None
_GOOGLEADSFIELD.fields_by_name['data_type']._options = None
_GOOGLEADSFIELD.fields_by_name['type_url']._options = None
_GOOGLEADSFIELD.fields_by_name['is_repeated']._options = None
_GOOGLEADSFIELD._options = None
# @@protoc_insertion_point(module_scope)
