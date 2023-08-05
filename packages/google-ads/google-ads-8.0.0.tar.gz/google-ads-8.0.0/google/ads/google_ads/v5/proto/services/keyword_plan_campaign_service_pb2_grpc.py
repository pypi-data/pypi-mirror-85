# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.ads.google_ads.v5.proto.resources import keyword_plan_campaign_pb2 as google_dot_ads_dot_googleads__v5_dot_proto_dot_resources_dot_keyword__plan__campaign__pb2
from google.ads.google_ads.v5.proto.services import keyword_plan_campaign_service_pb2 as google_dot_ads_dot_googleads__v5_dot_proto_dot_services_dot_keyword__plan__campaign__service__pb2


class KeywordPlanCampaignServiceStub(object):
    """Proto file describing the keyword plan campaign service.

    Service to manage Keyword Plan campaigns.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetKeywordPlanCampaign = channel.unary_unary(
                '/google.ads.googleads.v5.services.KeywordPlanCampaignService/GetKeywordPlanCampaign',
                request_serializer=google_dot_ads_dot_googleads__v5_dot_proto_dot_services_dot_keyword__plan__campaign__service__pb2.GetKeywordPlanCampaignRequest.SerializeToString,
                response_deserializer=google_dot_ads_dot_googleads__v5_dot_proto_dot_resources_dot_keyword__plan__campaign__pb2.KeywordPlanCampaign.FromString,
                )
        self.MutateKeywordPlanCampaigns = channel.unary_unary(
                '/google.ads.googleads.v5.services.KeywordPlanCampaignService/MutateKeywordPlanCampaigns',
                request_serializer=google_dot_ads_dot_googleads__v5_dot_proto_dot_services_dot_keyword__plan__campaign__service__pb2.MutateKeywordPlanCampaignsRequest.SerializeToString,
                response_deserializer=google_dot_ads_dot_googleads__v5_dot_proto_dot_services_dot_keyword__plan__campaign__service__pb2.MutateKeywordPlanCampaignsResponse.FromString,
                )


class KeywordPlanCampaignServiceServicer(object):
    """Proto file describing the keyword plan campaign service.

    Service to manage Keyword Plan campaigns.
    """

    def GetKeywordPlanCampaign(self, request, context):
        """Returns the requested Keyword Plan campaign in full detail.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def MutateKeywordPlanCampaigns(self, request, context):
        """Creates, updates, or removes Keyword Plan campaigns. Operation statuses are
        returned.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_KeywordPlanCampaignServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetKeywordPlanCampaign': grpc.unary_unary_rpc_method_handler(
                    servicer.GetKeywordPlanCampaign,
                    request_deserializer=google_dot_ads_dot_googleads__v5_dot_proto_dot_services_dot_keyword__plan__campaign__service__pb2.GetKeywordPlanCampaignRequest.FromString,
                    response_serializer=google_dot_ads_dot_googleads__v5_dot_proto_dot_resources_dot_keyword__plan__campaign__pb2.KeywordPlanCampaign.SerializeToString,
            ),
            'MutateKeywordPlanCampaigns': grpc.unary_unary_rpc_method_handler(
                    servicer.MutateKeywordPlanCampaigns,
                    request_deserializer=google_dot_ads_dot_googleads__v5_dot_proto_dot_services_dot_keyword__plan__campaign__service__pb2.MutateKeywordPlanCampaignsRequest.FromString,
                    response_serializer=google_dot_ads_dot_googleads__v5_dot_proto_dot_services_dot_keyword__plan__campaign__service__pb2.MutateKeywordPlanCampaignsResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'google.ads.googleads.v5.services.KeywordPlanCampaignService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class KeywordPlanCampaignService(object):
    """Proto file describing the keyword plan campaign service.

    Service to manage Keyword Plan campaigns.
    """

    @staticmethod
    def GetKeywordPlanCampaign(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/google.ads.googleads.v5.services.KeywordPlanCampaignService/GetKeywordPlanCampaign',
            google_dot_ads_dot_googleads__v5_dot_proto_dot_services_dot_keyword__plan__campaign__service__pb2.GetKeywordPlanCampaignRequest.SerializeToString,
            google_dot_ads_dot_googleads__v5_dot_proto_dot_resources_dot_keyword__plan__campaign__pb2.KeywordPlanCampaign.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def MutateKeywordPlanCampaigns(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/google.ads.googleads.v5.services.KeywordPlanCampaignService/MutateKeywordPlanCampaigns',
            google_dot_ads_dot_googleads__v5_dot_proto_dot_services_dot_keyword__plan__campaign__service__pb2.MutateKeywordPlanCampaignsRequest.SerializeToString,
            google_dot_ads_dot_googleads__v5_dot_proto_dot_services_dot_keyword__plan__campaign__service__pb2.MutateKeywordPlanCampaignsResponse.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)
