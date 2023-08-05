# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v6/proto/resources/video.proto

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
  name='google/ads/googleads_v6/proto/resources/video.proto',
  package='google.ads.googleads.v6.resources',
  syntax='proto3',
  serialized_options=b'\n%com.google.ads.googleads.v6.resourcesB\nVideoProtoP\001ZJgoogle.golang.org/genproto/googleapis/ads/googleads/v6/resources;resources\242\002\003GAA\252\002!Google.Ads.GoogleAds.V6.Resources\312\002!Google\\Ads\\GoogleAds\\V6\\Resources\352\002%Google::Ads::GoogleAds::V6::Resources',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n3google/ads/googleads_v6/proto/resources/video.proto\x12!google.ads.googleads.v6.resources\x1a\x1fgoogle/api/field_behavior.proto\x1a\x19google/api/resource.proto\x1a\x1cgoogle/api/annotations.proto\"\xba\x02\n\x05Video\x12=\n\rresource_name\x18\x01 \x01(\tB&\xe0\x41\x03\xfa\x41 \n\x1egoogleads.googleapis.com/Video\x12\x14\n\x02id\x18\x06 \x01(\tB\x03\xe0\x41\x03H\x00\x88\x01\x01\x12\x1c\n\nchannel_id\x18\x07 \x01(\tB\x03\xe0\x41\x03H\x01\x88\x01\x01\x12!\n\x0f\x64uration_millis\x18\x08 \x01(\x03\x42\x03\xe0\x41\x03H\x02\x88\x01\x01\x12\x17\n\x05title\x18\t \x01(\tB\x03\xe0\x41\x03H\x03\x88\x01\x01:N\xea\x41K\n\x1egoogleads.googleapis.com/Video\x12)customers/{customer_id}/videos/{video_id}B\x05\n\x03_idB\r\n\x0b_channel_idB\x12\n\x10_duration_millisB\x08\n\x06_titleB\xf7\x01\n%com.google.ads.googleads.v6.resourcesB\nVideoProtoP\x01ZJgoogle.golang.org/genproto/googleapis/ads/googleads/v6/resources;resources\xa2\x02\x03GAA\xaa\x02!Google.Ads.GoogleAds.V6.Resources\xca\x02!Google\\Ads\\GoogleAds\\V6\\Resources\xea\x02%Google::Ads::GoogleAds::V6::Resourcesb\x06proto3'
  ,
  dependencies=[google_dot_api_dot_field__behavior__pb2.DESCRIPTOR,google_dot_api_dot_resource__pb2.DESCRIPTOR,google_dot_api_dot_annotations__pb2.DESCRIPTOR,])




_VIDEO = _descriptor.Descriptor(
  name='Video',
  full_name='google.ads.googleads.v6.resources.Video',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_name', full_name='google.ads.googleads.v6.resources.Video.resource_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\340A\003\372A \n\036googleads.googleapis.com/Video', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='id', full_name='google.ads.googleads.v6.resources.Video.id', index=1,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\340A\003', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='channel_id', full_name='google.ads.googleads.v6.resources.Video.channel_id', index=2,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\340A\003', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='duration_millis', full_name='google.ads.googleads.v6.resources.Video.duration_millis', index=3,
      number=8, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\340A\003', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='title', full_name='google.ads.googleads.v6.resources.Video.title', index=4,
      number=9, type=9, cpp_type=9, label=1,
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
  serialized_options=b'\352AK\n\036googleads.googleapis.com/Video\022)customers/{customer_id}/videos/{video_id}',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='_id', full_name='google.ads.googleads.v6.resources.Video._id',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
    _descriptor.OneofDescriptor(
      name='_channel_id', full_name='google.ads.googleads.v6.resources.Video._channel_id',
      index=1, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
    _descriptor.OneofDescriptor(
      name='_duration_millis', full_name='google.ads.googleads.v6.resources.Video._duration_millis',
      index=2, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
    _descriptor.OneofDescriptor(
      name='_title', full_name='google.ads.googleads.v6.resources.Video._title',
      index=3, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=181,
  serialized_end=495,
)

_VIDEO.oneofs_by_name['_id'].fields.append(
  _VIDEO.fields_by_name['id'])
_VIDEO.fields_by_name['id'].containing_oneof = _VIDEO.oneofs_by_name['_id']
_VIDEO.oneofs_by_name['_channel_id'].fields.append(
  _VIDEO.fields_by_name['channel_id'])
_VIDEO.fields_by_name['channel_id'].containing_oneof = _VIDEO.oneofs_by_name['_channel_id']
_VIDEO.oneofs_by_name['_duration_millis'].fields.append(
  _VIDEO.fields_by_name['duration_millis'])
_VIDEO.fields_by_name['duration_millis'].containing_oneof = _VIDEO.oneofs_by_name['_duration_millis']
_VIDEO.oneofs_by_name['_title'].fields.append(
  _VIDEO.fields_by_name['title'])
_VIDEO.fields_by_name['title'].containing_oneof = _VIDEO.oneofs_by_name['_title']
DESCRIPTOR.message_types_by_name['Video'] = _VIDEO
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Video = _reflection.GeneratedProtocolMessageType('Video', (_message.Message,), {
  'DESCRIPTOR' : _VIDEO,
  '__module__' : 'google.ads.googleads_v6.proto.resources.video_pb2'
  ,
  '__doc__': """A video.
  
  Attributes:
      resource_name:
          Output only. The resource name of the video. Video resource
          names have the form:
          ``customers/{customer_id}/videos/{video_id}``
      id:
          Output only. The ID of the video.
      channel_id:
          Output only. The owner channel id of the video.
      duration_millis:
          Output only. The duration of the video in milliseconds.
      title:
          Output only. The title of the video.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v6.resources.Video)
  })
_sym_db.RegisterMessage(Video)


DESCRIPTOR._options = None
_VIDEO.fields_by_name['resource_name']._options = None
_VIDEO.fields_by_name['id']._options = None
_VIDEO.fields_by_name['channel_id']._options = None
_VIDEO.fields_by_name['duration_millis']._options = None
_VIDEO.fields_by_name['title']._options = None
_VIDEO._options = None
# @@protoc_insertion_point(module_scope)
