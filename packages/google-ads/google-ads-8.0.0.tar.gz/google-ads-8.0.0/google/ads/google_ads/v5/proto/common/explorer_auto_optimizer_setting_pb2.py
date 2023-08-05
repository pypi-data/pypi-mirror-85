# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v5/proto/common/explorer_auto_optimizer_setting.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v5/proto/common/explorer_auto_optimizer_setting.proto',
  package='google.ads.googleads.v5.common',
  syntax='proto3',
  serialized_options=b'\n\"com.google.ads.googleads.v5.commonB!ExplorerAutoOptimizerSettingProtoP\001ZDgoogle.golang.org/genproto/googleapis/ads/googleads/v5/common;common\242\002\003GAA\252\002\036Google.Ads.GoogleAds.V5.Common\312\002\036Google\\Ads\\GoogleAds\\V5\\Common\352\002\"Google::Ads::GoogleAds::V5::Common',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\nJgoogle/ads/googleads_v5/proto/common/explorer_auto_optimizer_setting.proto\x12\x1egoogle.ads.googleads.v5.common\x1a\x1cgoogle/api/annotations.proto\">\n\x1c\x45xplorerAutoOptimizerSetting\x12\x13\n\x06opt_in\x18\x02 \x01(\x08H\x00\x88\x01\x01\x42\t\n\x07_opt_inB\xfc\x01\n\"com.google.ads.googleads.v5.commonB!ExplorerAutoOptimizerSettingProtoP\x01ZDgoogle.golang.org/genproto/googleapis/ads/googleads/v5/common;common\xa2\x02\x03GAA\xaa\x02\x1eGoogle.Ads.GoogleAds.V5.Common\xca\x02\x1eGoogle\\Ads\\GoogleAds\\V5\\Common\xea\x02\"Google::Ads::GoogleAds::V5::Commonb\x06proto3'
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,])




_EXPLORERAUTOOPTIMIZERSETTING = _descriptor.Descriptor(
  name='ExplorerAutoOptimizerSetting',
  full_name='google.ads.googleads.v5.common.ExplorerAutoOptimizerSetting',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='opt_in', full_name='google.ads.googleads.v5.common.ExplorerAutoOptimizerSetting.opt_in', index=0,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
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
      name='_opt_in', full_name='google.ads.googleads.v5.common.ExplorerAutoOptimizerSetting._opt_in',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=140,
  serialized_end=202,
)

_EXPLORERAUTOOPTIMIZERSETTING.oneofs_by_name['_opt_in'].fields.append(
  _EXPLORERAUTOOPTIMIZERSETTING.fields_by_name['opt_in'])
_EXPLORERAUTOOPTIMIZERSETTING.fields_by_name['opt_in'].containing_oneof = _EXPLORERAUTOOPTIMIZERSETTING.oneofs_by_name['_opt_in']
DESCRIPTOR.message_types_by_name['ExplorerAutoOptimizerSetting'] = _EXPLORERAUTOOPTIMIZERSETTING
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ExplorerAutoOptimizerSetting = _reflection.GeneratedProtocolMessageType('ExplorerAutoOptimizerSetting', (_message.Message,), {
  'DESCRIPTOR' : _EXPLORERAUTOOPTIMIZERSETTING,
  '__module__' : 'google.ads.googleads_v5.proto.common.explorer_auto_optimizer_setting_pb2'
  ,
  '__doc__': """Settings for the Display Campaign Optimizer, initially named
  "Explorer". Learn more about `automatic targeting
  <https://support.google.com/google-ads/answer/190596>`__.
  
  Attributes:
      opt_in:
          Indicates whether the optimizer is turned on.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v5.common.ExplorerAutoOptimizerSetting)
  })
_sym_db.RegisterMessage(ExplorerAutoOptimizerSetting)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
