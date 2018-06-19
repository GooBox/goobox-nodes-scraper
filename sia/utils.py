import datetime
import json


class SiaNodeDecoder(json.JSONDecoder):
    datetime_format = "%Y-%m-%dT%H:%M:%S.%fZ"

    def decode(self, *args, **kwargs):
        obj = super().decode(*args, **kwargs)

        for node in obj["hosts"]:
            if "scanhistory" in node:
                for scan in node["scanhistory"]:
                    scan["timestamp"] = datetime.datetime.strptime(scan["timestamp"][:-4] + "Z", self.datetime_format)

        return obj["hosts"]
