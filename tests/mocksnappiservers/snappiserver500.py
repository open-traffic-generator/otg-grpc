from flask import Flask, request, Response
import threading
import json
import time
import requests

app = Flask(__name__)
CONFIG = None


@app.route('/status', methods=['GET'])
def get_status():
    return Response(status=200,
                    response=json.dumps({'status': 'up'}),
                    headers={'Content-Type': 'application/json'})


@app.route('/config', methods=['POST'])
def set_config():
    return Response(status=500,
                    response=json.dumps(
                        {'errors': ['mock 500 set_config error']}),
                    headers={'Content-Type': 'application/json'})


@app.route('/config', methods=['GET'])
def get_config():
    return Response(status=500,
                    response=json.dumps(
                        {'errors': ['mock 500 get_config error']}),
                    headers={'Content-Type': 'application/json'})


@app.route('/control/transmit', methods=['POST'])
def set_transmit_state():
    return Response(status=500,
                    response=json.dumps(
                        {'errors': ['mock 500 set_transmit_state error']}),
                    headers={'Content-Type': 'application/json'})


@app.route('/control/link', methods=['POST'])
def set_link_state():
    return Response(status=500,
                    response=json.dumps(
                        {'errors': ['mock 500 set_link_state error']}),
                    headers={'Content-Type': 'application/json'})


@app.route('/results/metrics', methods=['POST'])
def get_metrics():
    return Response(status=500,
                    response=json.dumps(
                        {'errors': ['mock 500 get_metrics error']}),
                    headers={'Content-Type': 'application/json'})


@app.after_request
def after_request(resp):
    print(request.method, request.url, ' -> ', resp.status)
    return resp


def web_server():
    app.run(port=100, debug=True, use_reloader=False)


class SnappiServer500(object):
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
                r = requests.get(url='http://127.0.0.1:100/status')
                res = r.json()
                if res['status'] != 'up':
                    raise Exception('waiting for SnappiServer500 to be up')
                break
            except Exception as e:
                print(e)
                pass
            time.sleep(.1)
