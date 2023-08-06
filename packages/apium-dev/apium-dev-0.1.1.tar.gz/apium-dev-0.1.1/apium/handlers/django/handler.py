import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from apium import api_dispatch, ResponseJsonEncoder


@csrf_exempt
def api_handler(request):
    response = HttpResponse(content_type='application/json')
    jsonrpc_response = api_dispatch(request, response, request.body)
    response.content = json.dumps(jsonrpc_response, cls=ResponseJsonEncoder)
    return response
