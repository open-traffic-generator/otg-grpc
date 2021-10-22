# Python implementation of gRPC Server
import argparse
import logging
from concurrent import futures

# gRPC stuffs
import grpc
# signal for SIGTERM
import signal
# snappi
import snappi
# datetime
import datetime
from google.protobuf import json_format

from .autogen import snappipb_pb2, snappipb_pb2_grpc
from .common.utils import get_error_details, init_logging, get_time_elapsed

# set API version
OTG_API_Version = "0.6.6"

server = None


class Openapi(snappipb_pb2_grpc.OpenapiServicer):

    def __init__(self, args):
        super().__init__()

        self.logger = logging.getLogger(args.logfile)

        self.app_mode = args.app_mode
        self.target_address = "{}:{}".format(
            args.target_host,
            args.target_port
        )
        self.api_initialized = False

        self.snappi_log_level = logging.INFO
        if args.log_debug:
            self.snappi_log_level = logging.DEBUG

    def InitSanppi(self):
        # for snappi
        init_snappi_start = datetime.datetime.now()
        try:
            if not self.api_initialized:
                if self.app_mode == 'ixnetwork':
                    target = "http://{}".format(self.target_address)
                    self.api = snappi.api(
                        location=target,
                        ext=self.app_mode,
                        verify=False,
                        loglevel=self.snappi_log_level
                    )
                    self.logger.info(
                        "Snappi Remote Server address = {} in IxNetwork mode".format(target)) # noqa
                elif self.app_mode == "athena-insecure":
                    target = "http://{}".format(self.target_address)
                    self.api = snappi.api(
                        location=target,
                        verify=False
                    )
                    self.logger.info(
                        "Snappi Remote Server address = {} in Athena mode".format(target)) # noqa
                else:
                    target = "https://{}".format(self.target_address)
                    self.api = snappi.api(
                        location=target,
                        verify=False,
                        loglevel=self.snappi_log_level
                    )
                    self.logger.info(
                        "Snappi Remote Server address = {} in Athena mode".format(target)) # noqa

                self.api_initialized = True
                self.logger.info('Snappi initialized')
        finally:
            self.logger.info(
                "InitSanppi took {} ns".format(
                    get_time_elapsed(init_snappi_start)
                )
            )

    def SetConfig(self, request, context):
        grpc_api_start = datetime.datetime.now()
        try:
            jsonObj = json_format.MessageToJson(
                request.config,
                including_default_value_fields=False,
                preserving_proto_field_name=True
            )
            self.logger.debug(
                "Received request.config (JSON)(default=False) = {}".format(
                    jsonObj
                )
            )

            self.InitSanppi()

            self.logger.info("Requesting set_config ...")
            try:
                snappi_api_start = datetime.datetime.now()
                response = self.api.set_config(jsonObj)
                self.logger.info(
                    "Snappi_api-SetConfig took {} ns".format(
                        get_time_elapsed(snappi_api_start)
                    )
                )
                response_200 = """
                {
                    "status_code_200" : {
                        "warnings" : []
                    }
                }
                """
                config_response = json_format.Parse(
                    response_200,
                    snappipb_pb2.SetConfigResponse()
                )
                if len(response.warnings) > 0:
                    config_response.status_code_200.warnings.extend(response.warnings) # noqa
                    self.logger.debug(
                        "Snappi_api Setconfig Returned Warnings: {}".format(
                            response.warnings))
                else:
                    self.logger.debug(
                        "Snappi_api Setconfig Returned without any Warnings")
                self.logger.debug("Returning status_code_200 to client ...")
                return config_response

            except Exception as e:
                self.logger.info(
                    "Snappi_api-SetConfig took {} ns".format(
                        get_time_elapsed(snappi_api_start)
                    )
                )
                response_400 = """
                {
                    "status_code_400" : {
                        "errors" : []
                    }
                }
                """
                response_500 = """
                {
                    "status_code_500" : {
                        "errors" : []
                    }
                }
                """
                self.logger.error(
                    "Snappi_api Setconfig Returned Exception :  {}".format(
                        repr(e)))
                if e is ConnectionError:
                    config_response = json_format.Parse(
                        response_500, snappipb_pb2.SetConfigResponse())
                    config_response.status_code_500.errors.extend(e.details) # noqa
                    self.logger.debug(
                        "Returning status_code_500 to client ...")
                    return config_response

                error_code, error_details = get_error_details(e)

                if error_code == 400:
                    config_response = json_format.Parse(
                        response_400, snappipb_pb2.SetConfigResponse())
                    config_response.status_code_400.errors.extend(error_details) # noqa
                    self.logger.debug(
                        "Returning status_code_400 to client ...")
                    return config_response
                elif error_code == 500:
                    config_response = json_format.Parse(
                        response_500, snappipb_pb2.SetConfigResponse())
                    config_response.status_code_500.errors.extend(error_details) # noqa
                    self.logger.debug(
                        "Returning status_code_500 to client ...")
                    return config_response
                else:
                    raise NotImplementedError()
        finally:
            self.logger.info(
                "gRPC-SetConfig took {} ns".format(
                    get_time_elapsed(grpc_api_start)
                )
            )

    def GetConfig(self, request, context):
        grpc_api_start = datetime.datetime.now()
        try:
            self.InitSanppi()
            self.logger.info("Requesting get_config ...")
            try:
                snappi_api_start = datetime.datetime.now()
                response = self.api.get_config()
                self.logger.info(
                    "Snappi_api-GetConfig took {} ns".format(
                        get_time_elapsed(snappi_api_start)
                    )
                )
                self.logger.debug("Snappi_api GetConfig Returned : {}".format(
                    response))

                config_proto = json_format.Parse(
                    response.serialize(),
                    snappipb_pb2.Config()
                )
                config_response = snappipb_pb2.GetConfigResponse(
                    status_code_200=config_proto
                )
                self.logger.debug("Returning config to client ...")
                return config_response

            except Exception as e:
                self.logger.info(
                    "Snappi_api-GetConfig took {} ns".format(
                        get_time_elapsed(snappi_api_start)
                    )
                )
                response_400 = """
                {
                    "status_code_400" : {
                        "errors" : []
                    }
                }
                """
                response_500 = """
                {
                    "status_code_500" : {
                        "errors" : []
                    }
                }
                """
                self.logger.error(
                    "Snappi_api Getconfig Returned Exception :  {}".format(
                        repr(e)))
                error_code, error_details = get_error_details(e)

                if error_code == 400:
                    config_response = json_format.Parse(
                        response_400,
                        snappipb_pb2.GetConfigResponse()
                    )
                    config_response.status_code_400.errors.extend(error_details) # noqa
                    return config_response
                elif error_code == 500:
                    config_response = json_format.Parse(
                        response_500,
                        snappipb_pb2.GetConfigResponse()
                    )
                    config_response.status_code_500.errors.extend(error_details) # noqa
                    return config_response
                else:
                    raise NotImplementedError()

        finally:
            self.logger.info(
                "gRPC-GetConfig took {} ns".format(
                    get_time_elapsed(grpc_api_start)
                )
            )

    def SetLinkState(self, request, context):
        grpc_api_start = datetime.datetime.now()
        try:
            jsonObj = json_format.MessageToJson(
                request.link_state,
                preserving_proto_field_name=True
            )
            self.logger.debug(
                "Received request.linkstate (JSON) = {}".format(
                    jsonObj
                )
            )

            self.InitSanppi()

            self.logger.info("Requesting SetLinkState ...")
            try:
                snappi_api_start = datetime.datetime.now()
                response = self.api.set_link_state(jsonObj)
                self.logger.info(
                    "Snappi_api-SetLinkState took {} ns".format(
                        get_time_elapsed(snappi_api_start)
                    )
                )
                response_200 = """
                {
                    "status_code_200" : {
                        "warnings" : []
                    }
                }
                """
                link_state_response = json_format.Parse(
                    response_200,
                    snappipb_pb2.SetLinkStateResponse()
                )
                if len(response.warnings) > 0:
                    link_state_response.status_code_200.warnings.extend(response.warnings) # noqa
                    self.logger.debug(
                        "Snappi_api set_link_state Returned Warnings: {}".format( # noqa
                            response.warnings
                        )
                    )
                self.logger.debug("Returning status_code_200 to client ...")
                return link_state_response

            except Exception as e:
                self.logger.info(
                    "Snappi_api-SetLinkState took {} ns".format(
                        get_time_elapsed(snappi_api_start)
                    )
                )
                response_400 = """
                {
                    "status_code_400" : {
                        "errors" : []
                    }
                }
                """
                response_500 = """
                {
                    "status_code_500" : {
                        "errors" : []
                    }
                }
                """
                self.logger.error(
                    "Snappi_api set_link_state Returned Exception :  {}".format( # noqa
                        repr(e)
                    )
                )
                error_code, error_details = get_error_details(e)

                if error_code == 400:
                    link_state_response = json_format.Parse(
                        response_400,
                        snappipb_pb2.SetLinkStateResponse()
                    )
                    link_state_response.status_code_400.errors.extend(error_details) # noqa
                    return link_state_response
                elif error_code == 500:
                    link_state_response = json_format.Parse(
                        response_500,
                        snappipb_pb2.SetLinkStateResponse()
                    )
                    link_state_response.status_code_500.errors.extend(error_details) # noqa
                    return link_state_response
                else:
                    raise NotImplementedError()
        finally:
            self.logger.info(
                "gRPC-SetLinkState took {} ns".format(
                    get_time_elapsed(grpc_api_start)
                )
            )

    def SetTransmitState(self, request, context):
        grpc_api_start = datetime.datetime.now()
        try:
            jsonObj = json_format.MessageToJson(
                request.transmit_state,
                preserving_proto_field_name=True
            )
            self.logger.debug(
                "Received request.transmitstate (JSON)(default=False) = {}".format( # noqa
                    jsonObj
                )
            )

            self.InitSanppi()

            self.logger.info("Requesting SetTransmitState ...")
            try:
                snappi_api_start = datetime.datetime.now()
                self.logger.info(
                    "Snappi_api-SetTransmitState took {} ns".format(
                        get_time_elapsed(snappi_api_start)
                    )
                )
                response = self.api.set_transmit_state(jsonObj)
                response_200 = """
                {
                    "status_code_200" : {
                        "warnings" : []
                    }
                }
                """
                transmit_response = json_format.Parse(
                    response_200,
                    snappipb_pb2.SetTransmitStateResponse()
                )
                if len(response.warnings) > 0:
                    transmit_response.status_code_200.warnings.extend(response.warnings) # noqa
                    self.logger.debug(
                        "Snappi_api SetTransmitState Returned Warnings: {}".format( # noqa
                            response.warnings
                        )
                    )
                self.logger.debug("Returning status_code_200 to client ...")
                return transmit_response

            except Exception as e:
                self.logger.info(
                    "Snappi_api-SetTransmitState took {} ns".format(
                        get_time_elapsed(snappi_api_start)
                    )
                )
                response_400 = """
                {
                    "status_code_400" : {
                        "errors" : []
                    }
                }
                """
                response_500 = """
                {
                    "status_code_500" : {
                        "errors" : []
                    }
                }
                """
                self.logger.error(
                    "Snappi_api SetTransmitState Returned Exception : {}".format( # noqa
                        repr(e)
                    )
                )
                error_code, error_details = get_error_details(e)
                if error_code == 400:
                    transmit_response = json_format.Parse(
                        response_400,
                        snappipb_pb2.SetTransmitStateResponse()
                    )
                    transmit_response.status_code_400.errors.extend(error_details) # noqa
                    return transmit_response
                elif error_code == 500:
                    transmit_response = json_format.Parse(
                        response_500,
                        snappipb_pb2.SetTransmitStateResponse()
                    )
                    transmit_response.status_code_500.errors.extend(error_details) # noqa
                    return transmit_response
                else:
                    raise NotImplementedError()

        finally:
            self.logger.info(
                "gRPC-SetTransmitState took {} ns".format(
                    get_time_elapsed(grpc_api_start)
                )
            )

    def SetRouteState(self, request, context):
        grpc_api_start = datetime.datetime.now()
        try:
            jsonObj = json_format.MessageToJson(
                request.route_state,
                preserving_proto_field_name=True
            )
            self.logger.debug(
                "Received request.routestate (JSON)(default=False) = {}".format( # noqa
                    jsonObj
                )
            )

            self.InitSanppi()

            self.logger.info("Requesting SetRouteState ...")
            try:
                snappi_api_start = datetime.datetime.now()
                response = self.api.set_route_state(jsonObj)
                self.logger.info(
                    "Snappi_api-SetRouteState took {} ns".format(
                        get_time_elapsed(snappi_api_start)
                    )
                )
                response_200 = """
                {
                    "status_code_200" : {
                        "warnings" : []
                    }
                }
                """
                route_response = json_format.Parse(
                    response_200,
                    snappipb_pb2.SetRouteStateResponse()
                )
                if len(response.warnings) > 0:
                    route_response.status_code_200.warnings.extend(response.warnings) # noqa
                    self.logger.debug(
                        "Snappi_api SetTransmitState Returned Warnings: {}".format( # noqa
                            response.warnings
                        )
                    )
                self.logger.debug("Returning status_code_200 to client ...")
                return route_response

            except Exception as e:
                self.logger.info(
                    "Snappi_api-SetRouteState took {} ns".format(
                        get_time_elapsed(snappi_api_start)
                    )
                )
                response_400 = """
                {
                    "status_code_400" : {
                        "errors" : []
                    }
                }
                """
                response_500 = """
                {
                    "status_code_500" : {
                        "errors" : []
                    }
                }
                """
                self.logger.error(
                    "Snappi_api SetRouteState Returned Exception : {}".format(
                        repr(e)
                    )
                )
                error_code, error_details = get_error_details(e)
                if error_code == 400:
                    route_response = json_format.Parse(
                        response_400,
                        snappipb_pb2.SetRouteStateResponse()
                    )
                    route_response.status_code_400.errors.extend(error_details) # noqa
                    return route_response
                elif error_code == 500:
                    route_response = json_format.Parse(
                        response_500,
                        snappipb_pb2.SetRouteStateResponse()
                    )
                    route_response.status_code_500.errors.extend(error_details) # noqa
                    return route_response
                else:
                    raise NotImplementedError()

        finally:
            self.logger.info(
                "gRPC-SetRouteState took {} ns".format(
                    get_time_elapsed(grpc_api_start)
                )
            )

    def SetProtocolState(self, request, context):
        grpc_api_start = datetime.datetime.now()
        try:
            jsonObj = json_format.MessageToJson(
                request.protocol_state,
                preserving_proto_field_name=True
            )
            self.logger.debug(
                "Received request.protocolstate (JSON)(default=False) = {}".format( # noqa
                    jsonObj
                )
            )

            self.InitSanppi()

            self.logger.info("Requesting SetProtocolState ...")
            try:
                snappi_api_start = datetime.datetime.now()
                response = self.api.set_protocol_state(jsonObj)
                self.logger.info(
                    "Snappi_api-SetProtocolState took {} ns".format(
                        get_time_elapsed(snappi_api_start)
                    )
                )
                response_200 = """
                {
                    "status_code_200" : {
                        "warnings" : []
                    }
                }
                """
                protocol_response = json_format.Parse(
                    response_200,
                    snappipb_pb2.SetProtocolStateResponse()
                )
                if len(response.warnings) > 0:
                    protocol_response.status_code_200.warnings.extend(response.warnings) # noqa
                    self.logger.debug(
                        "Snappi_api SetProtocolState Returned Warnings: {}".format( # noqa
                            response.warnings
                        )
                    )
                self.logger.debug("Returning status_code_200 to client ...")
                return protocol_response

            except Exception as e:
                self.logger.info(
                    "Snappi_api-SetProtocolState took {} ns".format(
                        get_time_elapsed(snappi_api_start)
                    )
                )
                response_400 = """
                {
                    "status_code_400" : {
                        "errors" : []
                    }
                }
                """
                response_500 = """
                {
                    "status_code_500" : {
                        "errors" : []
                    }
                }
                """
                self.logger.error(
                    "Snappi_api SetProtocolState Returned Exception : {}".format( # noqa
                        repr(e)
                    )
                )
                error_code, error_details = get_error_details(e)
                if error_code == 400:
                    protocol_response = json_format.Parse(
                        response_400,
                        snappipb_pb2.SetProtocolStateResponse()
                    )
                    protocol_response.status_code_400.errors.extend(error_details) # noqa
                    return protocol_response
                elif error_code == 500:
                    protocol_response = json_format.Parse(
                        response_500,
                        snappipb_pb2.SetProtocolStateResponse()
                    )
                    protocol_response.status_code_500.errors.extend(error_details) # noqa
                    return protocol_response
                else:
                    raise NotImplementedError()
        finally:
            self.logger.info(
                "gRPC-SetProtocolState took {} ns".format(
                    get_time_elapsed(grpc_api_start)
                )
            )

    def SetCaptureState(self, request, context):
        grpc_api_start = datetime.datetime.now()
        try:
            jsonObj = json_format.MessageToJson(
                request.capture_state,
                preserving_proto_field_name=True
            )
            self.logger.debug(
                "Received request.capture_state (JSON)(default=False) = {}".format( # noqa
                    jsonObj
                )
            )

            self.InitSanppi()

            self.logger.info("Requesting SetCaptureState ...")
            try:
                snappi_api_start = datetime.datetime.now()
                response = self.api.set_capture_state(jsonObj)
                self.logger.info(
                    "Snappi_api-SetCaptureState took {} ns".format(
                        get_time_elapsed(snappi_api_start)
                    )
                )
                response_200 = """
                {
                    "status_code_200" : {
                        "warnings" : []
                    }
                }
                """
                capture_response = json_format.Parse(
                    response_200,
                    snappipb_pb2.SetCaptureStateResponse()
                )
                if len(response.warnings) > 0:
                    capture_response.status_code_200.warnings.extend(response.warnings) # noqa
                    self.logger.debug(
                        "Snappi_api SetCaptureState Returned Warnings: {}".format( # noqa
                            response.warnings
                        )
                    )
                self.logger.debug("Returning status_code_200 to client ...")
                return capture_response

            except Exception as e:
                self.logger.info(
                    "Snappi_api-SetCaptureState took {} ns".format(
                        get_time_elapsed(snappi_api_start)
                    )
                )
                response_400 = """
                {
                    "status_code_400" : {
                        "errors" : []
                    }
                }
                """
                response_500 = """
                {
                    "status_code_500" : {
                        "errors" : []
                    }
                }
                """
                self.logger.error(
                    "Snappi_api SetCaptureState Returned Exception : {}".format( # noqa
                        repr(e)
                    )
                )
                error_code, error_details = get_error_details(e)
                if error_code == 400:
                    capture_response = json_format.Parse(
                        response_400,
                        snappipb_pb2.SetCaptureStateResponse()
                    )
                    capture_response.status_code_400.errors.extend(error_details) # noqa
                    return capture_response
                elif error_code == 500:
                    capture_response = json_format.Parse(
                        response_500,
                        snappipb_pb2.SetCaptureStateResponse()
                    )
                    capture_response.status_code_500.errors.extend(error_details) # noqa
                    return capture_response
                else:
                    raise NotImplementedError()

        finally:
            self.logger.info(
                "gRPC-SetCaptureState took {} ns".format(
                    get_time_elapsed(grpc_api_start)
                )
            )

    def GetMetrics(self, request, context):
        grpc_api_start = datetime.datetime.now()
        try:
            jsonObj = json_format.MessageToJson(
                request.metrics_request,
                preserving_proto_field_name=True
            )
            self.logger.debug(
                "Received request.metrics_request (JSON)(default=False) = {}".format( # noqa
                    jsonObj
                )
            )

            self.InitSanppi()

            self.logger.info("Requesting GetMetrics ...")
            try:
                snappi_api_start = datetime.datetime.now()
                response = self.api.get_metrics(jsonObj)
                self.logger.info(
                    "Snappi_api-GetMetrics took {} ns".format(
                        get_time_elapsed(snappi_api_start)
                    )
                )
                self.logger.debug(
                    "Snappi_api GetMetrics Returned : {}".format(
                        response
                    )
                )

                metric_proto = json_format.Parse(
                    response.serialize(),
                    snappipb_pb2.MetricsResponse()
                )
                get_metric_response = snappipb_pb2.GetMetricsResponse(
                    status_code_200=metric_proto
                )
                self.logger.debug("Returning Metrics to client ...")
                return get_metric_response

            except Exception as e:
                self.logger.info(
                    "Snappi_api-GetMetrics took {} ns".format(
                        get_time_elapsed(snappi_api_start)
                    )
                )
                self.logger.error(
                    "Snappi_api GetMetrics Returned Exception :  {}".format(
                        repr(e)
                    )
                )

                response_400 = """
                {
                    "status_code_400" : {
                        "errors" : []
                    }
                }
                """
                response_500 = """
                {
                    "status_code_500" : {
                        "errors" : []
                    }
                }
                """
                self.logger.error(
                    "Snappi_api GetMetrics Returned Exception : {}".format(
                        repr(e)
                    )
                )
                error_code, error_details = get_error_details(e)
                if error_code == 400:
                    metric_response = json_format.Parse(
                        response_400,
                        snappipb_pb2.GetMetricsResponse()
                    )
                    metric_response.status_code_400.errors.extend(error_details) # noqa
                    return metric_response
                elif error_code == 500:
                    metric_response = json_format.Parse(
                        response_500,
                        snappipb_pb2.GetMetricsResponse()
                    )
                    metric_response.status_code_500.errors.extend(error_details) # noqa
                    return metric_response
                else:
                    raise NotImplementedError()

        finally:
            self.logger.info(
                "gRPC-GetMetrics took {} ns".format(
                    get_time_elapsed(grpc_api_start)
                )
            )

    def GetCapture(self, request, context):
        grpc_api_start = datetime.datetime.now()
        try:
            jsonObj = json_format.MessageToJson(
                request.capture_request,
                preserving_proto_field_name=True
            )

            self.logger.debug(
                "Received request.capture_request (JSON)(default=False) = {}".format( # noqa
                    jsonObj
                )
            )

            self.InitSanppi()

            self.logger.info("Requesting GetCapture ...")
            try:
                snappi_api_start = datetime.datetime.now()
                response = self.api.get_capture(jsonObj)
                self.logger.info(
                    "Snappi_api-GetCapture took {} ns".format(
                        get_time_elapsed(snappi_api_start)
                    )
                )
                self.logger.debug(
                    "Snappi_api GetCapture Returned : {}".format(
                        response
                    )
                )

                get_capture_response = snappipb_pb2.GetCaptureResponse(
                    status_code_200=response.getvalue()
                )

                self.logger.debug("Returning Capture to client ...")
                return get_capture_response

            except Exception as e:
                self.logger.info(
                    "Snappi_api-GetCapture took {} ns".format(
                        get_time_elapsed(snappi_api_start)
                    )
                )
                self.logger.error(
                    "Snappi_api GetCapture Returned Exception :  {}".format(
                        repr(e)
                    )
                )

                response_400 = """
                {
                    "status_code_400" : {
                        "errors" : []
                    }
                }
                """
                response_500 = """
                {
                    "status_code_500" : {
                        "errors" : []
                    }
                }
                """
                self.logger.error(
                    "Snappi_api GetCapture Returned Exception : {}".format(
                        repr(e)
                    )
                )
                error_code, error_details = get_error_details(e)
                if error_code == 400:
                    capture_response = json_format.Parse(
                        response_400,
                        snappipb_pb2.GetCaptureResponse()
                    )
                    capture_response.status_code_400.errors.extend(error_details) # noqa
                    return capture_response
                elif error_code == 500:
                    capture_response = json_format.Parse(
                        response_500,
                        snappipb_pb2.GetCaptureResponse()
                    )
                    capture_response.status_code_500.errors.extend(error_details) # noqa
                    return capture_response
                else:
                    raise NotImplementedError()

        finally:
            self.logger.info(
                "gRPC-GetCapture took {} ns".format(
                    get_time_elapsed(grpc_api_start)
                )
            )


