import json
import datetime

from django.http import HttpResponse


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, "to_json"):
            return obj.to_json()
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


class JsonResponse(HttpResponse):
    def __init__(self, content, mimetype='application/json', status=None, content_type='application/json'):
        json_text = json.dumps(content, cls=ComplexEncoder)
        super(JsonResponse, self).__init__(
            content=json_text,
            status=status,
            content_type=content_type)
