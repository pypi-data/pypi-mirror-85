# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v6/proto/resources/custom_audience.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.ads.google_ads.v6.proto.enums import custom_audience_member_type_pb2 as google_dot_ads_dot_googleads__v6_dot_proto_dot_enums_dot_custom__audience__member__type__pb2
from google.ads.google_ads.v6.proto.enums import custom_audience_status_pb2 as google_dot_ads_dot_googleads__v6_dot_proto_dot_enums_dot_custom__audience__status__pb2
from google.ads.google_ads.v6.proto.enums import custom_audience_type_pb2 as google_dot_ads_dot_googleads__v6_dot_proto_dot_enums_dot_custom__audience__type__pb2
from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from google.api import resource_pb2 as google_dot_api_dot_resource__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v6/proto/resources/custom_audience.proto',
  package='google.ads.googleads.v6.resources',
  syntax='proto3',
  serialized_options=b'\n%com.google.ads.googleads.v6.resourcesB\023CustomAudienceProtoP\001ZJgoogle.golang.org/genproto/googleapis/ads/googleads/v6/resources;resources\242\002\003GAA\252\002!Google.Ads.GoogleAds.V6.Resources\312\002!Google\\Ads\\GoogleAds\\V6\\Resources\352\002%Google::Ads::GoogleAds::V6::Resources',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n=google/ads/googleads_v6/proto/resources/custom_audience.proto\x12!google.ads.googleads.v6.resources\x1a\x45google/ads/googleads_v6/proto/enums/custom_audience_member_type.proto\x1a@google/ads/googleads_v6/proto/enums/custom_audience_status.proto\x1a>google/ads/googleads_v6/proto/enums/custom_audience_type.proto\x1a\x1fgoogle/api/field_behavior.proto\x1a\x19google/api/resource.proto\x1a\x1cgoogle/api/annotations.proto\"\xfd\x03\n\x0e\x43ustomAudience\x12\x46\n\rresource_name\x18\x01 \x01(\tB/\xe0\x41\x05\xfa\x41)\n\'googleads.googleapis.com/CustomAudience\x12\x0f\n\x02id\x18\x02 \x01(\x03\x42\x03\xe0\x41\x03\x12\x61\n\x06status\x18\x03 \x01(\x0e\x32L.google.ads.googleads.v6.enums.CustomAudienceStatusEnum.CustomAudienceStatusB\x03\xe0\x41\x03\x12\x0c\n\x04name\x18\x04 \x01(\t\x12V\n\x04type\x18\x05 \x01(\x0e\x32H.google.ads.googleads.v6.enums.CustomAudienceTypeEnum.CustomAudienceType\x12\x13\n\x0b\x64\x65scription\x18\x06 \x01(\t\x12H\n\x07members\x18\x07 \x03(\x0b\x32\x37.google.ads.googleads.v6.resources.CustomAudienceMember:j\xea\x41g\n\'googleads.googleapis.com/CustomAudience\x12<customers/{customer_id}/customAudiences/{custom_audience_id}\"\xd5\x01\n\x14\x43ustomAudienceMember\x12i\n\x0bmember_type\x18\x01 \x01(\x0e\x32T.google.ads.googleads.v6.enums.CustomAudienceMemberTypeEnum.CustomAudienceMemberType\x12\x11\n\x07keyword\x18\x02 \x01(\tH\x00\x12\r\n\x03url\x18\x03 \x01(\tH\x00\x12\x18\n\x0eplace_category\x18\x04 \x01(\x03H\x00\x12\r\n\x03\x61pp\x18\x05 \x01(\tH\x00\x42\x07\n\x05valueB\x80\x02\n%com.google.ads.googleads.v6.resourcesB\x13\x43ustomAudienceProtoP\x01ZJgoogle.golang.org/genproto/googleapis/ads/googleads/v6/resources;resources\xa2\x02\x03GAA\xaa\x02!Google.Ads.GoogleAds.V6.Resources\xca\x02!Google\\Ads\\GoogleAds\\V6\\Resources\xea\x02%Google::Ads::GoogleAds::V6::Resourcesb\x06proto3'
  ,
  dependencies=[google_dot_ads_dot_googleads__v6_dot_proto_dot_enums_dot_custom__audience__member__type__pb2.DESCRIPTOR,google_dot_ads_dot_googleads__v6_dot_proto_dot_enums_dot_custom__audience__status__pb2.DESCRIPTOR,google_dot_ads_dot_googleads__v6_dot_proto_dot_enums_dot_custom__audience__type__pb2.DESCRIPTOR,google_dot_api_dot_field__behavior__pb2.DESCRIPTOR,google_dot_api_dot_resource__pb2.DESCRIPTOR,google_dot_api_dot_annotations__pb2.DESCRIPTOR,])




