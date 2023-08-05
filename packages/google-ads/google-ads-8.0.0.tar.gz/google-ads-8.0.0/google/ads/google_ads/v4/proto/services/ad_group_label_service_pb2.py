# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v4/proto/services/ad_group_label_service.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.ads.google_ads.v4.proto.resources import ad_group_label_pb2 as google_dot_ads_dot_googleads__v4_dot_proto_dot_resources_dot_ad__group__label__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.api import client_pb2 as google_dot_api_dot_client__pb2
from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from google.api import resource_pb2 as google_dot_api_dot_resource__pb2
from google.rpc import status_pb2 as google_dot_rpc_dot_status__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v4/proto/services/ad_group_label_service.proto',
  package='google.ads.googleads.v4.services',
  syntax='proto3',
  serialized_options=_b('\n$com.google.ads.googleads.v4.servicesB\030AdGroupLabelServiceProtoP\001ZHgoogle.golang.org/genproto/googleapis/ads/googleads/v4/services;services\242\002\003GAA\252\002 Google.Ads.GoogleAds.V4.Services\312\002 Google\\Ads\\GoogleAds\\V4\\Services\352\002$Google::Ads::GoogleAds::V4::Services'),
  serialized_pb=_b('\nCgoogle/ads/googleads_v4/proto/services/ad_group_label_service.proto\x12 google.ads.googleads.v4.services\x1a<google/ads/googleads_v4/proto/resources/ad_group_label.proto\x1a\x1cgoogle/api/annotations.proto\x1a\x17google/api/client.proto\x1a\x1fgoogle/api/field_behavior.proto\x1a\x19google/api/resource.proto\x1a\x17google/rpc/status.proto\"^\n\x16GetAdGroupLabelRequest\x12\x44\n\rresource_name\x18\x01 \x01(\tB-\xe0\x41\x02\xfa\x41\'\n%googleads.googleapis.com/AdGroupLabel\"\xb8\x01\n\x1aMutateAdGroupLabelsRequest\x12\x18\n\x0b\x63ustomer_id\x18\x01 \x01(\tB\x03\xe0\x41\x02\x12P\n\noperations\x18\x02 \x03(\x0b\x32\x37.google.ads.googleads.v4.services.AdGroupLabelOperationB\x03\xe0\x41\x02\x12\x17\n\x0fpartial_failure\x18\x03 \x01(\x08\x12\x15\n\rvalidate_only\x18\x04 \x01(\x08\"y\n\x15\x41\x64GroupLabelOperation\x12\x41\n\x06\x63reate\x18\x01 \x01(\x0b\x32/.google.ads.googleads.v4.resources.AdGroupLabelH\x00\x12\x10\n\x06remove\x18\x02 \x01(\tH\x00\x42\x0b\n\toperation\"\x9d\x01\n\x1bMutateAdGroupLabelsResponse\x12\x31\n\x15partial_failure_error\x18\x03 \x01(\x0b\x32\x12.google.rpc.Status\x12K\n\x07results\x18\x02 \x03(\x0b\x32:.google.ads.googleads.v4.services.MutateAdGroupLabelResult\"1\n\x18MutateAdGroupLabelResult\x12\x15\n\rresource_name\x18\x01 \x01(\t2\xe7\x03\n\x13\x41\x64GroupLabelService\x12\xc5\x01\n\x0fGetAdGroupLabel\x12\x38.google.ads.googleads.v4.services.GetAdGroupLabelRequest\x1a/.google.ads.googleads.v4.resources.AdGroupLabel\"G\x82\xd3\xe4\x93\x02\x31\x12//v4/{resource_name=customers/*/adGroupLabels/*}\xda\x41\rresource_name\x12\xea\x01\n\x13MutateAdGroupLabels\x12<.google.ads.googleads.v4.services.MutateAdGroupLabelsRequest\x1a=.google.ads.googleads.v4.services.MutateAdGroupLabelsResponse\"V\x82\xd3\xe4\x93\x02\x37\"2/v4/customers/{customer_id=*}/adGroupLabels:mutate:\x01*\xda\x41\x16\x63ustomer_id,operations\x1a\x1b\xca\x41\x18googleads.googleapis.comB\xff\x01\n$com.google.ads.googleads.v4.servicesB\x18\x41\x64GroupLabelServiceProtoP\x01ZHgoogle.golang.org/genproto/googleapis/ads/googleads/v4/services;services\xa2\x02\x03GAA\xaa\x02 Google.Ads.GoogleAds.V4.Services\xca\x02 Google\\Ads\\GoogleAds\\V4\\Services\xea\x02$Google::Ads::GoogleAds::V4::Servicesb\x06proto3')
  ,
  dependencies=[google_dot_ads_dot_googleads__v4_dot_proto_dot_resources_dot_ad__group__label__pb2.DESCRIPTOR,google_dot_api_dot_annotations__pb2.DESCRIPTOR,google_dot_api_dot_client__pb2.DESCRIPTOR,google_dot_api_dot_field__behavior__pb2.DESCRIPTOR,google_dot_api_dot_resource__pb2.DESCRIPTOR,google_dot_rpc_dot_status__pb2.DESCRIPTOR,])




