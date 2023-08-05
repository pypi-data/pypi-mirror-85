# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.ads.google_ads.v5.proto.services import conversion_upload_service_pb2 as google_dot_ads_dot_googleads__v5_dot_proto_dot_services_dot_conversion__upload__service__pb2


class ConversionUploadServiceStub(object):
    """Service to upload conversions.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.UploadClickConversions = channel.unary_unary(
                '/google.ads.googleads.v5.services.ConversionUploadService/UploadClickConversions',
                request_serializer=google_dot_ads_dot_googleads__v5_dot_proto_dot_services_dot_conversion__upload__service__pb2.UploadClickConversionsRequest.SerializeToString,
                response_deserializer=google_dot_ads_dot_googleads__v5_dot_proto_dot_services_dot_conversion__upload__service__pb2.UploadClickConversionsResponse.FromString,
                )
        self.UploadCallConversions = channel.unary_unary(
                '/google.ads.googleads.v5.services.ConversionUploadService/UploadCallConversions',
                request_serializer=google_dot_ads_dot_googleads__v5_dot_proto_dot_services_dot_conversion__upload__service__pb2.UploadCallConversionsRequest.SerializeToString,
                response_deserializer=google_dot_ads_dot_googleads__v5_dot_proto_dot_services_dot_conversion__upload__service__pb2.UploadCallConversionsResponse.FromString,
                )


class ConversionUploadServiceServicer(object):
    """Service to upload conversions.
    """

    def UploadClickConversions(self, request, context):
        """Processes the given click conversions.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UploadCallConversions(self, request, context):
        """Processes the given call conversions.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ConversionUploadServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'UploadClickConversions': grpc.unary_unary_rpc_method_handler(
                    servicer.UploadClickConversions,
                    request_deserializer=google_dot_ads_dot_googleads__v5_dot_proto_dot_services_dot_conversion__upload__service__pb2.UploadClickConversionsRequest.FromString,
                    response_serializer=google_dot_ads_dot_googleads__v5_dot_proto_dot_services_dot_conversion__upload__service__pb2.UploadClickConversionsResponse.SerializeToString,
            ),
            'UploadCallConversions': grpc.unary_unary_rpc_method_handler(
                    servicer.UploadCallConversions,
                    request_deserializer=google_dot_ads_dot_googleads__v5_dot_proto_dot_services_dot_conversion__upload__service__pb2.UploadCallConversionsRequest.FromString,
                    response_serializer=google_dot_ads_dot_googleads__v5_dot_proto_dot_services_dot_conversion__upload__service__pb2.UploadCallConversionsResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'google.ads.googleads.v5.services.ConversionUploadService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ConversionUploadService(object):
    """Service to upload conversions.
    """

    @staticmethod
    def UploadClickConversions(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/google.ads.googleads.v5.services.ConversionUploadService/UploadClickConversions',
            google_dot_ads_dot_googleads__v5_dot_proto_dot_services_dot_conversion__upload__service__pb2.UploadClickConversionsRequest.SerializeToString,
            google_dot_ads_dot_googleads__v5_dot_proto_dot_services_dot_conversion__upload__service__pb2.UploadClickConversionsResponse.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UploadCallConversions(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/google.ads.googleads.v5.services.ConversionUploadService/UploadCallConversions',
            google_dot_ads_dot_googleads__v5_dot_proto_dot_services_dot_conversion__upload__service__pb2.UploadCallConversionsRequest.SerializeToString,
            google_dot_ads_dot_googleads__v5_dot_proto_dot_services_dot_conversion__upload__service__pb2.UploadCallConversionsResponse.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)
