# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v3/proto/services/media_file_service.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.ads.google_ads.v3.proto.resources import media_file_pb2 as google_dot_ads_dot_googleads__v3_dot_proto_dot_resources_dot_media__file__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.api import client_pb2 as google_dot_api_dot_client__pb2
from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from google.api import resource_pb2 as google_dot_api_dot_resource__pb2
from google.rpc import status_pb2 as google_dot_rpc_dot_status__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v3/proto/services/media_file_service.proto',
  package='google.ads.googleads.v3.services',
  syntax='proto3',
  serialized_options=_b('\n$com.google.ads.googleads.v3.servicesB\025MediaFileServiceProtoP\001ZHgoogle.golang.org/genproto/googleapis/ads/googleads/v3/services;services\242\002\003GAA\252\002 Google.Ads.GoogleAds.V3.Services\312\002 Google\\Ads\\GoogleAds\\V3\\Services\352\002$Google::Ads::GoogleAds::V3::Services'),
  serialized_pb=_b('\n?google/ads/googleads_v3/proto/services/media_file_service.proto\x12 google.ads.googleads.v3.services\x1a\x38google/ads/googleads_v3/proto/resources/media_file.proto\x1a\x1cgoogle/api/annotations.proto\x1a\x17google/api/client.proto\x1a\x1fgoogle/api/field_behavior.proto\x1a\x19google/api/resource.proto\x1a\x17google/rpc/status.proto\"X\n\x13GetMediaFileRequest\x12\x41\n\rresource_name\x18\x01 \x01(\tB*\xe0\x41\x02\xfa\x41$\n\"googleads.googleapis.com/MediaFile\"\xb2\x01\n\x17MutateMediaFilesRequest\x12\x18\n\x0b\x63ustomer_id\x18\x01 \x01(\tB\x03\xe0\x41\x02\x12M\n\noperations\x18\x02 \x03(\x0b\x32\x34.google.ads.googleads.v3.services.MediaFileOperationB\x03\xe0\x41\x02\x12\x17\n\x0fpartial_failure\x18\x03 \x01(\x08\x12\x15\n\rvalidate_only\x18\x04 \x01(\x08\"a\n\x12MediaFileOperation\x12>\n\x06\x63reate\x18\x01 \x01(\x0b\x32,.google.ads.googleads.v3.resources.MediaFileH\x00\x42\x0b\n\toperation\"\x97\x01\n\x18MutateMediaFilesResponse\x12\x31\n\x15partial_failure_error\x18\x03 \x01(\x0b\x32\x12.google.rpc.Status\x12H\n\x07results\x18\x02 \x03(\x0b\x32\x37.google.ads.googleads.v3.services.MutateMediaFileResult\".\n\x15MutateMediaFileResult\x12\x15\n\rresource_name\x18\x01 \x01(\t2\xcc\x03\n\x10MediaFileService\x12\xb9\x01\n\x0cGetMediaFile\x12\x35.google.ads.googleads.v3.services.GetMediaFileRequest\x1a,.google.ads.googleads.v3.resources.MediaFile\"D\x82\xd3\xe4\x93\x02.\x12,/v3/{resource_name=customers/*/mediaFiles/*}\xda\x41\rresource_name\x12\xde\x01\n\x10MutateMediaFiles\x12\x39.google.ads.googleads.v3.services.MutateMediaFilesRequest\x1a:.google.ads.googleads.v3.services.MutateMediaFilesResponse\"S\x82\xd3\xe4\x93\x02\x34\"//v3/customers/{customer_id=*}/mediaFiles:mutate:\x01*\xda\x41\x16\x63ustomer_id,operations\x1a\x1b\xca\x41\x18googleads.googleapis.comB\xfc\x01\n$com.google.ads.googleads.v3.servicesB\x15MediaFileServiceProtoP\x01ZHgoogle.golang.org/genproto/googleapis/ads/googleads/v3/services;services\xa2\x02\x03GAA\xaa\x02 Google.Ads.GoogleAds.V3.Services\xca\x02 Google\\Ads\\GoogleAds\\V3\\Services\xea\x02$Google::Ads::GoogleAds::V3::Servicesb\x06proto3')
  ,
  dependencies=[google_dot_ads_dot_googleads__v3_dot_proto_dot_resources_dot_media__file__pb2.DESCRIPTOR,google_dot_api_dot_annotations__pb2.DESCRIPTOR,google_dot_api_dot_client__pb2.DESCRIPTOR,google_dot_api_dot_field__behavior__pb2.DESCRIPTOR,google_dot_api_dot_resource__pb2.DESCRIPTOR,google_dot_rpc_dot_status__pb2.DESCRIPTOR,])




