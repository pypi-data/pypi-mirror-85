import urllib.parse
from logging import Handler

from django.conf import settings
from rest_framework.utils import json

from hologger.middleware import HoLoggingMiddleware


def get_serial_data(record):
    result = {}

    try:
        result['status'] = record.data['response'].status_code
    except (AttributeError, KeyError):
        result['status'] = ""

    try:
        result['host'] = record.data['request'].META['HTTP_HOST']
    except (AttributeError, KeyError):
        result['host'] = ""

    try:
        result['uri'] = urllib.parse.urlparse(record.data['request'].get_full_path()).path
    except (AttributeError, KeyError):
        result['uri'] = ""

    try:
        result['method'] = record.data['request'].method
    except (AttributeError, KeyError):
        result['method'] = ""

    try:
        result['remote_addr'] = record.data['request'].META['REMOTE_ADDR']
    except (AttributeError, KeyError):
        result['remote_addr'] = ""

    try:
        header = {}
        for key in record.data['request'].META.keys():
            if 'wsgi' not in key:
                header[key] = record.data['request'].META[key]
        result['header'] = json.dumps(header, skipkeys=True, allow_nan=True)
    except (AttributeError, KeyError):
        result['header'] = "{}"

    try:
        result['body'] = json.dumps(record.data['body'], ensure_ascii=False)
    except (AttributeError, KeyError):
        result['body'] = "{}"

    try:
        result['response'] = record.data['response'].content.decode('utf-8')
    except (AttributeError, KeyError):
        result['response'] = "{}"

    try:
        result['pid'] = record.data['pid']
    except (AttributeError, KeyError):
        result['pid'] = None

    try:
        result['logs'] = record.data['logs']
    except (AttributeError, KeyError):
        result['logs'] = ""

    try:
        result['duration'] = record.data['duration']
    except (AttributeError, KeyError):
        result['duration'] = None

    return result


class HoLogHandler(Handler):

    def emit(self, record):

        data = get_serial_data(record)
        if data['pid'] is not None and data['uri'] not in getattr(settings, 'EXCLUDE_URIS', []):
            from .serializers import ApiResponseSerializer
            serializer = ApiResponseSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
        return


class HoLogSqlHandler(Handler):

    def emit(self, record):
        if hasattr(HoLoggingMiddleware.thread_local, "pid"):
            if not hasattr(HoLoggingMiddleware.thread_local, "logs") or HoLoggingMiddleware.thread_local.logs is None:
                HoLoggingMiddleware.thread_local.logs = ""
            HoLoggingMiddleware.thread_local.logs += "\n" + self.format(record)

