# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from google.ads.google_ads.v3.proto.resources import remarketing_action_pb2 as google_dot_ads_dot_googleads__v3_dot_proto_dot_resources_dot_remarketing__action__pb2
from google.ads.google_ads.v3.proto.services import remarketing_action_service_pb2 as google_dot_ads_dot_googleads__v3_dot_proto_dot_services_dot_remarketing__action__service__pb2


class RemarketingActionServiceStub(object):
  """Proto file describing the Remarketing Action service.

  Service to manage remarketing actions.
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.GetRemarketingAction = channel.unary_unary(
        '/google.ads.googleads.v3.services.RemarketingActionService/GetRemarketingAction',
        request_serializer=google_dot_ads_dot_googleads__v3_dot_proto_dot_services_dot_remarketing__action__service__pb2.GetRemarketingActionRequest.SerializeToString,
        response_deserializer=google_dot_ads_dot_googleads__v3_dot_proto_dot_resources_dot_remarketing__action__pb2.RemarketingAction.FromString,
        )
    self.MutateRemarketingActions = channel.unary_unary(
        '/google.ads.googleads.v3.services.RemarketingActionService/MutateRemarketingActions',
        request_serializer=google_dot_ads_dot_googleads__v3_dot_proto_dot_services_dot_remarketing__action__service__pb2.MutateRemarketingActionsRequest.SerializeToString,
        response_deserializer=google_dot_ads_dot_googleads__v3_dot_proto_dot_services_dot_remarketing__action__service__pb2.MutateRemarketingActionsResponse.FromString,
        )


class RemarketingActionServiceServicer(object):
  """Proto file describing the Remarketing Action service.

  Service to manage remarketing actions.
  """

  def GetRemarketingAction(self, request, context):
    """Returns the requested remarketing action in full detail.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def MutateRemarketingActions(self, request, context):
    """Creates or updates remarketing actions. Operation statuses are returned.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_RemarketingActionServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'GetRemarketingAction': grpc.unary_unary_rpc_method_handler(
          servicer.GetRemarketingAction,
          request_deserializer=google_dot_ads_dot_googleads__v3_dot_proto_dot_services_dot_remarketing__action__service__pb2.GetRemarketingActionRequest.FromString,
          response_serializer=google_dot_ads_dot_googleads__v3_dot_proto_dot_resources_dot_remarketing__action__pb2.RemarketingAction.SerializeToString,
      ),
      'MutateRemarketingActions': grpc.unary_unary_rpc_method_handler(
          servicer.MutateRemarketingActions,
          request_deserializer=google_dot_ads_dot_googleads__v3_dot_proto_dot_services_dot_remarketing__action__service__pb2.MutateRemarketingActionsRequest.FromString,
          response_serializer=google_dot_ads_dot_googleads__v3_dot_proto_dot_services_dot_remarketing__action__service__pb2.MutateRemarketingActionsResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'google.ads.googleads.v3.services.RemarketingActionService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