def sighandler(signum, frame):
    global server

    if server is not None:
        server.stop(5)
        server = None
        print("Server shutdown gracefully")


def serve(args):
    global server

    log_level = logging.INFO
    if args.log_debug:
        log_level = logging.DEBUG
    args.logfile = init_logging(args.logfile, log_level, args.log_stdout)

    server_logger = logging.getLogger(args.logfile)

    server_logger.info(
        "Starting gRPC Server [OTG API Version = {}] ...".format(
            OTG_API_Version
        )
    )

    signal.signal(signal.SIGTERM, sighandler)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    snappipb_pb2_grpc.add_OpenapiServicer_to_server(Openapi(args), server)

    server_address = "[::]:{}".format(args.server_port)

    if args.insecure:
        server_logger.info("Enabling insecure channel ...")
        server.add_insecure_port(server_address)
        server_logger.info("Enabled insecure channel")
    else:
        server_logger.info("Enabling secure channel ...")
        private_key = None
        certificate_chain = None
        with open(args.server_key, 'rb') as f:
            private_key = f.read()
        with open(args.server_crt, 'rb') as f:
            certificate_chain = f.read()

        if private_key is not None and certificate_chain is not None:
            server_credentials = grpc.ssl_server_credentials( ( (private_key, certificate_chain), ) ) # noqa
            server.add_secure_port(server_address, server_credentials)
            server_logger.info("Enabled secure channel")
        else:
            server_logger.error("Cannot create secure channel, need openssl key. You can generate it with below openssl command") # noqa
            server_logger.error("openssl req -newkey rsa:2048 -nodes -keyout server.key -x509 -days 365 -out server.crt -subj '/CN=test.local'") # noqa

    server.start()
    server_logger.info("gRPC Server Started at {} ...".format(server_address))

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop(5)
        server = None
        print("Server shutdown gracefully")


if __name__ == '__main__':

    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--server-port',
                        help='gRPC server port number',
                        default=40051,
                        type=int)
    parser.add_argument('--app-mode',
                        help='target Application mode',
                        choices=['ixnetwork', 'athena', 'athena-insecure'],
                        default='athena',
                        type=str)
    parser.add_argument('--target-host', help='target host address',
                        default='10.74.47.38',
                        type=str)
    parser.add_argument('--target-port', help='target port number',
                        default=30729,
                        type=int)
    parser.add_argument('--logfile',
                        help='logfile name [date and time auto appended]',
                        default='grpc_server',
                        type=str)
    parser.add_argument('--insecure',
                        help='disable TSL security, by default enabled',
                        default=True,
                        action='store_true')
    parser.add_argument('--server-key',
                        help='path to private key, default is server.key',
                        default='server.key',
                        type=str)
    parser.add_argument('--server-crt',
                        help='path to certificate key, default is server.crt',
                        default='server.crt',
                        type=str)
    parser.add_argument('--log-stdout',
                        help='show log on stdout, in addition to file',
                        default=False,
                        action='store_true')
    parser.add_argument('--log-debug',
                        help='enable debug level logging',
                        default=False,
                        action='store_true')
    args = parser.parse_args()
    serve(args)
