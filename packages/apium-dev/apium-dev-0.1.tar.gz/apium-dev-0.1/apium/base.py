import json
import logging
import re
import sys
from collections import OrderedDict, defaultdict
from importlib import import_module
import traceback
from .fields import UNDEF, BaseField

api_methods = {}

# TODO: move from global namespace or clean each time by run api method
middle_order = {}
fields_middles_map = defaultdict(list)

try:
    from api.api_settings import DEBUG, JR_API_DIR, JR_API_FILE
except ImportError:
    DEBUG = False
    JR_API_DIR = 'api'
    JR_API_FILE = 'method'

# TODO: remove from global namespace after testing ordered middleware
# middles_is_mapped_to_fields = []
last_middles = []
last_middles_name = set()

first_middles = []
first_middles_name = set()


class ResponseJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if obj == UNDEF:
            return None
        return super(ResponseJsonEncoder, self).default(obj)


def api_dispatch(request, response, body):
    try:
        body = json.loads(body)
    except json.decoder.JSONDecodeError:
        return {
            'jsonrpc': '2.0',
            'id': None,
            'error': {
                'code': -32700,
                'message': 'Parse error',
            },
        }
    request_id = body.get('id')
    version = body.get('jsonrpc')
    if version != '2.0':
        error_text = 'JSONRPC protocol version MUST be exactly "2.0"'
        return {
            'jsonrpc': '2.0',
            'id': request_id,
            'error': {
                'code': -32600,
                'message': 'Invalid Request',
                'data': {
                    'text': error_text,
                },
            },
        }
    api_name = body.get('method')
    if not api_name:
        error_text = (
            'Method field MUST containing the name of the method to be invoked'
        )
        return {
            'jsonrpc': '2.0',
            'id': request_id,
            'error': {
                'code': -32600,
                'message': 'Invalid Request',
                'data': {
                    'text': error_text,
                },
            },
        }
    if api_name not in api_methods:
        try:
            # example: api.echo.method
            # file: api/echo/method.py
            import_module('{}.{}.{}'.format(JR_API_DIR, api_name, JR_API_FILE))
        except ModuleNotFoundError:
            return {
                'jsonrpc': '2.0',
                'id': request_id,
                'error': {
                    'code': -32601,
                    'message': 'Method not found',
                },
            }
        except Exception:
            jsonrpc_response = {
                'jsonrpc': '2.0',
                'id': request_id,
            }
            error = {
                'code': -1,
                'message': 'Internal error',
            }
            stack = traceback.format_exc()
            if DEBUG:
                error['data'] = {
                    'stack': stack,
                    'executable': sys.executable,
                }
            logging.error('{}'.format(stack))
            jsonrpc_response.update({'error': error})
            return jsonrpc_response
    cls = api_methods.get(api_name)
    if not cls:
        return {
            'jsonrpc': '2.0',
            'id': request_id,
            'error': {
                'code': -32601,
                'message': 'Method not found',
            },
        }
    params = body.get('params', {})  # TODO: support params as list (not {})
    jsonrpc_response = {
        'jsonrpc': '2.0',
        'id': request_id,
    }
    try:
        instance = cls(request, response, params)
        if instance.result is not UNDEF:
            jsonrpc_response.update({'result': instance.result})
            return jsonrpc_response
        else:
            jsonrpc_response.update({
                'error': {
                    'code': -32603,
                    'message': 'Internal error',
                }
            })
    except Exception as exc:
        error = {
            'code': -1,
            'message': str(exc),
        }
        stack = traceback.format_exc()
        if DEBUG:
            error['data'] = {
                'stack': stack,
                'executable': sys.executable,
            }
        logging.error('{}'.format(stack))
        jsonrpc_response.update({'error': error})
    return jsonrpc_response


class MetaBase(type):
    def __new__(self, name, bases, namespace):
        cls = super(MetaBase, self).__new__(self, name, bases, namespace)
        cls_mro = cls.mro()
        if len(cls_mro) > 2:  # 1 - UserCustomMethod, 2 - Method, 3 - object
            api_name = cls.__name__
            api_name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', api_name)
            api_name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', api_name).lower()
            api_methods[api_name] = cls
        cls._fields = {
            key: val.order
            for key, val in namespace.items()
            if isinstance(val, BaseField)
        }
        # for inheritance
        for item in cls_mro[1:-1]:  # exclude UserCustomMethod and object
            if hasattr(item, '_fields'):
                cls._fields.update(item._fields)
        cls._fields = OrderedDict(
            sorted(cls._fields.items(), key=lambda item: item[1])
        )
        return cls


