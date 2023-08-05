# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.ads.google_ads.v5.proto.resources import ad_group_criterion_label_pb2 as google_dot_ads_dot_googleads__v5_dot_proto_dot_resources_dot_ad__group__criterion__label__pb2
from google.ads.google_ads.v5.proto.services import ad_group_criterion_label_service_pb2 as google_dot_ads_dot_googleads__v5_dot_proto_dot_services_dot_ad__group__criterion__label__service__pb2


class AdGroupCriterionLabelServiceStub(object):
    """Proto file describing the Ad Group Criterion Label service.

    Service to manage labels on ad group criteria.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetAdGroupCriterionLabel = channel.unary_unary(
                '/google.ads.googleads.v5.services.AdGroupCriterionLabelService/GetAdGroupCriterionLabel',
                request_serializer=google_dot_ads_dot_googleads__v5_dot_proto_dot_services_dot_ad__group__criterion__label__service__pb2.GetAdGroupCriterionLabelRequest.SerializeToString,
                response_deserializer=google_dot_ads_dot_googleads__v5_dot_proto_dot_resources_dot_ad__group__criterion__label__pb2.AdGroupCriterionLabel.FromString,
                )
        self.MutateAdGroupCriterionLabels = channel.unary_unary(
                '/google.ads.googleads.v5.services.AdGroupCriterionLabelService/MutateAdGroupCriterionLabels',
                request_serializer=google_dot_ads_dot_googleads__v5_dot_proto_dot_services_dot_ad__group__criterion__label__service__pb2.MutateAdGroupCriterionLabelsRequest.SerializeToString,
                response_deserializer=google_dot_ads_dot_googleads__v5_dot_proto_dot_services_dot_ad__group__criterion__label__service__pb2.MutateAdGroupCriterionLabelsResponse.FromString,
                )


class AdGroupCriterionLabelServiceServicer(object):
    """Proto file describing the Ad Group Criterion Label service.

    Service to manage labels on ad group criteria.
    """

    def GetAdGroupCriterionLabel(self, request, context):
        """Returns the requested ad group criterion label in full detail.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def MutateAdGroupCriterionLabels(self, request, context):
        """Creates and removes ad group criterion labels.
        Operation statuses are returned.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_AdGroupCriterionLabelServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetAdGroupCriterionLabel': grpc.unary_unary_rpc_method_handler(
                    servicer.GetAdGroupCriterionLabel,
                    request_deserializer=google_dot_ads_dot_googleads__v5_dot_proto_dot_services_dot_ad__group__criterion__label__service__pb2.GetAdGroupCriterionLabelRequest.FromString,
                    response_serializer=google_dot_ads_dot_googleads__v5_dot_proto_dot_resources_dot_ad__group__criterion__label__pb2.AdGroupCriterionLabel.SerializeToString,
            ),
            'MutateAdGroupCriterionLabels': grpc.unary_unary_rpc_method_handler(
                    servicer.MutateAdGroupCriterionLabels,
                    request_deserializer=google_dot_ads_dot_googleads__v5_dot_proto_dot_services_dot_ad__group__criterion__label__service__pb2.MutateAdGroupCriterionLabelsRequest.FromString,
                    response_serializer=google_dot_ads_dot_googleads__v5_dot_proto_dot_services_dot_ad__group__criterion__label__service__pb2.MutateAdGroupCriterionLabelsResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'google.ads.googleads.v5.services.AdGroupCriterionLabelService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class AdGroupCriterionLabelService(object):
    """Proto file describing the Ad Group Criterion Label service.

    Service to manage labels on ad group criteria.
    """

    @staticmethod
    def GetAdGroupCriterionLabel(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/google.ads.googleads.v5.services.AdGroupCriterionLabelService/GetAdGroupCriterionLabel',
            google_dot_ads_dot_googleads__v5_dot_proto_dot_services_dot_ad__group__criterion__label__service__pb2.GetAdGroupCriterionLabelRequest.SerializeToString,
            google_dot_ads_dot_googleads__v5_dot_proto_dot_resources_dot_ad__group__criterion__label__pb2.AdGroupCriterionLabel.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def MutateAdGroupCriterionLabels(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/google.ads.googleads.v5.services.AdGroupCriterionLabelService/MutateAdGroupCriterionLabels',
            google_dot_ads_dot_googleads__v5_dot_proto_dot_services_dot_ad__group__criterion__label__service__pb2.MutateAdGroupCriterionLabelsRequest.SerializeToString,
            google_dot_ads_dot_googleads__v5_dot_proto_dot_services_dot_ad__group__criterion__label__service__pb2.MutateAdGroupCriterionLabelsResponse.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)
