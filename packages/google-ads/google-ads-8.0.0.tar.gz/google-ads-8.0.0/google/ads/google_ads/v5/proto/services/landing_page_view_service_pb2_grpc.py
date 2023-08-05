# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.ads.google_ads.v5.proto.resources import landing_page_view_pb2 as google_dot_ads_dot_googleads__v5_dot_proto_dot_resources_dot_landing__page__view__pb2
from google.ads.google_ads.v5.proto.services import landing_page_view_service_pb2 as google_dot_ads_dot_googleads__v5_dot_proto_dot_services_dot_landing__page__view__service__pb2


class LandingPageViewServiceStub(object):
    """Proto file describing the landing page view service.

    Service to fetch landing page views.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetLandingPageView = channel.unary_unary(
                '/google.ads.googleads.v5.services.LandingPageViewService/GetLandingPageView',
                request_serializer=google_dot_ads_dot_googleads__v5_dot_proto_dot_services_dot_landing__page__view__service__pb2.GetLandingPageViewRequest.SerializeToString,
                response_deserializer=google_dot_ads_dot_googleads__v5_dot_proto_dot_resources_dot_landing__page__view__pb2.LandingPageView.FromString,
                )


class LandingPageViewServiceServicer(object):
    """Proto file describing the landing page view service.

    Service to fetch landing page views.
    """

    def GetLandingPageView(self, request, context):
        """Returns the requested landing page view in full detail.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_LandingPageViewServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetLandingPageView': grpc.unary_unary_rpc_method_handler(
                    servicer.GetLandingPageView,
                    request_deserializer=google_dot_ads_dot_googleads__v5_dot_proto_dot_services_dot_landing__page__view__service__pb2.GetLandingPageViewRequest.FromString,
                    response_serializer=google_dot_ads_dot_googleads__v5_dot_proto_dot_resources_dot_landing__page__view__pb2.LandingPageView.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'google.ads.googleads.v5.services.LandingPageViewService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class LandingPageViewService(object):
    """Proto file describing the landing page view service.

    Service to fetch landing page views.
    """

    @staticmethod
    def GetLandingPageView(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/google.ads.googleads.v5.services.LandingPageViewService/GetLandingPageView',
            google_dot_ads_dot_googleads__v5_dot_proto_dot_services_dot_landing__page__view__service__pb2.GetLandingPageViewRequest.SerializeToString,
            google_dot_ads_dot_googleads__v5_dot_proto_dot_resources_dot_landing__page__view__pb2.LandingPageView.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)
