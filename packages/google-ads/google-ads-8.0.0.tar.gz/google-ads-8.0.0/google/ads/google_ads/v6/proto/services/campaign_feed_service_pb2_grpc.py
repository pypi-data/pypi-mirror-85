# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.ads.google_ads.v6.proto.resources import campaign_feed_pb2 as google_dot_ads_dot_googleads__v6_dot_proto_dot_resources_dot_campaign__feed__pb2
from google.ads.google_ads.v6.proto.services import campaign_feed_service_pb2 as google_dot_ads_dot_googleads__v6_dot_proto_dot_services_dot_campaign__feed__service__pb2


class CampaignFeedServiceStub(object):
    """Proto file describing the CampaignFeed service.

    Service to manage campaign feeds.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetCampaignFeed = channel.unary_unary(
                '/google.ads.googleads.v6.services.CampaignFeedService/GetCampaignFeed',
                request_serializer=google_dot_ads_dot_googleads__v6_dot_proto_dot_services_dot_campaign__feed__service__pb2.GetCampaignFeedRequest.SerializeToString,
                response_deserializer=google_dot_ads_dot_googleads__v6_dot_proto_dot_resources_dot_campaign__feed__pb2.CampaignFeed.FromString,
                )
        self.MutateCampaignFeeds = channel.unary_unary(
                '/google.ads.googleads.v6.services.CampaignFeedService/MutateCampaignFeeds',
                request_serializer=google_dot_ads_dot_googleads__v6_dot_proto_dot_services_dot_campaign__feed__service__pb2.MutateCampaignFeedsRequest.SerializeToString,
                response_deserializer=google_dot_ads_dot_googleads__v6_dot_proto_dot_services_dot_campaign__feed__service__pb2.MutateCampaignFeedsResponse.FromString,
                )


class CampaignFeedServiceServicer(object):
    """Proto file describing the CampaignFeed service.

    Service to manage campaign feeds.
    """

    def GetCampaignFeed(self, request, context):
        """Returns the requested campaign feed in full detail.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def MutateCampaignFeeds(self, request, context):
        """Creates, updates, or removes campaign feeds. Operation statuses are
        returned.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_CampaignFeedServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetCampaignFeed': grpc.unary_unary_rpc_method_handler(
                    servicer.GetCampaignFeed,
                    request_deserializer=google_dot_ads_dot_googleads__v6_dot_proto_dot_services_dot_campaign__feed__service__pb2.GetCampaignFeedRequest.FromString,
                    response_serializer=google_dot_ads_dot_googleads__v6_dot_proto_dot_resources_dot_campaign__feed__pb2.CampaignFeed.SerializeToString,
            ),
            'MutateCampaignFeeds': grpc.unary_unary_rpc_method_handler(
                    servicer.MutateCampaignFeeds,
                    request_deserializer=google_dot_ads_dot_googleads__v6_dot_proto_dot_services_dot_campaign__feed__service__pb2.MutateCampaignFeedsRequest.FromString,
                    response_serializer=google_dot_ads_dot_googleads__v6_dot_proto_dot_services_dot_campaign__feed__service__pb2.MutateCampaignFeedsResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'google.ads.googleads.v6.services.CampaignFeedService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class CampaignFeedService(object):
    """Proto file describing the CampaignFeed service.

    Service to manage campaign feeds.
    """

    @staticmethod
    def GetCampaignFeed(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/google.ads.googleads.v6.services.CampaignFeedService/GetCampaignFeed',
            google_dot_ads_dot_googleads__v6_dot_proto_dot_services_dot_campaign__feed__service__pb2.GetCampaignFeedRequest.SerializeToString,
            google_dot_ads_dot_googleads__v6_dot_proto_dot_resources_dot_campaign__feed__pb2.CampaignFeed.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def MutateCampaignFeeds(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/google.ads.googleads.v6.services.CampaignFeedService/MutateCampaignFeeds',
            google_dot_ads_dot_googleads__v6_dot_proto_dot_services_dot_campaign__feed__service__pb2.MutateCampaignFeedsRequest.SerializeToString,
            google_dot_ads_dot_googleads__v6_dot_proto_dot_services_dot_campaign__feed__service__pb2.MutateCampaignFeedsResponse.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)
