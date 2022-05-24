from enum import Enum
from typing import Type
from bottle import PluginError, Route, Bottle, request, response
from inspect import signature

class Resource(object):

    class Methods(Enum):
        GET = "GET"
        POST = "POST"
        PUT = "PUT"
        DELETE = "DELETE"
        OPTIONS = "OPTIONS"

    @property
    def params(self):
        return request.params

    def getFunction(self, method: str):
        return getattr(self, method.lower(), None)

    def getRouteConfig(self, method: str):
        return getattr(self, method.upper(), {})


class API(object):
    name = 'bottle-rest'
    api = 2

    def __init__(self, debug=False):
         self.debug = debug

    def setup(self, app: Bottle):
        ''' Make sure that other installed plugins don't affect the same
            keyword argument.'''
        self.app = app
        for other in app.plugins:
            if not isinstance(other, API): continue
            if other.keyword == self.keyword:
                raise PluginError("Found another sqlite plugin with "\
                "conflicting settings (non-unique keyword).")

    def apply(self, callback, context: Route):
        def _wrapper(*args, **kwargs):
            params = signature(callback).parameters
            if self.debug:
                print(f"args: {args}")
                print(f"kwargs: {kwargs}")
                print(f"url params: {list(request.params.items())}")
                print(f"method params: {params}")
            if params:
                data = request.json
                if not data:
                    data = {}
                for name, val in params.items():
                    if (name not in data) and (name not in kwargs) and (val.default == val.empty):
                        response.status = 400
                        return {name: f"This feild is is required"}
                return callback(**data, **kwargs)
            return callback()
        return _wrapper

    def addResource(self, resource_cls: Type[Resource], *rules):
        for rule in rules:
            if self.debug:
                (f"Adding rescource '{rule}'")
            resource = resource_cls()
            for method in resource.Methods:
                method = method.value
                func = resource.getFunction(method)
                cfg = resource.getRouteConfig(method)
                if func:
                    if self.debug:
                        print(f"Creating route {method} {rule} for method {func}")
                    self.app.route(rule, method, func, **cfg)