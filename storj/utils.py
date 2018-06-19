import datetime
import json


class StorjNodeDecoder(json.JSONDecoder):
    datetime_format = "%Y-%m-%dT%H:%M:%S.%fZ"

    def decode(self, *args, **kwargs):
        nodes = super().decode(*args, **kwargs)

        for node in nodes:
            if "lastSeen" in node:
                node["lastSeen"] = datetime.datetime.strptime(node["lastSeen"], self.datetime_format)

            if "lastTimeout" in node:
                node["lastTimeout"] = datetime.datetime.strptime(node["lastTimeout"], self.datetime_format)

        return nodes
