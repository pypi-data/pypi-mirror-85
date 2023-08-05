# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.ads.google_ads.v6.proto.resources import ad_group_criterion_pb2 as google_dot_ads_dot_googleads__v6_dot_proto_dot_resources_dot_ad__group__criterion__pb2
from google.ads.google_ads.v6.proto.services import ad_group_criterion_service_pb2 as google_dot_ads_dot_googleads__v6_dot_proto_dot_services_dot_ad__group__criterion__service__pb2


class AdGroupCriterionServiceStub(object):
    """Proto file describing the Ad Group Criterion service.

    Service to manage ad group criteria.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetAdGroupCriterion = channel.unary_unary(
                '/google.ads.googleads.v6.services.AdGroupCriterionService/GetAdGroupCriterion',
                request_serializer=google_dot_ads_dot_googleads__v6_dot_proto_dot_services_dot_ad__group__criterion__service__pb2.GetAdGroupCriterionRequest.SerializeToString,
                response_deserializer=google_dot_ads_dot_googleads__v6_dot_proto_dot_resources_dot_ad__group__criterion__pb2.AdGroupCriterion.FromString,
                )
        self.MutateAdGroupCriteria = channel.unary_unary(
                '/google.ads.googleads.v6.services.AdGroupCriterionService/MutateAdGroupCriteria',
                request_serializer=google_dot_ads_dot_googleads__v6_dot_proto_dot_services_dot_ad__group__criterion__service__pb2.MutateAdGroupCriteriaRequest.SerializeToString,
                response_deserializer=google_dot_ads_dot_googleads__v6_dot_proto_dot_services_dot_ad__group__criterion__service__pb2.MutateAdGroupCriteriaResponse.FromString,
                )


class AdGroupCriterionServiceServicer(object):
    """Proto file describing the Ad Group Criterion service.

    Service to manage ad group criteria.
    """

    def GetAdGroupCriterion(self, request, context):
        """Returns the requested criterion in full detail.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def MutateAdGroupCriteria(self, request, context):
        """Creates, updates, or removes criteria. Operation statuses are returned.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_AdGroupCriterionServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetAdGroupCriterion': grpc.unary_unary_rpc_method_handler(
                    servicer.GetAdGroupCriterion,
                    request_deserializer=google_dot_ads_dot_googleads__v6_dot_proto_dot_services_dot_ad__group__criterion__service__pb2.GetAdGroupCriterionRequest.FromString,
                    response_serializer=google_dot_ads_dot_googleads__v6_dot_proto_dot_resources_dot_ad__group__criterion__pb2.AdGroupCriterion.SerializeToString,
            ),
            'MutateAdGroupCriteria': grpc.unary_unary_rpc_method_handler(
                    servicer.MutateAdGroupCriteria,
                    request_deserializer=google_dot_ads_dot_googleads__v6_dot_proto_dot_services_dot_ad__group__criterion__service__pb2.MutateAdGroupCriteriaRequest.FromString,
                    response_serializer=google_dot_ads_dot_googleads__v6_dot_proto_dot_services_dot_ad__group__criterion__service__pb2.MutateAdGroupCriteriaResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'google.ads.googleads.v6.services.AdGroupCriterionService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class AdGroupCriterionService(object):
    """Proto file describing the Ad Group Criterion service.

    Service to manage ad group criteria.
    """

    @staticmethod
    def GetAdGroupCriterion(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/google.ads.googleads.v6.services.AdGroupCriterionService/GetAdGroupCriterion',
            google_dot_ads_dot_googleads__v6_dot_proto_dot_services_dot_ad__group__criterion__service__pb2.GetAdGroupCriterionRequest.SerializeToString,
            google_dot_ads_dot_googleads__v6_dot_proto_dot_resources_dot_ad__group__criterion__pb2.AdGroupCriterion.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def MutateAdGroupCriteria(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/google.ads.googleads.v6.services.AdGroupCriterionService/MutateAdGroupCriteria',
            google_dot_ads_dot_googleads__v6_dot_proto_dot_services_dot_ad__group__criterion__service__pb2.MutateAdGroupCriteriaRequest.SerializeToString,
            google_dot_ads_dot_googleads__v6_dot_proto_dot_services_dot_ad__group__criterion__service__pb2.MutateAdGroupCriteriaResponse.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)
