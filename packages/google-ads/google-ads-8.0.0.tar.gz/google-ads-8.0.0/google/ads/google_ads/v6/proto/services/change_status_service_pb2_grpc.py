# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.ads.google_ads.v6.proto.resources import change_status_pb2 as google_dot_ads_dot_googleads__v6_dot_proto_dot_resources_dot_change__status__pb2
from google.ads.google_ads.v6.proto.services import change_status_service_pb2 as google_dot_ads_dot_googleads__v6_dot_proto_dot_services_dot_change__status__service__pb2


class ChangeStatusServiceStub(object):
    """Proto file describing the Change Status service.

    Service to fetch change statuses.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetChangeStatus = channel.unary_unary(
                '/google.ads.googleads.v6.services.ChangeStatusService/GetChangeStatus',
                request_serializer=google_dot_ads_dot_googleads__v6_dot_proto_dot_services_dot_change__status__service__pb2.GetChangeStatusRequest.SerializeToString,
                response_deserializer=google_dot_ads_dot_googleads__v6_dot_proto_dot_resources_dot_change__status__pb2.ChangeStatus.FromString,
                )


class ChangeStatusServiceServicer(object):
    """Proto file describing the Change Status service.

    Service to fetch change statuses.
    """

    def GetChangeStatus(self, request, context):
        """Returns the requested change status in full detail.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ChangeStatusServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetChangeStatus': grpc.unary_unary_rpc_method_handler(
                    servicer.GetChangeStatus,
                    request_deserializer=google_dot_ads_dot_googleads__v6_dot_proto_dot_services_dot_change__status__service__pb2.GetChangeStatusRequest.FromString,
                    response_serializer=google_dot_ads_dot_googleads__v6_dot_proto_dot_resources_dot_change__status__pb2.ChangeStatus.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'google.ads.googleads.v6.services.ChangeStatusService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ChangeStatusService(object):
    """Proto file describing the Change Status service.

    Service to fetch change statuses.
    """

    @staticmethod
    def GetChangeStatus(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/google.ads.googleads.v6.services.ChangeStatusService/GetChangeStatus',
            google_dot_ads_dot_googleads__v6_dot_proto_dot_services_dot_change__status__service__pb2.GetChangeStatusRequest.SerializeToString,
            google_dot_ads_dot_googleads__v6_dot_proto_dot_resources_dot_change__status__pb2.ChangeStatus.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)