_GETADGROUPLABELREQUEST = _descriptor.Descriptor(
  name='GetAdGroupLabelRequest',
  full_name='google.ads.googleads.v4.services.GetAdGroupLabelRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_name', full_name='google.ads.googleads.v4.services.GetAdGroupLabelRequest.resource_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\002\372A\'\n%googleads.googleapis.com/AdGroupLabel'), file=DESCRIPTOR),
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
  serialized_start=307,
  serialized_end=401,
)


_MUTATEADGROUPLABELSREQUEST = _descriptor.Descriptor(
  name='MutateAdGroupLabelsRequest',
  full_name='google.ads.googleads.v4.services.MutateAdGroupLabelsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='customer_id', full_name='google.ads.googleads.v4.services.MutateAdGroupLabelsRequest.customer_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\002'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='operations', full_name='google.ads.googleads.v4.services.MutateAdGroupLabelsRequest.operations', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\002'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='partial_failure', full_name='google.ads.googleads.v4.services.MutateAdGroupLabelsRequest.partial_failure', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='validate_only', full_name='google.ads.googleads.v4.services.MutateAdGroupLabelsRequest.validate_only', index=3,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=404,
  serialized_end=588,
)


_ADGROUPLABELOPERATION = _descriptor.Descriptor(
  name='AdGroupLabelOperation',
  full_name='google.ads.googleads.v4.services.AdGroupLabelOperation',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='create', full_name='google.ads.googleads.v4.services.AdGroupLabelOperation.create', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='remove', full_name='google.ads.googleads.v4.services.AdGroupLabelOperation.remove', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
      name='operation', full_name='google.ads.googleads.v4.services.AdGroupLabelOperation.operation',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=590,
  serialized_end=711,
)


_MUTATEADGROUPLABELSRESPONSE = _descriptor.Descriptor(
  name='MutateAdGroupLabelsResponse',
  full_name='google.ads.googleads.v4.services.MutateAdGroupLabelsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='partial_failure_error', full_name='google.ads.googleads.v4.services.MutateAdGroupLabelsResponse.partial_failure_error', index=0,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='results', full_name='google.ads.googleads.v4.services.MutateAdGroupLabelsResponse.results', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=714,
  serialized_end=871,
)


_MUTATEADGROUPLABELRESULT = _descriptor.Descriptor(
  name='MutateAdGroupLabelResult',
  full_name='google.ads.googleads.v4.services.MutateAdGroupLabelResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_name', full_name='google.ads.googleads.v4.services.MutateAdGroupLabelResult.resource_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=873,
  serialized_end=922,
)

