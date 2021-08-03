from flask import Flask, request, Response
import threading
import json
import time
import snappi
import requests
import tests.common.utils as utils

app = Flask(__name__)
CONFIG = None


@app.route('/status', methods=['GET'])
def get_status():
    return Response(status=200,
                    response=json.dumps({'status': 'up'}),
                    headers={'Content-Type': 'application/json'})


@app.route('/config', methods=['POST'])
def set_config():
    global CONFIG
    config = snappi.api().config()
    config.deserialize(request.data.decode('utf-8'))
    test = config.options.port_options.location_preemption
    if test is not None and isinstance(test, bool) is False:
        return Response(status=590,
                        response=json.dumps({'detail': 'invalid data type'}),
                        headers={'Content-Type': 'application/json'})
    else:
        status = utils.get_mockserver_status()
        if status == "200":
            CONFIG = config
            return Response(status=200,
                            response=json.dumps({'warnings': []}),
                            headers={'Content-Type': 'application/json'})
        elif status == "200-warning":
            CONFIG = config
            return Response(status=200,
                            response=json.dumps(
                                {'warnings': ['mock 200 set_config warning']}),
                            headers={'Content-Type': 'application/json'})
        elif status == "400":
            return Response(status=400,
                            response=json.dumps(
                                {'errors': ['mock 400 set_config error']}),
                            headers={'Content-Type': 'application/json'})
        elif status == "500":
            return Response(status=500,
                            response=json.dumps(
                                {'errors': ['mock 500 set_config error']}),
                            headers={'Content-Type': 'application/json'})
        else:
            return Response(status=501,
                            response=json.dumps(
                                {'errors': ['set_config is not implemented']}),
                            headers={'Content-Type': 'application/json'})


@app.route('/config', methods=['GET'])
def get_config():
    global CONFIG
    status = utils.get_mockserver_status()
    if status in ["200",  "200-warning"]:
        return Response(CONFIG.serialize() if CONFIG is not None else '{}',
                        mimetype='application/json',
                        status=200)
    elif status == "400":
        return Response(status=400,
                        response=json.dumps(
                            {'errors': ['mock 400 get_config error']}),
                        headers={'Content-Type': 'application/json'})
    elif status == "500":
        return Response(status=500,
                        response=json.dumps(
                            {'errors': ['mock 500 get_config error']}),
                        headers={'Content-Type': 'application/json'})
    else:
        return Response(status=501,
                        response=json.dumps(
                            {'errors': ['get_config is not implemented']}),
                        headers={'Content-Type': 'application/json'})


@app.route('/control/link', methods=['POST'])
def set_link_state():
    global CONFIG
    status = utils.get_mockserver_status()
    if status == "200":
        return Response(status=200,
                        response=json.dumps({'warnings': []}),
                        headers={'Content-Type': 'application/json'})
    elif status == "200-warning":
        return Response(status=200,
                        response=json.dumps(
                            {'warnings': ['mock 200 set_link_state warning']}),
                        headers={'Content-Type': 'application/json'})
    elif status == "400":
        return Response(status=400,
                        response=json.dumps(
                            {'errors': ['mock 400 set_link_state error']}),
                        headers={'Content-Type': 'application/json'})
    elif status == "500":
        return Response(status=500,
                        response=json.dumps(
                            {'errors': ['mock 500 set_link_state error']}),
                        headers={'Content-Type': 'application/json'})
    else:
        return Response(status=501,
                        response=json.dumps(
                            {'errors': ['set_link_state is not implemented']}),
                        headers={'Content-Type': 'application/json'})


@app.route('/control/transmit', methods=['POST'])
def set_transmit_state():
    global CONFIG
    status = utils.get_mockserver_status()
    if status == "200":
        return Response(status=200,
                        response=json.dumps({'warnings': []}),
                        headers={'Content-Type': 'application/json'})
    elif status == "200-warning":
        return Response(status=200,
                        response=json.dumps(
                            {
                                'warnings': [
                                    'mock 200 set_transmit_state warning'
                                ]
                            }
                        ),
                        headers={'Content-Type': 'application/json'})
    elif status == "400":
        return Response(status=400,
                        response=json.dumps(
                            {'errors': ['mock 400 set_transmit_state error']}),
                        headers={'Content-Type': 'application/json'})
    elif status == "500":
        return Response(status=500,
                        response=json.dumps(
                            {'errors': ['mock 500 set_transmit_state error']}),
                        headers={'Content-Type': 'application/json'})
    else:
        return Response(status=501,
                        response=json.dumps(
                            {
                                'errors': [
                                    'set_transmit_state is not implemented'
                                ]
                            }
                        ),
                        headers={'Content-Type': 'application/json'})


@app.route('/results/metrics', methods=['POST'])
def get_metrics():
    status = utils.get_mockserver_status()
    global CONFIG
    if status in ["200", "200-warning"]:
        api = snappi.api()
        metrics_request = api.metrics_request()
        metrics_request.deserialize(request.data.decode('utf-8'))
        metrics_response = api.metrics_response()
        if metrics_request.choice == 'port':
            for port in CONFIG.ports:
                metrics_response.port_metrics.metric(
                    name=port.name, frames_tx=10000, frames_rx=10000
                )
        elif metrics_request.choice == 'flow':
            for flow in CONFIG.flows:
                metrics_response.flow_metrics.metric(
                    name=flow.name, frames_tx=10000, frames_rx=10000
                )

        return Response(metrics_response.serialize(),
                        mimetype='application/json',
                        status=200)
    elif status == "400":
        return Response(status=400,
                        response=json.dumps(
                            {'errors': ['mock 400 get_metrics error']}),
                        headers={'Content-Type': 'application/json'})
    elif status == "500":
        return Response(status=500,
                        response=json.dumps(
                            {'errors': ['mock 500 get_metrics error']}),
                        headers={'Content-Type': 'application/json'})
    else:
        return Response(status=501,
                        response=json.dumps(
                            {'errors': ['get_metrics is not implemented']}),
                        headers={'Content-Type': 'application/json'})


@app.after_request
def after_request(resp):
    print(request.method, request.url, ' -> ', resp.status)
    return resp


def web_server():
    app.run(port=80, debug=True, use_reloader=False)


class SnappiServer(object):
    def __init__(self):
        self._CONFIG = None

    def start(self):
        self._web_server_thread = threading.Thread(target=web_server)
        self._web_server_thread.setDaemon(True)
        self._web_server_thread.start()
        self._wait_until_ready()
        return self

    def _wait_until_ready(self):
        while True:
            try:
                r = requests.get(url='http://127.0.0.1:80/status')
                res = r.json()
                if res['status'] != 'up':
                    raise Exception('waiting for SnappiServer to be up')
                break
            except Exception as e:
                print(e)
                pass
            time.sleep(.1)
