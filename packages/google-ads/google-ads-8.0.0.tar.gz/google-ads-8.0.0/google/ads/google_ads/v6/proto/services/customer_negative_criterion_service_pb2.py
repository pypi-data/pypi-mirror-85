# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v6/proto/services/customer_negative_criterion_service.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.ads.google_ads.v6.proto.resources import customer_negative_criterion_pb2 as google_dot_ads_dot_googleads__v6_dot_proto_dot_resources_dot_customer__negative__criterion__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.api import client_pb2 as google_dot_api_dot_client__pb2
from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from google.api import resource_pb2 as google_dot_api_dot_resource__pb2
from google.rpc import status_pb2 as google_dot_rpc_dot_status__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v6/proto/services/customer_negative_criterion_service.proto',
  package='google.ads.googleads.v6.services',
  syntax='proto3',
  serialized_options=b'\n$com.google.ads.googleads.v6.servicesB%CustomerNegativeCriterionServiceProtoP\001ZHgoogle.golang.org/genproto/googleapis/ads/googleads/v6/services;services\242\002\003GAA\252\002 Google.Ads.GoogleAds.V6.Services\312\002 Google\\Ads\\GoogleAds\\V6\\Services\352\002$Google::Ads::GoogleAds::V6::Services',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\nPgoogle/ads/googleads_v6/proto/services/customer_negative_criterion_service.proto\x12 google.ads.googleads.v6.services\x1aIgoogle/ads/googleads_v6/proto/resources/customer_negative_criterion.proto\x1a\x1cgoogle/api/annotations.proto\x1a\x17google/api/client.proto\x1a\x1fgoogle/api/field_behavior.proto\x1a\x19google/api/resource.proto\x1a\x17google/rpc/status.proto\"x\n#GetCustomerNegativeCriterionRequest\x12Q\n\rresource_name\x18\x01 \x01(\tB:\xe0\x41\x02\xfa\x41\x34\n2googleads.googleapis.com/CustomerNegativeCriterion\"\xd0\x01\n%MutateCustomerNegativeCriteriaRequest\x12\x18\n\x0b\x63ustomer_id\x18\x01 \x01(\tB\x03\xe0\x41\x02\x12]\n\noperations\x18\x02 \x03(\x0b\x32\x44.google.ads.googleads.v6.services.CustomerNegativeCriterionOperationB\x03\xe0\x41\x02\x12\x17\n\x0fpartial_failure\x18\x03 \x01(\x08\x12\x15\n\rvalidate_only\x18\x04 \x01(\x08\"\x93\x01\n\"CustomerNegativeCriterionOperation\x12N\n\x06\x63reate\x18\x01 \x01(\x0b\x32<.google.ads.googleads.v6.resources.CustomerNegativeCriterionH\x00\x12\x10\n\x06remove\x18\x02 \x01(\tH\x00\x42\x0b\n\toperation\"\xb4\x01\n&MutateCustomerNegativeCriteriaResponse\x12\x31\n\x15partial_failure_error\x18\x03 \x01(\x0b\x32\x12.google.rpc.Status\x12W\n\x07results\x18\x02 \x03(\x0b\x32\x46.google.ads.googleads.v6.services.MutateCustomerNegativeCriteriaResult\"=\n$MutateCustomerNegativeCriteriaResult\x12\x15\n\rresource_name\x18\x01 \x01(\t2\xd2\x04\n CustomerNegativeCriterionService\x12\xf7\x01\n\x1cGetCustomerNegativeCriterion\x12\x45.google.ads.googleads.v6.services.GetCustomerNegativeCriterionRequest\x1a<.google.ads.googleads.v6.resources.CustomerNegativeCriterion\"R\x82\xd3\xe4\x93\x02<\x12:/v6/{resource_name=customers/*/customerNegativeCriteria/*}\xda\x41\rresource_name\x12\x96\x02\n\x1eMutateCustomerNegativeCriteria\x12G.google.ads.googleads.v6.services.MutateCustomerNegativeCriteriaRequest\x1aH.google.ads.googleads.v6.services.MutateCustomerNegativeCriteriaResponse\"a\x82\xd3\xe4\x93\x02\x42\"=/v6/customers/{customer_id=*}/customerNegativeCriteria:mutate:\x01*\xda\x41\x16\x63ustomer_id,operations\x1a\x1b\xca\x41\x18googleads.googleapis.comB\x8c\x02\n$com.google.ads.googleads.v6.servicesB%CustomerNegativeCriterionServiceProtoP\x01ZHgoogle.golang.org/genproto/googleapis/ads/googleads/v6/services;services\xa2\x02\x03GAA\xaa\x02 Google.Ads.GoogleAds.V6.Services\xca\x02 Google\\Ads\\GoogleAds\\V6\\Services\xea\x02$Google::Ads::GoogleAds::V6::Servicesb\x06proto3'
  ,
  dependencies=[google_dot_ads_dot_googleads__v6_dot_proto_dot_resources_dot_customer__negative__criterion__pb2.DESCRIPTOR,google_dot_api_dot_annotations__pb2.DESCRIPTOR,google_dot_api_dot_client__pb2.DESCRIPTOR,google_dot_api_dot_field__behavior__pb2.DESCRIPTOR,google_dot_api_dot_resource__pb2.DESCRIPTOR,google_dot_rpc_dot_status__pb2.DESCRIPTOR,])




