from flask import Flask, request, jsonify

from ._configuration import interception_config
from wafec.openstack.testlib.clients import InterceptionAgentClient

app = Flask(__name__)

__all__ = [
    'start_controller_server'
]

agents = [

]


@app.route("/", methods=["GET"])
def index():
    return jsonify({'message': 'Hello World!'})


@app.route('/api/interception', methods=['PUT'])
def interception_put():
    key = request.json['key']
    method = request.json['method']
    for agent in agents:
        client = InterceptionAgentClient(agent)
        client.put(key, method)
    return jsonify({'success': True})


def start_controller_server():
    app.run(host='0.0.0.0', port=interception_config.controller_port)


if __name__ == '__main__':
    start_controller_server()