_CUSTOMAUDIENCE = _descriptor.Descriptor(
  name='CustomAudience',
  full_name='google.ads.googleads.v6.resources.CustomAudience',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_name', full_name='google.ads.googleads.v6.resources.CustomAudience.resource_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\340A\005\372A)\n\'googleads.googleapis.com/CustomAudience', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='id', full_name='google.ads.googleads.v6.resources.CustomAudience.id', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\340A\003', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='status', full_name='google.ads.googleads.v6.resources.CustomAudience.status', index=2,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\340A\003', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='name', full_name='google.ads.googleads.v6.resources.CustomAudience.name', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='type', full_name='google.ads.googleads.v6.resources.CustomAudience.type', index=4,
      number=5, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='description', full_name='google.ads.googleads.v6.resources.CustomAudience.description', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='members', full_name='google.ads.googleads.v6.resources.CustomAudience.members', index=6,
      number=7, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=b'\352Ag\n\'googleads.googleapis.com/CustomAudience\022<customers/{customer_id}/customAudiences/{custom_audience_id}',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=392,
  serialized_end=901,
)


_CUSTOMAUDIENCEMEMBER = _descriptor.Descriptor(
  name='CustomAudienceMember',
  full_name='google.ads.googleads.v6.resources.CustomAudienceMember',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='member_type', full_name='google.ads.googleads.v6.resources.CustomAudienceMember.member_type', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='keyword', full_name='google.ads.googleads.v6.resources.CustomAudienceMember.keyword', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='url', full_name='google.ads.googleads.v6.resources.CustomAudienceMember.url', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='place_category', full_name='google.ads.googleads.v6.resources.CustomAudienceMember.place_category', index=3,
      number=4, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='app', full_name='google.ads.googleads.v6.resources.CustomAudienceMember.app', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
    _descriptor.OneofDescriptor(
      name='value', full_name='google.ads.googleads.v6.resources.CustomAudienceMember.value',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=904,
  serialized_end=1117,
)

_CUSTOMAUDIENCE.fields_by_name['status'].enum_type = google_dot_ads_dot_googleads__v6_dot_proto_dot_enums_dot_custom__audience__status__pb2._CUSTOMAUDIENCESTATUSENUM_CUSTOMAUDIENCESTATUS
_CUSTOMAUDIENCE.fields_by_name['type'].enum_type = google_dot_ads_dot_googleads__v6_dot_proto_dot_enums_dot_custom__audience__type__pb2._CUSTOMAUDIENCETYPEENUM_CUSTOMAUDIENCETYPE
_CUSTOMAUDIENCE.fields_by_name['members'].message_type = _CUSTOMAUDIENCEMEMBER
_CUSTOMAUDIENCEMEMBER.fields_by_name['member_type'].enum_type = google_dot_ads_dot_googleads__v6_dot_proto_dot_enums_dot_custom__audience__member__type__pb2._CUSTOMAUDIENCEMEMBERTYPEENUM_CUSTOMAUDIENCEMEMBERTYPE
_CUSTOMAUDIENCEMEMBER.oneofs_by_name['value'].fields.append(
  _CUSTOMAUDIENCEMEMBER.fields_by_name['keyword'])
_CUSTOMAUDIENCEMEMBER.fields_by_name['keyword'].containing_oneof = _CUSTOMAUDIENCEMEMBER.oneofs_by_name['value']
_CUSTOMAUDIENCEMEMBER.oneofs_by_name['value'].fields.append(
  _CUSTOMAUDIENCEMEMBER.fields_by_name['url'])
_CUSTOMAUDIENCEMEMBER.fields_by_name['url'].containing_oneof = _CUSTOMAUDIENCEMEMBER.oneofs_by_name['value']
_CUSTOMAUDIENCEMEMBER.oneofs_by_name['value'].fields.append(
  _CUSTOMAUDIENCEMEMBER.fields_by_name['place_category'])
_CUSTOMAUDIENCEMEMBER.fields_by_name['place_category'].containing_oneof = _CUSTOMAUDIENCEMEMBER.oneofs_by_name['value']
_CUSTOMAUDIENCEMEMBER.oneofs_by_name['value'].fields.append(
  _CUSTOMAUDIENCEMEMBER.fields_by_name['app'])
_CUSTOMAUDIENCEMEMBER.fields_by_name['app'].containing_oneof = _CUSTOMAUDIENCEMEMBER.oneofs_by_name['value']
DESCRIPTOR.message_types_by_name['CustomAudience'] = _CUSTOMAUDIENCE
DESCRIPTOR.message_types_by_name['CustomAudienceMember'] = _CUSTOMAUDIENCEMEMBER
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

CustomAudience = _reflection.GeneratedProtocolMessageType('CustomAudience', (_message.Message,), {
  'DESCRIPTOR' : _CUSTOMAUDIENCE,
  '__module__' : 'google.ads.googleads_v6.proto.resources.custom_audience_pb2'
  ,
  '__doc__': """A custom audience. This is a list of users by interest.
  
  Attributes:
      resource_name:
          Immutable. The resource name of the custom audience. Custom
          audience resource names have the form:  ``customers/{customer_
          id}/customAudiences/{custom_audience_id}``
      id:
          Output only. ID of the custom audience.
      status:
          Output only. Status of this custom audience. Indicates whether
          the custom audience is enabled or removed.
      name:
          Name of the custom audience. It should be unique for all
          custom audiences created by a customer. This field is required
          for creating operations.
      type:
          Type of the custom audience. ("INTEREST" OR "PURCHASE\_INTENT"
          is not allowed for newly created custom audience but kept for
          existing audiences)
      description:
          Description of this custom audience.
      members:
          List of custom audience members that this custom audience is
          composed of. Members can be added during CustomAudience
          creation. If members are presented in UPDATE operation,
          existing members will be overridden.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v6.resources.CustomAudience)
  })
_sym_db.RegisterMessage(CustomAudience)

CustomAudienceMember = _reflection.GeneratedProtocolMessageType('CustomAudienceMember', (_message.Message,), {
  'DESCRIPTOR' : _CUSTOMAUDIENCEMEMBER,
  '__module__' : 'google.ads.googleads_v6.proto.resources.custom_audience_pb2'
  ,
  '__doc__': """A member of custom audience. A member can be a KEYWORD, URL,
  PLACE\_CATEGORY or APP. It can only be created or removed but not
  changed.
  
  Attributes:
      member_type:
          The type of custom audience member, KEYWORD, URL,
          PLACE\_CATEGORY or APP.
      value:
          The CustomAudienceMember value. One field is populated
          depending on the member type.
      keyword:
          A keyword or keyword phrase — at most 10 words and 80
          characters. Languages with double-width characters such as
          Chinese, Japanese, or Korean, are allowed 40 characters, which
          describes the user's interests or actions.
      url:
          An HTTP URL, protocol-included — at most 2048 characters,
          which includes contents users have interests in.
      place_category:
          A place type described by a place category users visit.
      app:
          A package name of Android apps which users installed such as
          com.google.example.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v6.resources.CustomAudienceMember)
  })
_sym_db.RegisterMessage(CustomAudienceMember)


DESCRIPTOR._options = None
_CUSTOMAUDIENCE.fields_by_name['resource_name']._options = None
_CUSTOMAUDIENCE.fields_by_name['id']._options = None
_CUSTOMAUDIENCE.fields_by_name['status']._options = None
_CUSTOMAUDIENCE._options = None
# @@protoc_insertion_point(module_scope)