_GETCUSTOMERNEGATIVECRITERIONREQUEST = _descriptor.Descriptor(
  name='GetCustomerNegativeCriterionRequest',
  full_name='google.ads.googleads.v6.services.GetCustomerNegativeCriterionRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_name', full_name='google.ads.googleads.v6.services.GetCustomerNegativeCriterionRequest.resource_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\340A\002\372A4\n2googleads.googleapis.com/CustomerNegativeCriterion', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=333,
  serialized_end=453,
)


_MUTATECUSTOMERNEGATIVECRITERIAREQUEST = _descriptor.Descriptor(
  name='MutateCustomerNegativeCriteriaRequest',
  full_name='google.ads.googleads.v6.services.MutateCustomerNegativeCriteriaRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='customer_id', full_name='google.ads.googleads.v6.services.MutateCustomerNegativeCriteriaRequest.customer_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\340A\002', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='operations', full_name='google.ads.googleads.v6.services.MutateCustomerNegativeCriteriaRequest.operations', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\340A\002', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='partial_failure', full_name='google.ads.googleads.v6.services.MutateCustomerNegativeCriteriaRequest.partial_failure', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='validate_only', full_name='google.ads.googleads.v6.services.MutateCustomerNegativeCriteriaRequest.validate_only', index=3,
      number=4, type=8, cpp_type=7, label=1,
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
  ],
  serialized_start=456,
  serialized_end=664,
)


_CUSTOMERNEGATIVECRITERIONOPERATION = _descriptor.Descriptor(
  name='CustomerNegativeCriterionOperation',
  full_name='google.ads.googleads.v6.services.CustomerNegativeCriterionOperation',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='create', full_name='google.ads.googleads.v6.services.CustomerNegativeCriterionOperation.create', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='remove', full_name='google.ads.googleads.v6.services.CustomerNegativeCriterionOperation.remove', index=1,
      number=2, type=9, cpp_type=9, label=1,
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
      name='operation', full_name='google.ads.googleads.v6.services.CustomerNegativeCriterionOperation.operation',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=667,
  serialized_end=814,
)


_MUTATECUSTOMERNEGATIVECRITERIARESPONSE = _descriptor.Descriptor(
  name='MutateCustomerNegativeCriteriaResponse',
  full_name='google.ads.googleads.v6.services.MutateCustomerNegativeCriteriaResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='partial_failure_error', full_name='google.ads.googleads.v6.services.MutateCustomerNegativeCriteriaResponse.partial_failure_error', index=0,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='results', full_name='google.ads.googleads.v6.services.MutateCustomerNegativeCriteriaResponse.results', index=1,
      number=2, type=11, cpp_type=10, label=3,
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
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=817,
  serialized_end=997,
)


_MUTATECUSTOMERNEGATIVECRITERIARESULT = _descriptor.Descriptor(
  name='MutateCustomerNegativeCriteriaResult',
  full_name='google.ads.googleads.v6.services.MutateCustomerNegativeCriteriaResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_name', full_name='google.ads.googleads.v6.services.MutateCustomerNegativeCriteriaResult.resource_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
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
  ],
  serialized_start=999,
  serialized_end=1060,
)

_MUTATECUSTOMERNEGATIVECRITERIAREQUEST.fields_by_name['operations'].message_type = _CUSTOMERNEGATIVECRITERIONOPERATION
_CUSTOMERNEGATIVECRITERIONOPERATION.fields_by_name['create'].message_type = google_dot_ads_dot_googleads__v6_dot_proto_dot_resources_dot_customer__negative__criterion__pb2._CUSTOMERNEGATIVECRITERION
_CUSTOMERNEGATIVECRITERIONOPERATION.oneofs_by_name['operation'].fields.append(
  _CUSTOMERNEGATIVECRITERIONOPERATION.fields_by_name['create'])