_MUTATEADGROUPLABELSREQUEST.fields_by_name['operations'].message_type = _ADGROUPLABELOPERATION
_ADGROUPLABELOPERATION.fields_by_name['create'].message_type = google_dot_ads_dot_googleads__v4_dot_proto_dot_resources_dot_ad__group__label__pb2._ADGROUPLABEL
_ADGROUPLABELOPERATION.oneofs_by_name['operation'].fields.append(
  _ADGROUPLABELOPERATION.fields_by_name['create'])
_ADGROUPLABELOPERATION.fields_by_name['create'].containing_oneof = _ADGROUPLABELOPERATION.oneofs_by_name['operation']
_ADGROUPLABELOPERATION.oneofs_by_name['operation'].fields.append(
  _ADGROUPLABELOPERATION.fields_by_name['remove'])
_ADGROUPLABELOPERATION.fields_by_name['remove'].containing_oneof = _ADGROUPLABELOPERATION.oneofs_by_name['operation']
_MUTATEADGROUPLABELSRESPONSE.fields_by_name['partial_failure_error'].message_type = google_dot_rpc_dot_status__pb2._STATUS
_MUTATEADGROUPLABELSRESPONSE.fields_by_name['results'].message_type = _MUTATEADGROUPLABELRESULT
DESCRIPTOR.message_types_by_name['GetAdGroupLabelRequest'] = _GETADGROUPLABELREQUEST
DESCRIPTOR.message_types_by_name['MutateAdGroupLabelsRequest'] = _MUTATEADGROUPLABELSREQUEST
DESCRIPTOR.message_types_by_name['AdGroupLabelOperation'] = _ADGROUPLABELOPERATION
DESCRIPTOR.message_types_by_name['MutateAdGroupLabelsResponse'] = _MUTATEADGROUPLABELSRESPONSE
DESCRIPTOR.message_types_by_name['MutateAdGroupLabelResult'] = _MUTATEADGROUPLABELRESULT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GetAdGroupLabelRequest = _reflection.GeneratedProtocolMessageType('GetAdGroupLabelRequest', (_message.Message,), dict(
  DESCRIPTOR = _GETADGROUPLABELREQUEST,
  __module__ = 'google.ads.googleads_v4.proto.services.ad_group_label_service_pb2'
  ,
  __doc__ = """Request message for
  [AdGroupLabelService.GetAdGroupLabel][google.ads.googleads.v4.services.AdGroupLabelService.GetAdGroupLabel].
  
  
  Attributes:
      resource_name:
          Required. The resource name of the ad group label to fetch.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v4.services.GetAdGroupLabelRequest)
  ))
_sym_db.RegisterMessage(GetAdGroupLabelRequest)

MutateAdGroupLabelsRequest = _reflection.GeneratedProtocolMessageType('MutateAdGroupLabelsRequest', (_message.Message,), dict(
  DESCRIPTOR = _MUTATEADGROUPLABELSREQUEST,
  __module__ = 'google.ads.googleads_v4.proto.services.ad_group_label_service_pb2'
  ,
  __doc__ = """Request message for
  [AdGroupLabelService.MutateAdGroupLabels][google.ads.googleads.v4.services.AdGroupLabelService.MutateAdGroupLabels].
  
  
  Attributes:
      customer_id:
          Required. ID of the customer whose ad group labels are being
          modified.
      operations:
          Required. The list of operations to perform on ad group
          labels.
      partial_failure:
          If true, successful operations will be carried out and invalid
          operations will return errors. If false, all operations will
          be carried out in one transaction if and only if they are all
          valid. Default is false.
      validate_only:
          If true, the request is validated but not executed. Only
          errors are returned, not results.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v4.services.MutateAdGroupLabelsRequest)
  ))
_sym_db.RegisterMessage(MutateAdGroupLabelsRequest)

