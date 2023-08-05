# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v3/proto/resources/change_status.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.ads.google_ads.v3.proto.enums import change_status_operation_pb2 as google_dot_ads_dot_googleads__v3_dot_proto_dot_enums_dot_change__status__operation__pb2
from google.ads.google_ads.v3.proto.enums import change_status_resource_type_pb2 as google_dot_ads_dot_googleads__v3_dot_proto_dot_enums_dot_change__status__resource__type__pb2
from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from google.api import resource_pb2 as google_dot_api_dot_resource__pb2
from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v3/proto/resources/change_status.proto',
  package='google.ads.googleads.v3.resources',
  syntax='proto3',
  serialized_options=_b('\n%com.google.ads.googleads.v3.resourcesB\021ChangeStatusProtoP\001ZJgoogle.golang.org/genproto/googleapis/ads/googleads/v3/resources;resources\242\002\003GAA\252\002!Google.Ads.GoogleAds.V3.Resources\312\002!Google\\Ads\\GoogleAds\\V3\\Resources\352\002%Google::Ads::GoogleAds::V3::Resources'),
  serialized_pb=_b('\n;google/ads/googleads_v3/proto/resources/change_status.proto\x12!google.ads.googleads.v3.resources\x1a\x41google/ads/googleads_v3/proto/enums/change_status_operation.proto\x1a\x45google/ads/googleads_v3/proto/enums/change_status_resource_type.proto\x1a\x1fgoogle/api/field_behavior.proto\x1a\x19google/api/resource.proto\x1a\x1egoogle/protobuf/wrappers.proto\x1a\x1cgoogle/api/annotations.proto\"\xac\x0b\n\x0c\x43hangeStatus\x12\x44\n\rresource_name\x18\x01 \x01(\tB-\xe0\x41\x03\xfa\x41\'\n%googleads.googleapis.com/ChangeStatus\x12@\n\x15last_change_date_time\x18\x03 \x01(\x0b\x32\x1c.google.protobuf.StringValueB\x03\xe0\x41\x03\x12p\n\rresource_type\x18\x04 \x01(\x0e\x32T.google.ads.googleads.v3.enums.ChangeStatusResourceTypeEnum.ChangeStatusResourceTypeB\x03\xe0\x41\x03\x12Y\n\x08\x63\x61mpaign\x18\x05 \x01(\x0b\x32\x1c.google.protobuf.StringValueB)\xe0\x41\x03\xfa\x41#\n!googleads.googleapis.com/Campaign\x12X\n\x08\x61\x64_group\x18\x06 \x01(\x0b\x32\x1c.google.protobuf.StringValueB(\xe0\x41\x03\xfa\x41\"\n googleads.googleapis.com/AdGroup\x12l\n\x0fresource_status\x18\x08 \x01(\x0e\x32N.google.ads.googleads.v3.enums.ChangeStatusOperationEnum.ChangeStatusOperationB\x03\xe0\x41\x03\x12]\n\x0b\x61\x64_group_ad\x18\t \x01(\x0b\x32\x1c.google.protobuf.StringValueB*\xe0\x41\x03\xfa\x41$\n\"googleads.googleapis.com/AdGroupAd\x12k\n\x12\x61\x64_group_criterion\x18\n \x01(\x0b\x32\x1c.google.protobuf.StringValueB1\xe0\x41\x03\xfa\x41+\n)googleads.googleapis.com/AdGroupCriterion\x12l\n\x12\x63\x61mpaign_criterion\x18\x0b \x01(\x0b\x32\x1c.google.protobuf.StringValueB2\xe0\x41\x03\xfa\x41,\n*googleads.googleapis.com/CampaignCriterion\x12Q\n\x04\x66\x65\x65\x64\x18\x0c \x01(\x0b\x32\x1c.google.protobuf.StringValueB%\xe0\x41\x03\xfa\x41\x1f\n\x1dgoogleads.googleapis.com/Feed\x12Z\n\tfeed_item\x18\r \x01(\x0b\x32\x1c.google.protobuf.StringValueB)\xe0\x41\x03\xfa\x41#\n!googleads.googleapis.com/FeedItem\x12\x61\n\rad_group_feed\x18\x0e \x01(\x0b\x32\x1c.google.protobuf.StringValueB,\xe0\x41\x03\xfa\x41&\n$googleads.googleapis.com/AdGroupFeed\x12\x62\n\rcampaign_feed\x18\x0f \x01(\x0b\x32\x1c.google.protobuf.StringValueB-\xe0\x41\x03\xfa\x41\'\n%googleads.googleapis.com/CampaignFeed\x12p\n\x15\x61\x64_group_bid_modifier\x18\x10 \x01(\x0b\x32\x1c.google.protobuf.StringValueB3\xe0\x41\x03\xfa\x41-\n+googleads.googleapis.com/AdGroupBidModifier:]\xea\x41Z\n%googleads.googleapis.com/ChangeStatus\x12\x31\x63ustomers/{customer}/changeStatus/{change_status}B\xfe\x01\n%com.google.ads.googleads.v3.resourcesB\x11\x43hangeStatusProtoP\x01ZJgoogle.golang.org/genproto/googleapis/ads/googleads/v3/resources;resources\xa2\x02\x03GAA\xaa\x02!Google.Ads.GoogleAds.V3.Resources\xca\x02!Google\\Ads\\GoogleAds\\V3\\Resources\xea\x02%Google::Ads::GoogleAds::V3::Resourcesb\x06proto3')
  ,
  dependencies=[google_dot_ads_dot_googleads__v3_dot_proto_dot_enums_dot_change__status__operation__pb2.DESCRIPTOR,google_dot_ads_dot_googleads__v3_dot_proto_dot_enums_dot_change__status__resource__type__pb2.DESCRIPTOR,google_dot_api_dot_field__behavior__pb2.DESCRIPTOR,google_dot_api_dot_resource__pb2.DESCRIPTOR,google_dot_protobuf_dot_wrappers__pb2.DESCRIPTOR,google_dot_api_dot_annotations__pb2.DESCRIPTOR,])




