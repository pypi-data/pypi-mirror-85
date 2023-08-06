import json
from .renderer.base import Author
from .renderer.paidmessage import Colors


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Author) or isinstance(obj, Colors):
            return vars(obj)
        return json.JSONEncoder.default(self, obj)