AdGroupLabelOperation = _reflection.GeneratedProtocolMessageType('AdGroupLabelOperation', (_message.Message,), dict(
  DESCRIPTOR = _ADGROUPLABELOPERATION,
  __module__ = 'google.ads.googleads_v4.proto.services.ad_group_label_service_pb2'
  ,
  __doc__ = """A single operation (create, remove) on an ad group label.
  
  
  Attributes:
      operation:
          The mutate operation.
      create:
          Create operation: No resource name is expected for the new ad
          group label.
      remove:
          Remove operation: A resource name for the ad group label being
          removed, in this format:  ``customers/{customer_id}/adGroupLab
          els/{ad_group_id}~{label_id}``
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v4.services.AdGroupLabelOperation)
  ))
_sym_db.RegisterMessage(AdGroupLabelOperation)

MutateAdGroupLabelsResponse = _reflection.GeneratedProtocolMessageType('MutateAdGroupLabelsResponse', (_message.Message,), dict(
  DESCRIPTOR = _MUTATEADGROUPLABELSRESPONSE,
  __module__ = 'google.ads.googleads_v4.proto.services.ad_group_label_service_pb2'
  ,
  __doc__ = """Response message for an ad group labels mutate.
  
  
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
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v4.services.MutateAdGroupLabelsResponse)
  ))
_sym_db.RegisterMessage(MutateAdGroupLabelsResponse)

MutateAdGroupLabelResult = _reflection.GeneratedProtocolMessageType('MutateAdGroupLabelResult', (_message.Message,), dict(
  DESCRIPTOR = _MUTATEADGROUPLABELRESULT,
  __module__ = 'google.ads.googleads_v4.proto.services.ad_group_label_service_pb2'
  ,
  __doc__ = """The result for an ad group label mutate.
  
  
  Attributes:
      resource_name:
          Returned for successful operations.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v4.services.MutateAdGroupLabelResult)
  ))
_sym_db.RegisterMessage(MutateAdGroupLabelResult)


DESCRIPTOR._options = None
_GETADGROUPLABELREQUEST.fields_by_name['resource_name']._options = None
_MUTATEADGROUPLABELSREQUEST.fields_by_name['customer_id']._options = None
_MUTATEADGROUPLABELSREQUEST.fields_by_name['operations']._options = None

_ADGROUPLABELSERVICE = _descriptor.ServiceDescriptor(
  name='AdGroupLabelService',
  full_name='google.ads.googleads.v4.services.AdGroupLabelService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=_b('\312A\030googleads.googleapis.com'),
  serialized_start=925,
  serialized_end=1412,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetAdGroupLabel',
    full_name='google.ads.googleads.v4.services.AdGroupLabelService.GetAdGroupLabel',
    index=0,
    containing_service=None,
    input_type=_GETADGROUPLABELREQUEST,
    output_type=google_dot_ads_dot_googleads__v4_dot_proto_dot_resources_dot_ad__group__label__pb2._ADGROUPLABEL,
    serialized_options=_b('\202\323\344\223\0021\022//v4/{resource_name=customers/*/adGroupLabels/*}\332A\rresource_name'),
  ),
  _descriptor.MethodDescriptor(
    name='MutateAdGroupLabels',
    full_name='google.ads.googleads.v4.services.AdGroupLabelService.MutateAdGroupLabels',
    index=1,
    containing_service=None,
    input_type=_MUTATEADGROUPLABELSREQUEST,
    output_type=_MUTATEADGROUPLABELSRESPONSE,
    serialized_options=_b('\202\323\344\223\0027\"2/v4/customers/{customer_id=*}/adGroupLabels:mutate:\001*\332A\026customer_id,operations'),
  ),
])
_sym_db.RegisterServiceDescriptor(_ADGROUPLABELSERVICE)

DESCRIPTOR.services_by_name['AdGroupLabelService'] = _ADGROUPLABELSERVICE

# @@protoc_insertion_point(module_scope)
