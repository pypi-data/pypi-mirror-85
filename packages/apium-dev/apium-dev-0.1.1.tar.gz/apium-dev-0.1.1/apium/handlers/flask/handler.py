import json
from flask import make_response, request
from apium import api_dispatch, ResponseJsonEncoder


def api_handler():
    response = make_response()
    jsonrpc_response = api_dispatch(request, response, request.data)
    response.headers['Content-Type'] = 'application/json'
    response.data = json.dumps(jsonrpc_response, cls=ResponseJsonEncoder)
    return response
