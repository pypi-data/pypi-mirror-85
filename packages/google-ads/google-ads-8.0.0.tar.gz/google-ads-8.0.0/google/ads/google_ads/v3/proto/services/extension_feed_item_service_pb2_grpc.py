# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from google.ads.google_ads.v3.proto.resources import extension_feed_item_pb2 as google_dot_ads_dot_googleads__v3_dot_proto_dot_resources_dot_extension__feed__item__pb2
from google.ads.google_ads.v3.proto.services import extension_feed_item_service_pb2 as google_dot_ads_dot_googleads__v3_dot_proto_dot_services_dot_extension__feed__item__service__pb2


class ExtensionFeedItemServiceStub(object):
  """Proto file describing the ExtensionFeedItem service.

  Service to manage extension feed items.
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.GetExtensionFeedItem = channel.unary_unary(
        '/google.ads.googleads.v3.services.ExtensionFeedItemService/GetExtensionFeedItem',
        request_serializer=google_dot_ads_dot_googleads__v3_dot_proto_dot_services_dot_extension__feed__item__service__pb2.GetExtensionFeedItemRequest.SerializeToString,
        response_deserializer=google_dot_ads_dot_googleads__v3_dot_proto_dot_resources_dot_extension__feed__item__pb2.ExtensionFeedItem.FromString,
        )
    self.MutateExtensionFeedItems = channel.unary_unary(
        '/google.ads.googleads.v3.services.ExtensionFeedItemService/MutateExtensionFeedItems',
        request_serializer=google_dot_ads_dot_googleads__v3_dot_proto_dot_services_dot_extension__feed__item__service__pb2.MutateExtensionFeedItemsRequest.SerializeToString,
        response_deserializer=google_dot_ads_dot_googleads__v3_dot_proto_dot_services_dot_extension__feed__item__service__pb2.MutateExtensionFeedItemsResponse.FromString,
        )


class ExtensionFeedItemServiceServicer(object):
  """Proto file describing the ExtensionFeedItem service.

  Service to manage extension feed items.
  """

  def GetExtensionFeedItem(self, request, context):
    """Returns the requested extension feed item in full detail.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def MutateExtensionFeedItems(self, request, context):
    """Creates, updates, or removes extension feed items. Operation
    statuses are returned.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_ExtensionFeedItemServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'GetExtensionFeedItem': grpc.unary_unary_rpc_method_handler(
          servicer.GetExtensionFeedItem,
          request_deserializer=google_dot_ads_dot_googleads__v3_dot_proto_dot_services_dot_extension__feed__item__service__pb2.GetExtensionFeedItemRequest.FromString,
          response_serializer=google_dot_ads_dot_googleads__v3_dot_proto_dot_resources_dot_extension__feed__item__pb2.ExtensionFeedItem.SerializeToString,
      ),
      'MutateExtensionFeedItems': grpc.unary_unary_rpc_method_handler(
          servicer.MutateExtensionFeedItems,
          request_deserializer=google_dot_ads_dot_googleads__v3_dot_proto_dot_services_dot_extension__feed__item__service__pb2.MutateExtensionFeedItemsRequest.FromString,
          response_serializer=google_dot_ads_dot_googleads__v3_dot_proto_dot_services_dot_extension__feed__item__service__pb2.MutateExtensionFeedItemsResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'google.ads.googleads.v3.services.ExtensionFeedItemService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