_CUSTOMERNEGATIVECRITERIONOPERATION.fields_by_name['create'].containing_oneof = _CUSTOMERNEGATIVECRITERIONOPERATION.oneofs_by_name['operation']
_CUSTOMERNEGATIVECRITERIONOPERATION.oneofs_by_name['operation'].fields.append(
  _CUSTOMERNEGATIVECRITERIONOPERATION.fields_by_name['remove'])
_CUSTOMERNEGATIVECRITERIONOPERATION.fields_by_name['remove'].containing_oneof = _CUSTOMERNEGATIVECRITERIONOPERATION.oneofs_by_name['operation']
_MUTATECUSTOMERNEGATIVECRITERIARESPONSE.fields_by_name['partial_failure_error'].message_type = google_dot_rpc_dot_status__pb2._STATUS
_MUTATECUSTOMERNEGATIVECRITERIARESPONSE.fields_by_name['results'].message_type = _MUTATECUSTOMERNEGATIVECRITERIARESULT
DESCRIPTOR.message_types_by_name['GetCustomerNegativeCriterionRequest'] = _GETCUSTOMERNEGATIVECRITERIONREQUEST
DESCRIPTOR.message_types_by_name['MutateCustomerNegativeCriteriaRequest'] = _MUTATECUSTOMERNEGATIVECRITERIAREQUEST
DESCRIPTOR.message_types_by_name['CustomerNegativeCriterionOperation'] = _CUSTOMERNEGATIVECRITERIONOPERATION
DESCRIPTOR.message_types_by_name['MutateCustomerNegativeCriteriaResponse'] = _MUTATECUSTOMERNEGATIVECRITERIARESPONSE
DESCRIPTOR.message_types_by_name['MutateCustomerNegativeCriteriaResult'] = _MUTATECUSTOMERNEGATIVECRITERIARESULT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GetCustomerNegativeCriterionRequest = _reflection.GeneratedProtocolMessageType('GetCustomerNegativeCriterionRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETCUSTOMERNEGATIVECRITERIONREQUEST,
  '__module__' : 'google.ads.googleads_v6.proto.services.customer_negative_criterion_service_pb2'
  ,
  '__doc__': """Request message for [CustomerNegativeCriterionService.GetCustomerNegat
  iveCriterion][google.ads.googleads.v6.services.CustomerNegativeCriteri
  onService.GetCustomerNegativeCriterion].
  
  Attributes:
      resource_name:
          Required. The resource name of the criterion to fetch.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v6.services.GetCustomerNegativeCriterionRequest)
  })
_sym_db.RegisterMessage(GetCustomerNegativeCriterionRequest)

MutateCustomerNegativeCriteriaRequest = _reflection.GeneratedProtocolMessageType('MutateCustomerNegativeCriteriaRequest', (_message.Message,), {
  'DESCRIPTOR' : _MUTATECUSTOMERNEGATIVECRITERIAREQUEST,
  '__module__' : 'google.ads.googleads_v6.proto.services.customer_negative_criterion_service_pb2'
  ,
  '__doc__': """Request message for [CustomerNegativeCriterionService.MutateCustomerNe
  gativeCriteria][google.ads.googleads.v6.services.CustomerNegativeCrite
  rionService.MutateCustomerNegativeCriteria].
  
  Attributes:
      customer_id:
          Required. The ID of the customer whose criteria are being
          modified.
      operations:
          Required. The list of operations to perform on individual
          criteria.
      partial_failure:
          If true, successful operations will be carried out and invalid
          operations will return errors. If false, all operations will
          be carried out in one transaction if and only if they are all
          valid. Default is false.
      validate_only:
          If true, the request is validated but not executed. Only
          errors are returned, not results.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v6.services.MutateCustomerNegativeCriteriaRequest)
  })
_sym_db.RegisterMessage(MutateCustomerNegativeCriteriaRequest)

