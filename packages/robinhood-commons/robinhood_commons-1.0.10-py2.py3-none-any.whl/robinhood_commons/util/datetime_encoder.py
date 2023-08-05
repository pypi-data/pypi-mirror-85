from json import JSONDecoder, JSONEncoder
from datetime import datetime


class DateTimeEncoderDecoder(JSONDecoder, JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()