_GETMEDIAFILEREQUEST = _descriptor.Descriptor(
  name='GetMediaFileRequest',
  full_name='google.ads.googleads.v3.services.GetMediaFileRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_name', full_name='google.ads.googleads.v3.services.GetMediaFileRequest.resource_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\002\372A$\n\"googleads.googleapis.com/MediaFile'), file=DESCRIPTOR),
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
  serialized_start=299,
  serialized_end=387,
)


_MUTATEMEDIAFILESREQUEST = _descriptor.Descriptor(
  name='MutateMediaFilesRequest',
  full_name='google.ads.googleads.v3.services.MutateMediaFilesRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='customer_id', full_name='google.ads.googleads.v3.services.MutateMediaFilesRequest.customer_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\002'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='operations', full_name='google.ads.googleads.v3.services.MutateMediaFilesRequest.operations', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\002'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='partial_failure', full_name='google.ads.googleads.v3.services.MutateMediaFilesRequest.partial_failure', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='validate_only', full_name='google.ads.googleads.v3.services.MutateMediaFilesRequest.validate_only', index=3,
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
  serialized_start=390,
  serialized_end=568,
)


_MEDIAFILEOPERATION = _descriptor.Descriptor(
  name='MediaFileOperation',
  full_name='google.ads.googleads.v3.services.MediaFileOperation',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='create', full_name='google.ads.googleads.v3.services.MediaFileOperation.create', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
      name='operation', full_name='google.ads.googleads.v3.services.MediaFileOperation.operation',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=570,
  serialized_end=667,
)


_MUTATEMEDIAFILESRESPONSE = _descriptor.Descriptor(
  name='MutateMediaFilesResponse',
  full_name='google.ads.googleads.v3.services.MutateMediaFilesResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='partial_failure_error', full_name='google.ads.googleads.v3.services.MutateMediaFilesResponse.partial_failure_error', index=0,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='results', full_name='google.ads.googleads.v3.services.MutateMediaFilesResponse.results', index=1,
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
  serialized_start=670,
  serialized_end=821,
)


_MUTATEMEDIAFILERESULT = _descriptor.Descriptor(
  name='MutateMediaFileResult',
  full_name='google.ads.googleads.v3.services.MutateMediaFileResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_name', full_name='google.ads.googleads.v3.services.MutateMediaFileResult.resource_name', index=0,
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
  serialized_start=823,
  serialized_end=869,
)

_MUTATEMEDIAFILESREQUEST.fields_by_name['operations'].message_type = _MEDIAFILEOPERATION
_MEDIAFILEOPERATION.fields_by_name['create'].message_type = google_dot_ads_dot_googleads__v3_dot_proto_dot_resources_dot_media__file__pb2._MEDIAFILE
_MEDIAFILEOPERATION.oneofs_by_name['operation'].fields.append(
  _MEDIAFILEOPERATION.fields_by_name['create'])
_MEDIAFILEOPERATION.fields_by_name['create'].containing_oneof = _MEDIAFILEOPERATION.oneofs_by_name['operation']
_MUTATEMEDIAFILESRESPONSE.fields_by_name['partial_failure_error'].message_type = google_dot_rpc_dot_status__pb2._STATUS
_MUTATEMEDIAFILESRESPONSE.fields_by_name['results'].message_type = _MUTATEMEDIAFILERESULT
DESCRIPTOR.message_types_by_name['GetMediaFileRequest'] = _GETMEDIAFILEREQUEST
DESCRIPTOR.message_types_by_name['MutateMediaFilesRequest'] = _MUTATEMEDIAFILESREQUEST
DESCRIPTOR.message_types_by_name['MediaFileOperation'] = _MEDIAFILEOPERATION
DESCRIPTOR.message_types_by_name['MutateMediaFilesResponse'] = _MUTATEMEDIAFILESRESPONSE
DESCRIPTOR.message_types_by_name['MutateMediaFileResult'] = _MUTATEMEDIAFILERESULT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GetMediaFileRequest = _reflection.GeneratedProtocolMessageType('GetMediaFileRequest', (_message.Message,), dict(
  DESCRIPTOR = _GETMEDIAFILEREQUEST,
  __module__ = 'google.ads.googleads_v3.proto.services.media_file_service_pb2'
  ,
  __doc__ = """Request message for
  [MediaFileService.GetMediaFile][google.ads.googleads.v3.services.MediaFileService.GetMediaFile]
  
  
  Attributes:
      resource_name:
          Required. The resource name of the media file to fetch.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v3.services.GetMediaFileRequest)
  ))
_sym_db.RegisterMessage(GetMediaFileRequest)

MutateMediaFilesRequest = _reflection.GeneratedProtocolMessageType('MutateMediaFilesRequest', (_message.Message,), dict(
  DESCRIPTOR = _MUTATEMEDIAFILESREQUEST,
  __module__ = 'google.ads.googleads_v3.proto.services.media_file_service_pb2'
  ,
  __doc__ = """Request message for
  [MediaFileService.MutateMediaFiles][google.ads.googleads.v3.services.MediaFileService.MutateMediaFiles]
  
  
  Attributes:
      customer_id:
          Required. The ID of the customer whose media files are being
          modified.
      operations:
          Required. The list of operations to perform on individual
          media file.
      partial_failure:
          If true, successful operations will be carried out and invalid
          operations will return errors. If false, all operations will
          be carried out in one transaction if and only if they are all
          valid. Default is false.
      validate_only:
          If true, the request is validated but not executed. Only
          errors are returned, not results.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v3.services.MutateMediaFilesRequest)
  ))
