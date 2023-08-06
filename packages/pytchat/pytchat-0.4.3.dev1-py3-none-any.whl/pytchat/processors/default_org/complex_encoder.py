import json
from .renderer.base import Author


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Author):
            return vars(obj)
        return json.JSONEncoder.default(self, obj)
