# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from . import otg_pb2 as otg__pb2


class OpenapiStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetConfig = channel.unary_unary(
                '/otg.Openapi/GetConfig',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=otg__pb2.Config.FromString,
                )
        self.SetConfig = channel.unary_unary(
                '/otg.Openapi/SetConfig',
                request_serializer=otg__pb2.SetConfigParameters.SerializeToString,
                response_deserializer=otg__pb2.Details.FromString,
                )
        self.UpdateConfig = channel.unary_unary(
                '/otg.Openapi/UpdateConfig',
                request_serializer=otg__pb2.UpdateConfigParameters.SerializeToString,
                response_deserializer=otg__pb2.Details.FromString,
                )
        self.SetTransmitState = channel.unary_unary(
                '/otg.Openapi/SetTransmitState',
                request_serializer=otg__pb2.SetTransmitStateParameters.SerializeToString,
                response_deserializer=otg__pb2.Details.FromString,
                )
        self.SetLinkState = channel.unary_unary(
                '/otg.Openapi/SetLinkState',
                request_serializer=otg__pb2.SetLinkStateParameters.SerializeToString,
                response_deserializer=otg__pb2.Details.FromString,
                )
        self.SetCaptureState = channel.unary_unary(
                '/otg.Openapi/SetCaptureState',
                request_serializer=otg__pb2.SetCaptureStateParameters.SerializeToString,
                response_deserializer=otg__pb2.Details.FromString,
                )
        self.GetMetrics = channel.unary_unary(
                '/otg.Openapi/GetMetrics',
                request_serializer=otg__pb2.GetMetricsParameters.SerializeToString,
                response_deserializer=otg__pb2.MetricsResponse.FromString,
                )
        self.GetStateMetrics = channel.unary_unary(
                '/otg.Openapi/GetStateMetrics',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=otg__pb2.StateMetrics.FromString,
                )
        self.GetCapabilities = channel.unary_unary(
                '/otg.Openapi/GetCapabilities',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=otg__pb2.Capabilities.FromString,
                )
        self.GetCapture = channel.unary_unary(
                '/otg.Openapi/GetCapture',
                request_serializer=otg__pb2.GetCaptureParameters.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )


class OpenapiServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetConfig(self, request, context):
        """option (google.api.http) = { get:"/config"  };
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetConfig(self, request, context):
        """option (google.api.http) = { post:"/config"  };
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateConfig(self, request, context):
        """option (google.api.http) = { patch:"/config"  };
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetTransmitState(self, request, context):
        """option (google.api.http) = { post:"/control/transmit"  };
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetLinkState(self, request, context):
        """option (google.api.http) = { post:"/control/link"  };
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetCaptureState(self, request, context):
        """option (google.api.http) = { post:"/control/capture"  };
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetMetrics(self, request, context):
        """option (google.api.http) = { post:"/results/metrics"  };
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetStateMetrics(self, request, context):
        """option (google.api.http) = { post:"/results/state"  };
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetCapabilities(self, request, context):
        """option (google.api.http) = { post:"/results/capabilities"  };
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetCapture(self, request, context):
        """option (google.api.http) = { post:"/results/capture"  };
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_OpenapiServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetConfig': grpc.unary_unary_rpc_method_handler(
                    servicer.GetConfig,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=otg__pb2.Config.SerializeToString,
            ),
            'SetConfig': grpc.unary_unary_rpc_method_handler(
                    servicer.SetConfig,
                    request_deserializer=otg__pb2.SetConfigParameters.FromString,
                    response_serializer=otg__pb2.Details.SerializeToString,
            ),
            'UpdateConfig': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateConfig,
                    request_deserializer=otg__pb2.UpdateConfigParameters.FromString,
                    response_serializer=otg__pb2.Details.SerializeToString,
            ),
            'SetTransmitState': grpc.unary_unary_rpc_method_handler(
                    servicer.SetTransmitState,
                    request_deserializer=otg__pb2.SetTransmitStateParameters.FromString,
                    response_serializer=otg__pb2.Details.SerializeToString,
            ),
            'SetLinkState': grpc.unary_unary_rpc_method_handler(
                    servicer.SetLinkState,
                    request_deserializer=otg__pb2.SetLinkStateParameters.FromString,
                    response_serializer=otg__pb2.Details.SerializeToString,
            ),
            'SetCaptureState': grpc.unary_unary_rpc_method_handler(
                    servicer.SetCaptureState,
                    request_deserializer=otg__pb2.SetCaptureStateParameters.FromString,
                    response_serializer=otg__pb2.Details.SerializeToString,
            ),
            'GetMetrics': grpc.unary_unary_rpc_method_handler(
                    servicer.GetMetrics,
                    request_deserializer=otg__pb2.GetMetricsParameters.FromString,
                    response_serializer=otg__pb2.MetricsResponse.SerializeToString,
            ),
            'GetStateMetrics': grpc.unary_unary_rpc_method_handler(
                    servicer.GetStateMetrics,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=otg__pb2.StateMetrics.SerializeToString,
            ),
            'GetCapabilities': grpc.unary_unary_rpc_method_handler(
                    servicer.GetCapabilities,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=otg__pb2.Capabilities.SerializeToString,
            ),
            'GetCapture': grpc.unary_unary_rpc_method_handler(
                    servicer.GetCapture,
                    request_deserializer=otg__pb2.GetCaptureParameters.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'otg.Openapi', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Openapi(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetConfig(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/otg.Openapi/GetConfig',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            otg__pb2.Config.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SetConfig(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/otg.Openapi/SetConfig',
            otg__pb2.SetConfigParameters.SerializeToString,
            otg__pb2.Details.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateConfig(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/otg.Openapi/UpdateConfig',
            otg__pb2.UpdateConfigParameters.SerializeToString,
            otg__pb2.Details.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SetTransmitState(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/otg.Openapi/SetTransmitState',
            otg__pb2.SetTransmitStateParameters.SerializeToString,
            otg__pb2.Details.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SetLinkState(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/otg.Openapi/SetLinkState',
            otg__pb2.SetLinkStateParameters.SerializeToString,
            otg__pb2.Details.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SetCaptureState(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/otg.Openapi/SetCaptureState',
            otg__pb2.SetCaptureStateParameters.SerializeToString,
            otg__pb2.Details.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetMetrics(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/otg.Openapi/GetMetrics',
            otg__pb2.GetMetricsParameters.SerializeToString,
            otg__pb2.MetricsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetStateMetrics(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/otg.Openapi/GetStateMetrics',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            otg__pb2.StateMetrics.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetCapabilities(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/otg.Openapi/GetCapabilities',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            otg__pb2.Capabilities.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetCapture(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/otg.Openapi/GetCapture',
            otg__pb2.GetCaptureParameters.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