_CHANGESTATUS = _descriptor.Descriptor(
  name='ChangeStatus',
  full_name='google.ads.googleads.v3.resources.ChangeStatus',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_name', full_name='google.ads.googleads.v3.resources.ChangeStatus.resource_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\003\372A\'\n%googleads.googleapis.com/ChangeStatus'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='last_change_date_time', full_name='google.ads.googleads.v3.resources.ChangeStatus.last_change_date_time', index=1,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\003'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='resource_type', full_name='google.ads.googleads.v3.resources.ChangeStatus.resource_type', index=2,
      number=4, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\003'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='campaign', full_name='google.ads.googleads.v3.resources.ChangeStatus.campaign', index=3,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\003\372A#\n!googleads.googleapis.com/Campaign'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ad_group', full_name='google.ads.googleads.v3.resources.ChangeStatus.ad_group', index=4,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\003\372A\"\n googleads.googleapis.com/AdGroup'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='resource_status', full_name='google.ads.googleads.v3.resources.ChangeStatus.resource_status', index=5,
      number=8, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\003'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ad_group_ad', full_name='google.ads.googleads.v3.resources.ChangeStatus.ad_group_ad', index=6,
      number=9, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\003\372A$\n\"googleads.googleapis.com/AdGroupAd'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ad_group_criterion', full_name='google.ads.googleads.v3.resources.ChangeStatus.ad_group_criterion', index=7,
      number=10, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\003\372A+\n)googleads.googleapis.com/AdGroupCriterion'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='campaign_criterion', full_name='google.ads.googleads.v3.resources.ChangeStatus.campaign_criterion', index=8,
      number=11, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\003\372A,\n*googleads.googleapis.com/CampaignCriterion'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='feed', full_name='google.ads.googleads.v3.resources.ChangeStatus.feed', index=9,
      number=12, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\003\372A\037\n\035googleads.googleapis.com/Feed'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='feed_item', full_name='google.ads.googleads.v3.resources.ChangeStatus.feed_item', index=10,
      number=13, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\003\372A#\n!googleads.googleapis.com/FeedItem'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ad_group_feed', full_name='google.ads.googleads.v3.resources.ChangeStatus.ad_group_feed', index=11,
      number=14, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\003\372A&\n$googleads.googleapis.com/AdGroupFeed'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='campaign_feed', full_name='google.ads.googleads.v3.resources.ChangeStatus.campaign_feed', index=12,
      number=15, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\003\372A\'\n%googleads.googleapis.com/CampaignFeed'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ad_group_bid_modifier', full_name='google.ads.googleads.v3.resources.ChangeStatus.ad_group_bid_modifier', index=13,
      number=16, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\003\372A-\n+googleads.googleapis.com/AdGroupBidModifier'), file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=_b('\352AZ\n%googleads.googleapis.com/ChangeStatus\0221customers/{customer}/changeStatus/{change_status}'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=359,
  serialized_end=1811,
)

