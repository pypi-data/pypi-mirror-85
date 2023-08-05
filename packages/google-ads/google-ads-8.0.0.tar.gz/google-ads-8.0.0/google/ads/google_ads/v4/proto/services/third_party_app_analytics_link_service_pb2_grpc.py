# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from google.ads.google_ads.v4.proto.resources import third_party_app_analytics_link_pb2 as google_dot_ads_dot_googleads__v4_dot_proto_dot_resources_dot_third__party__app__analytics__link__pb2
from google.ads.google_ads.v4.proto.services import third_party_app_analytics_link_service_pb2 as google_dot_ads_dot_googleads__v4_dot_proto_dot_services_dot_third__party__app__analytics__link__service__pb2


class ThirdPartyAppAnalyticsLinkServiceStub(object):
  """This service allows management of links between Google Ads and third party
  app analytics.
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.GetThirdPartyAppAnalyticsLink = channel.unary_unary(
        '/google.ads.googleads.v4.services.ThirdPartyAppAnalyticsLinkService/GetThirdPartyAppAnalyticsLink',
        request_serializer=google_dot_ads_dot_googleads__v4_dot_proto_dot_services_dot_third__party__app__analytics__link__service__pb2.GetThirdPartyAppAnalyticsLinkRequest.SerializeToString,
        response_deserializer=google_dot_ads_dot_googleads__v4_dot_proto_dot_resources_dot_third__party__app__analytics__link__pb2.ThirdPartyAppAnalyticsLink.FromString,
        )


class ThirdPartyAppAnalyticsLinkServiceServicer(object):
  """This service allows management of links between Google Ads and third party
  app analytics.
  """

  def GetThirdPartyAppAnalyticsLink(self, request, context):
    """Returns the third party app analytics link in full detail.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_ThirdPartyAppAnalyticsLinkServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'GetThirdPartyAppAnalyticsLink': grpc.unary_unary_rpc_method_handler(
          servicer.GetThirdPartyAppAnalyticsLink,
          request_deserializer=google_dot_ads_dot_googleads__v4_dot_proto_dot_services_dot_third__party__app__analytics__link__service__pb2.GetThirdPartyAppAnalyticsLinkRequest.FromString,
          response_serializer=google_dot_ads_dot_googleads__v4_dot_proto_dot_resources_dot_third__party__app__analytics__link__pb2.ThirdPartyAppAnalyticsLink.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'google.ads.googleads.v4.services.ThirdPartyAppAnalyticsLinkService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
