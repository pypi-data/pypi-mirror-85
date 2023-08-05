# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from google.ads.google_ads.v3.proto.resources import feed_item_target_pb2 as google_dot_ads_dot_googleads__v3_dot_proto_dot_resources_dot_feed__item__target__pb2
from google.ads.google_ads.v3.proto.services import feed_item_target_service_pb2 as google_dot_ads_dot_googleads__v3_dot_proto_dot_services_dot_feed__item__target__service__pb2


class FeedItemTargetServiceStub(object):
  """Proto file describing the FeedItemTarget service.

  Service to manage feed item targets.
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.GetFeedItemTarget = channel.unary_unary(
        '/google.ads.googleads.v3.services.FeedItemTargetService/GetFeedItemTarget',
        request_serializer=google_dot_ads_dot_googleads__v3_dot_proto_dot_services_dot_feed__item__target__service__pb2.GetFeedItemTargetRequest.SerializeToString,
        response_deserializer=google_dot_ads_dot_googleads__v3_dot_proto_dot_resources_dot_feed__item__target__pb2.FeedItemTarget.FromString,
        )
    self.MutateFeedItemTargets = channel.unary_unary(
        '/google.ads.googleads.v3.services.FeedItemTargetService/MutateFeedItemTargets',
        request_serializer=google_dot_ads_dot_googleads__v3_dot_proto_dot_services_dot_feed__item__target__service__pb2.MutateFeedItemTargetsRequest.SerializeToString,
        response_deserializer=google_dot_ads_dot_googleads__v3_dot_proto_dot_services_dot_feed__item__target__service__pb2.MutateFeedItemTargetsResponse.FromString,
        )


class FeedItemTargetServiceServicer(object):
  """Proto file describing the FeedItemTarget service.

  Service to manage feed item targets.
  """

  def GetFeedItemTarget(self, request, context):
    """Returns the requested feed item targets in full detail.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def MutateFeedItemTargets(self, request, context):
    """Creates or removes feed item targets. Operation statuses are returned.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_FeedItemTargetServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'GetFeedItemTarget': grpc.unary_unary_rpc_method_handler(
          servicer.GetFeedItemTarget,
          request_deserializer=google_dot_ads_dot_googleads__v3_dot_proto_dot_services_dot_feed__item__target__service__pb2.GetFeedItemTargetRequest.FromString,
          response_serializer=google_dot_ads_dot_googleads__v3_dot_proto_dot_resources_dot_feed__item__target__pb2.FeedItemTarget.SerializeToString,
      ),
      'MutateFeedItemTargets': grpc.unary_unary_rpc_method_handler(
          servicer.MutateFeedItemTargets,
          request_deserializer=google_dot_ads_dot_googleads__v3_dot_proto_dot_services_dot_feed__item__target__service__pb2.MutateFeedItemTargetsRequest.FromString,
          response_serializer=google_dot_ads_dot_googleads__v3_dot_proto_dot_services_dot_feed__item__target__service__pb2.MutateFeedItemTargetsResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'google.ads.googleads.v3.services.FeedItemTargetService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
