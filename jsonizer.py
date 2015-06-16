import json

import datetime

from django.core import serializers
from django.db.models.query import QuerySet
from django.conf import settings

from django.template.defaultfilters import date


def datetime_serializer(datetime):
    return datetime.isoformat()


def date_serializer(date):
    return date.isoformat()


SERIALIZERS = dict((
    (datetime.datetime, datetime_serializer),
    (datetime.date, date_serializer)
))


def default(data):
    data_type = type(data)
    if data_type in SERIALIZERS:
        return SERIALIZERS[data_type](data)
    raise TypeError('Cannot serialize %r (type: %s)' % (data, data_type))


def jsonize(data_dict):
    dict_string = {}
    for key, value in data_dict.items():
        if isinstance(value, QuerySet):
            dict_string[key] = serializers.serialize('json', value,
                                                     fields=value.model._meta.get_all_field_names() + ['pk'])
        else:
            dict_string[key] = json.dumps(value, default=default)
    json_str = '{'
    for key, value in dict_string.items():
        json_str += '"%s":%s,' % (key, value)
    json_str = json_str[:-1] + '}'
    return json_str