class Method(metaclass=MetaBase):
    method_cache = {}

    def __init__(self, request, response, data, *args, **kwargs):
        print('class method init')
        self.request = request
        self.response = response
        self.result = UNDEF
        self.method_cache = {}
        print('M F {}'.format(self._fields))
        fields = list(self._fields.items())
        middles_is_mapped_to_fields = set()
        # run @order_first middlewares
        for item in type(self).mro()[:-1]:
            middle_method = getattr(
                self, '_{}__middle'.format(item.__name__), None
            )
            orig_qualname = '{}.__middle'.format(item.__name__)
            if (
                middle_method
                and middle_method not in middles_is_mapped_to_fields
                and orig_qualname in first_middles_name
            ):
                middle_method()
        if fields:
            middle_methods_mro = {}
            for item in type(self).mro()[:-1]:
                middle_method = getattr(
                    self, '_{}__middle'.format(item.__name__), None
                )
                if middle_method:
                    orig_qualname = '{}.__middle'.format(item.__name__)
                    middle_methods_mro[orig_qualname] = middle_method
            prev_field = fields[0]
            print('middle_order', middle_order)
            # run middlewares if order of middle less then order of first field
            for orig_qualname, method in middle_methods_mro.items():
                order = middle_order.get(orig_qualname)
                if method not in middles_is_mapped_to_fields:
                    if order is not None and order < prev_field[1]:
                        method()
                        middles_is_mapped_to_fields.add(method)
            for item_field in fields[1:]:
                for orig_qualname, method in middle_methods_mro.items():
                    order = middle_order.get(orig_qualname)
                    if method not in middles_is_mapped_to_fields:
                        if order is not None and order < item_field[1]:
                            fields_middles_map[prev_field[0]].append(method)
                            middles_is_mapped_to_fields.add(method)
                prev_field = item_field
        for key in self._fields:
            try:
                print('METHOD - {} : {}'.format(key, data.get(key)))
                setattr(self, key, data.get(key, UNDEF))
                # for ext validate (run validate_<field>)
                validator = getattr(self, 'validate_{}'.format(key), None)
                if validator:
                    validator(getattr(self, key))
                for middle_method in fields_middles_map[key]:
                    # middle_method(self)
                    middle_method()
            except Exception as exc:
                raise ValueError('{}: {}'.format(key, exc))
        self.validate()
        # for middleware (run __middle method)
        # run middleware if middleware not ordered by decorator
        for item in type(self).mro()[:-1]:
            middle_method = getattr(
                self, '_{}__middle'.format(item.__name__), None
            )
            orig_qualname = '{}.__middle'.format(item.__name__)
            if (
                middle_method
                and middle_method not in middles_is_mapped_to_fields
                and orig_qualname not in first_middles_name
                and orig_qualname not in last_middles_name
            ):
                middle_method()
        # run @order_last middlewares
        for item in type(self).mro()[:-1]:
            middle_method = getattr(
                self, '_{}__middle'.format(item.__name__), None
            )
            orig_qualname = '{}.__middle'.format(item.__name__)
            if (
                middle_method
                and middle_method not in middles_is_mapped_to_fields
                and orig_qualname in last_middles_name
            ):
                middle_method()
        self.result = self.execute()
        # for middleware after execute (run __after method)
        for item in type(self).mro()[:-1]:
            after_method = getattr(
                self, '_{}__after'.format(item.__name__), None
            )
            if after_method:
                after_method()

    def validate(self):
        pass

    def execute(self):
        pass


def order(value):
    def decorator(func):
        middle_order[func.__qualname__] = value

        def wrapper(*args, **kwargs):
            return_value = func(*args, **kwargs)
            return return_value

        return wrapper

    return decorator


def order_first(func):
    first_middles.append(func)
    first_middles_name.add(func.__qualname__)

    def wrapper(*args, **kwargs):
        return_value = func(*args, **kwargs)
        return return_value

    return wrapper


def order_last(func):
    last_middles.append(func)
    last_middles_name.add(func.__qualname__)

    def wrapper(*args, **kwargs):
        return_value = func(*args, **kwargs)
        return return_value

    return wrapper
