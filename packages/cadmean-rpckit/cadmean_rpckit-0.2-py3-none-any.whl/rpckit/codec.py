import json


class JsonCodec:

    def __init__(self):
        self.content_type = "application/json"

    def encode(self, obj):
        return json.dumps(obj).encode("utf-8")

    def decode(self, data):
        return json.loads(data.decode("utf-8"))