_CHANGESTATUS.fields_by_name['last_change_date_time'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_CHANGESTATUS.fields_by_name['resource_type'].enum_type = google_dot_ads_dot_googleads__v3_dot_proto_dot_enums_dot_change__status__resource__type__pb2._CHANGESTATUSRESOURCETYPEENUM_CHANGESTATUSRESOURCETYPE
_CHANGESTATUS.fields_by_name['campaign'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_CHANGESTATUS.fields_by_name['ad_group'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_CHANGESTATUS.fields_by_name['resource_status'].enum_type = google_dot_ads_dot_googleads__v3_dot_proto_dot_enums_dot_change__status__operation__pb2._CHANGESTATUSOPERATIONENUM_CHANGESTATUSOPERATION
_CHANGESTATUS.fields_by_name['ad_group_ad'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_CHANGESTATUS.fields_by_name['ad_group_criterion'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_CHANGESTATUS.fields_by_name['campaign_criterion'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_CHANGESTATUS.fields_by_name['feed'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_CHANGESTATUS.fields_by_name['feed_item'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_CHANGESTATUS.fields_by_name['ad_group_feed'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_CHANGESTATUS.fields_by_name['campaign_feed'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_CHANGESTATUS.fields_by_name['ad_group_bid_modifier'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
DESCRIPTOR.message_types_by_name['ChangeStatus'] = _CHANGESTATUS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ChangeStatus = _reflection.GeneratedProtocolMessageType('ChangeStatus', (_message.Message,), dict(
  DESCRIPTOR = _CHANGESTATUS,
  __module__ = 'google.ads.googleads_v3.proto.resources.change_status_pb2'
  ,
  __doc__ = """Describes the status of returned resource.
  
  
  Attributes:
      resource_name:
          Output only. The resource name of the change status. Change
          status resource names have the form:
          ``customers/{customer_id}/changeStatus/{change_status_id}``
      last_change_date_time:
          Output only. Time at which the most recent change has occurred
          on this resource.
      resource_type:
          Output only. Represents the type of the changed resource. This
          dictates what fields will be set. For example, for AD\_GROUP,
          campaign and ad\_group fields will be set.
      campaign:
          Output only. The Campaign affected by this change.
      ad_group:
          Output only. The AdGroup affected by this change.
      resource_status:
          Output only. Represents the status of the changed resource.
      ad_group_ad:
          Output only. The AdGroupAd affected by this change.
      ad_group_criterion:
          Output only. The AdGroupCriterion affected by this change.
      campaign_criterion:
          Output only. The CampaignCriterion affected by this change.
      feed:
          Output only. The Feed affected by this change.
      feed_item:
          Output only. The FeedItem affected by this change.
      ad_group_feed:
          Output only. The AdGroupFeed affected by this change.
      campaign_feed:
          Output only. The CampaignFeed affected by this change.
      ad_group_bid_modifier:
          Output only. The AdGroupBidModifier affected by this change.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v3.resources.ChangeStatus)
  ))
_sym_db.RegisterMessage(ChangeStatus)


DESCRIPTOR._options = None
_CHANGESTATUS.fields_by_name['resource_name']._options = None
_CHANGESTATUS.fields_by_name['last_change_date_time']._options = None
_CHANGESTATUS.fields_by_name['resource_type']._options = None
_CHANGESTATUS.fields_by_name['campaign']._options = None
_CHANGESTATUS.fields_by_name['ad_group']._options = None
_CHANGESTATUS.fields_by_name['resource_status']._options = None
_CHANGESTATUS.fields_by_name['ad_group_ad']._options = None
_CHANGESTATUS.fields_by_name['ad_group_criterion']._options = None
_CHANGESTATUS.fields_by_name['campaign_criterion']._options = None
_CHANGESTATUS.fields_by_name['feed']._options = None
_CHANGESTATUS.fields_by_name['feed_item']._options = None
_CHANGESTATUS.fields_by_name['ad_group_feed']._options = None
_CHANGESTATUS.fields_by_name['campaign_feed']._options = None
_CHANGESTATUS.fields_by_name['ad_group_bid_modifier']._options = None
_CHANGESTATUS._options = None
# @@protoc_insertion_point(module_scope)