_sym_db.RegisterMessage(MutateMediaFilesRequest)

MediaFileOperation = _reflection.GeneratedProtocolMessageType('MediaFileOperation', (_message.Message,), dict(
  DESCRIPTOR = _MEDIAFILEOPERATION,
  __module__ = 'google.ads.googleads_v3.proto.services.media_file_service_pb2'
  ,
  __doc__ = """A single operation to create media file.
  
  
  Attributes:
      operation:
          The mutate operation.
      create:
          Create operation: No resource name is expected for the new
          media file.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v3.services.MediaFileOperation)
  ))
_sym_db.RegisterMessage(MediaFileOperation)

MutateMediaFilesResponse = _reflection.GeneratedProtocolMessageType('MutateMediaFilesResponse', (_message.Message,), dict(
  DESCRIPTOR = _MUTATEMEDIAFILESRESPONSE,
  __module__ = 'google.ads.googleads_v3.proto.services.media_file_service_pb2'
  ,
  __doc__ = """Response message for a media file mutate.
  
  
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
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v3.services.MutateMediaFilesResponse)
  ))
_sym_db.RegisterMessage(MutateMediaFilesResponse)

MutateMediaFileResult = _reflection.GeneratedProtocolMessageType('MutateMediaFileResult', (_message.Message,), dict(
  DESCRIPTOR = _MUTATEMEDIAFILERESULT,
  __module__ = 'google.ads.googleads_v3.proto.services.media_file_service_pb2'
  ,
  __doc__ = """The result for the media file mutate.
  
  
  Attributes:
      resource_name:
          The resource name returned for successful operations.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v3.services.MutateMediaFileResult)
  ))
_sym_db.RegisterMessage(MutateMediaFileResult)


DESCRIPTOR._options = None
_GETMEDIAFILEREQUEST.fields_by_name['resource_name']._options = None
_MUTATEMEDIAFILESREQUEST.fields_by_name['customer_id']._options = None
_MUTATEMEDIAFILESREQUEST.fields_by_name['operations']._options = None

_MEDIAFILESERVICE = _descriptor.ServiceDescriptor(
  name='MediaFileService',
  full_name='google.ads.googleads.v3.services.MediaFileService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=_b('\312A\030googleads.googleapis.com'),
  serialized_start=872,
  serialized_end=1332,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetMediaFile',
    full_name='google.ads.googleads.v3.services.MediaFileService.GetMediaFile',
    index=0,
    containing_service=None,
    input_type=_GETMEDIAFILEREQUEST,
    output_type=google_dot_ads_dot_googleads__v3_dot_proto_dot_resources_dot_media__file__pb2._MEDIAFILE,
    serialized_options=_b('\202\323\344\223\002.\022,/v3/{resource_name=customers/*/mediaFiles/*}\332A\rresource_name'),
  ),
  _descriptor.MethodDescriptor(
    name='MutateMediaFiles',
    full_name='google.ads.googleads.v3.services.MediaFileService.MutateMediaFiles',
    index=1,
    containing_service=None,
    input_type=_MUTATEMEDIAFILESREQUEST,
    output_type=_MUTATEMEDIAFILESRESPONSE,
    serialized_options=_b('\202\323\344\223\0024\"//v3/customers/{customer_id=*}/mediaFiles:mutate:\001*\332A\026customer_id,operations'),
  ),
])
_sym_db.RegisterServiceDescriptor(_MEDIAFILESERVICE)

DESCRIPTOR.services_by_name['MediaFileService'] = _MEDIAFILESERVICE

# @@protoc_insertion_point(module_scope)
