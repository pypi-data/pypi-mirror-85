from flask import Flask, jsonify, request

from .interception_model import new_session
from .interception_service import InterceptionService
from ._configuration import interception_config
from .exceptions import ExceptionBase

__all__ = [
    'start_agent_server'
]

app = Flask(__name__)


@app.errorhandler(ExceptionBase)
def error(e):
    return jsonify({'cls': e.__class__.__name__}), 401


@app.route("/", methods=["GET"])
def index():
    return jsonify({'message': 'Hello World!'})


@app.route('/api/interception', methods=['POST'])
def interception_post():
    ps = request.json['ps']
    name = request.json['name']
    x = request.json['x']
    trace = request.json['trace']
    session = None
    try:
        session = new_session()
        interception_service = InterceptionService(session)
        interception = interception_service.add_interception(ps=ps, name=name, x=x, trace=trace)
        session.commit()
        return jsonify({'message': 'Interception added successfully', 'id': interception.id}), 201
    finally:
        if session:
            session.close()


@app.route('/api/interception', methods=['PUT'])
def interception_put():
    key = request.json['key']
    method = request.json['method']
    with open(interception_config.dat_file, 'w') as dat:
        dat.write(f'{key} {method}')
    return jsonify({'message': 'DAT file created'})


def start_agent_server():
    app.run(host='0.0.0.0', port=interception_config.agent_port)


if __name__ == '__main__':
    start_agent_server()
