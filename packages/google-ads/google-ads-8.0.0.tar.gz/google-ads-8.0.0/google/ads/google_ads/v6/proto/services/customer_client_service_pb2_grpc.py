# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.ads.google_ads.v6.proto.resources import customer_client_pb2 as google_dot_ads_dot_googleads__v6_dot_proto_dot_resources_dot_customer__client__pb2
from google.ads.google_ads.v6.proto.services import customer_client_service_pb2 as google_dot_ads_dot_googleads__v6_dot_proto_dot_services_dot_customer__client__service__pb2


class CustomerClientServiceStub(object):
    """Proto file describing the Customer Client service.

    Service to get clients in a customer's hierarchy.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetCustomerClient = channel.unary_unary(
                '/google.ads.googleads.v6.services.CustomerClientService/GetCustomerClient',
                request_serializer=google_dot_ads_dot_googleads__v6_dot_proto_dot_services_dot_customer__client__service__pb2.GetCustomerClientRequest.SerializeToString,
                response_deserializer=google_dot_ads_dot_googleads__v6_dot_proto_dot_resources_dot_customer__client__pb2.CustomerClient.FromString,
                )


class CustomerClientServiceServicer(object):
    """Proto file describing the Customer Client service.

    Service to get clients in a customer's hierarchy.
    """

    def GetCustomerClient(self, request, context):
        """Returns the requested client in full detail.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_CustomerClientServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetCustomerClient': grpc.unary_unary_rpc_method_handler(
                    servicer.GetCustomerClient,
                    request_deserializer=google_dot_ads_dot_googleads__v6_dot_proto_dot_services_dot_customer__client__service__pb2.GetCustomerClientRequest.FromString,
                    response_serializer=google_dot_ads_dot_googleads__v6_dot_proto_dot_resources_dot_customer__client__pb2.CustomerClient.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'google.ads.googleads.v6.services.CustomerClientService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class CustomerClientService(object):
    """Proto file describing the Customer Client service.

    Service to get clients in a customer's hierarchy.
    """

    @staticmethod
    def GetCustomerClient(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/google.ads.googleads.v6.services.CustomerClientService/GetCustomerClient',
            google_dot_ads_dot_googleads__v6_dot_proto_dot_services_dot_customer__client__service__pb2.GetCustomerClientRequest.SerializeToString,
            google_dot_ads_dot_googleads__v6_dot_proto_dot_resources_dot_customer__client__pb2.CustomerClient.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)