CustomerNegativeCriterionOperation = _reflection.GeneratedProtocolMessageType('CustomerNegativeCriterionOperation', (_message.Message,), {
  'DESCRIPTOR' : _CUSTOMERNEGATIVECRITERIONOPERATION,
  '__module__' : 'google.ads.googleads_v6.proto.services.customer_negative_criterion_service_pb2'
  ,
  '__doc__': """A single operation (create or remove) on a customer level negative
  criterion.
  
  Attributes:
      operation:
          The mutate operation.
      create:
          Create operation: No resource name is expected for the new
          criterion.
      remove:
          Remove operation: A resource name for the removed criterion is
          expected, in this format:  ``customers/{customer_id}/customerN
          egativeCriteria/{criterion_id}``
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v6.services.CustomerNegativeCriterionOperation)
  })
_sym_db.RegisterMessage(CustomerNegativeCriterionOperation)

MutateCustomerNegativeCriteriaResponse = _reflection.GeneratedProtocolMessageType('MutateCustomerNegativeCriteriaResponse', (_message.Message,), {
  'DESCRIPTOR' : _MUTATECUSTOMERNEGATIVECRITERIARESPONSE,
  '__module__' : 'google.ads.googleads_v6.proto.services.customer_negative_criterion_service_pb2'
  ,
  '__doc__': """Response message for customer negative criterion mutate.
  
  Attributes:
      partial_failure_error:
          Errors that pertain to operation failures in the partial
          failure mode. Returned only when partial\_failure = true and
          all errors occur inside the operations. If any errors occur
          outside the operations (e.g. auth errors), we return an RPC
          level error.
      results:
          All results for the mutate.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v6.services.MutateCustomerNegativeCriteriaResponse)
  })
_sym_db.RegisterMessage(MutateCustomerNegativeCriteriaResponse)

MutateCustomerNegativeCriteriaResult = _reflection.GeneratedProtocolMessageType('MutateCustomerNegativeCriteriaResult', (_message.Message,), {
  'DESCRIPTOR' : _MUTATECUSTOMERNEGATIVECRITERIARESULT,
  '__module__' : 'google.ads.googleads_v6.proto.services.customer_negative_criterion_service_pb2'
  ,
  '__doc__': """The result for the criterion mutate.
  
  Attributes:
      resource_name:
          Returned for successful operations.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v6.services.MutateCustomerNegativeCriteriaResult)
  })
_sym_db.RegisterMessage(MutateCustomerNegativeCriteriaResult)


DESCRIPTOR._options = None
_GETCUSTOMERNEGATIVECRITERIONREQUEST.fields_by_name['resource_name']._options = None
_MUTATECUSTOMERNEGATIVECRITERIAREQUEST.fields_by_name['customer_id']._options = None
_MUTATECUSTOMERNEGATIVECRITERIAREQUEST.fields_by_name['operations']._options = None

_CUSTOMERNEGATIVECRITERIONSERVICE = _descriptor.ServiceDescriptor(
  name='CustomerNegativeCriterionService',
  full_name='google.ads.googleads.v6.services.CustomerNegativeCriterionService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=b'\312A\030googleads.googleapis.com',
  create_key=_descriptor._internal_create_key,
  serialized_start=1063,
  serialized_end=1657,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetCustomerNegativeCriterion',
    full_name='google.ads.googleads.v6.services.CustomerNegativeCriterionService.GetCustomerNegativeCriterion',
    index=0,
    containing_service=None,
    input_type=_GETCUSTOMERNEGATIVECRITERIONREQUEST,
    output_type=google_dot_ads_dot_googleads__v6_dot_proto_dot_resources_dot_customer__negative__criterion__pb2._CUSTOMERNEGATIVECRITERION,
    serialized_options=b'\202\323\344\223\002<\022:/v6/{resource_name=customers/*/customerNegativeCriteria/*}\332A\rresource_name',
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='MutateCustomerNegativeCriteria',
    full_name='google.ads.googleads.v6.services.CustomerNegativeCriterionService.MutateCustomerNegativeCriteria',
    index=1,
    containing_service=None,
    input_type=_MUTATECUSTOMERNEGATIVECRITERIAREQUEST,
    output_type=_MUTATECUSTOMERNEGATIVECRITERIARESPONSE,
    serialized_options=b'\202\323\344\223\002B\"=/v6/customers/{customer_id=*}/customerNegativeCriteria:mutate:\001*\332A\026customer_id,operations',
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_CUSTOMERNEGATIVECRITERIONSERVICE)

DESCRIPTOR.services_by_name['CustomerNegativeCriterionService'] = _CUSTOMERNEGATIVECRITERIONSERVICE

# @@protoc_insertion_point(module_scope)
