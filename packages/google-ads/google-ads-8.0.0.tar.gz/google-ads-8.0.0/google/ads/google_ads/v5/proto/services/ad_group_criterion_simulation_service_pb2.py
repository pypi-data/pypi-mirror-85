# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v5/proto/services/ad_group_criterion_simulation_service.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.ads.google_ads.v5.proto.resources import ad_group_criterion_simulation_pb2 as google_dot_ads_dot_googleads__v5_dot_proto_dot_resources_dot_ad__group__criterion__simulation__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.api import client_pb2 as google_dot_api_dot_client__pb2
from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from google.api import resource_pb2 as google_dot_api_dot_resource__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v5/proto/services/ad_group_criterion_simulation_service.proto',
  package='google.ads.googleads.v5.services',
  syntax='proto3',
  serialized_options=b'\n$com.google.ads.googleads.v5.servicesB&AdGroupCriterionSimulationServiceProtoP\001ZHgoogle.golang.org/genproto/googleapis/ads/googleads/v5/services;services\242\002\003GAA\252\002 Google.Ads.GoogleAds.V5.Services\312\002 Google\\Ads\\GoogleAds\\V5\\Services\352\002$Google::Ads::GoogleAds::V5::Services',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\nRgoogle/ads/googleads_v5/proto/services/ad_group_criterion_simulation_service.proto\x12 google.ads.googleads.v5.services\x1aKgoogle/ads/googleads_v5/proto/resources/ad_group_criterion_simulation.proto\x1a\x1cgoogle/api/annotations.proto\x1a\x17google/api/client.proto\x1a\x1fgoogle/api/field_behavior.proto\x1a\x19google/api/resource.proto\"z\n$GetAdGroupCriterionSimulationRequest\x12R\n\rresource_name\x18\x01 \x01(\tB;\xe0\x41\x02\xfa\x41\x35\n3googleads.googleapis.com/AdGroupCriterionSimulation2\xc0\x02\n!AdGroupCriterionSimulationService\x12\xfd\x01\n\x1dGetAdGroupCriterionSimulation\x12\x46.google.ads.googleads.v5.services.GetAdGroupCriterionSimulationRequest\x1a=.google.ads.googleads.v5.resources.AdGroupCriterionSimulation\"U\x82\xd3\xe4\x93\x02?\x12=/v5/{resource_name=customers/*/adGroupCriterionSimulations/*}\xda\x41\rresource_name\x1a\x1b\xca\x41\x18googleads.googleapis.comB\x8d\x02\n$com.google.ads.googleads.v5.servicesB&AdGroupCriterionSimulationServiceProtoP\x01ZHgoogle.golang.org/genproto/googleapis/ads/googleads/v5/services;services\xa2\x02\x03GAA\xaa\x02 Google.Ads.GoogleAds.V5.Services\xca\x02 Google\\Ads\\GoogleAds\\V5\\Services\xea\x02$Google::Ads::GoogleAds::V5::Servicesb\x06proto3'
  ,
  dependencies=[google_dot_ads_dot_googleads__v5_dot_proto_dot_resources_dot_ad__group__criterion__simulation__pb2.DESCRIPTOR,google_dot_api_dot_annotations__pb2.DESCRIPTOR,google_dot_api_dot_client__pb2.DESCRIPTOR,google_dot_api_dot_field__behavior__pb2.DESCRIPTOR,google_dot_api_dot_resource__pb2.DESCRIPTOR,])




_GETADGROUPCRITERIONSIMULATIONREQUEST = _descriptor.Descriptor(
  name='GetAdGroupCriterionSimulationRequest',
  full_name='google.ads.googleads.v5.services.GetAdGroupCriterionSimulationRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_name', full_name='google.ads.googleads.v5.services.GetAdGroupCriterionSimulationRequest.resource_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\340A\002\372A5\n3googleads.googleapis.com/AdGroupCriterionSimulation', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=312,
  serialized_end=434,
)

DESCRIPTOR.message_types_by_name['GetAdGroupCriterionSimulationRequest'] = _GETADGROUPCRITERIONSIMULATIONREQUEST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GetAdGroupCriterionSimulationRequest = _reflection.GeneratedProtocolMessageType('GetAdGroupCriterionSimulationRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETADGROUPCRITERIONSIMULATIONREQUEST,
  '__module__' : 'google.ads.googleads_v5.proto.services.ad_group_criterion_simulation_service_pb2'
  ,
  '__doc__': """Request message for [AdGroupCriterionSimulationService.GetAdGroupCrite
  rionSimulation][google.ads.googleads.v5.services.AdGroupCriterionSimul
  ationService.GetAdGroupCriterionSimulation].
  
  Attributes:
      resource_name:
          Required. The resource name of the ad group criterion
          simulation to fetch.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v5.services.GetAdGroupCriterionSimulationRequest)
  })
_sym_db.RegisterMessage(GetAdGroupCriterionSimulationRequest)


DESCRIPTOR._options = None
_GETADGROUPCRITERIONSIMULATIONREQUEST.fields_by_name['resource_name']._options = None

_ADGROUPCRITERIONSIMULATIONSERVICE = _descriptor.ServiceDescriptor(
  name='AdGroupCriterionSimulationService',
  full_name='google.ads.googleads.v5.services.AdGroupCriterionSimulationService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=b'\312A\030googleads.googleapis.com',
  create_key=_descriptor._internal_create_key,
  serialized_start=437,
  serialized_end=757,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetAdGroupCriterionSimulation',
    full_name='google.ads.googleads.v5.services.AdGroupCriterionSimulationService.GetAdGroupCriterionSimulation',
    index=0,
    containing_service=None,
    input_type=_GETADGROUPCRITERIONSIMULATIONREQUEST,
    output_type=google_dot_ads_dot_googleads__v5_dot_proto_dot_resources_dot_ad__group__criterion__simulation__pb2._ADGROUPCRITERIONSIMULATION,
    serialized_options=b'\202\323\344\223\002?\022=/v5/{resource_name=customers/*/adGroupCriterionSimulations/*}\332A\rresource_name',
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_ADGROUPCRITERIONSIMULATIONSERVICE)

DESCRIPTOR.services_by_name['AdGroupCriterionSimulationService'] = _ADGROUPCRITERIONSIMULATIONSERVICE

# @@protoc_insertion_point(module_scope)
