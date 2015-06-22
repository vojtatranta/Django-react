import json

import datetime

from django.db.models.query import QuerySet
from django.core.serializers.base import Serializer as BaseSerializer
from django.core.serializers.python import Serializer as PythonSerializer
from django.core.serializers.json import Serializer as JsonSerializer
from django.utils import six


class ExtBaseSerializer(BaseSerializer):
    options = {}
    stream = None
    selected_fields = []
    use_natural_keys = False
    selected_props = []
    use_natural_foreign_keys = False
    use_natural_primary_keys = False

    def serialize(self, queryset, **options):
        self.options = options

        self.stream = options.pop('stream', six.StringIO())
        self.selected_fields = options.pop('fields', None)
        self.selected_props = options.pop('props', [])  # added this
        self.use_natural_keys = options.pop('use_natural_keys', False)
        self.use_natural_foreign_keys = options.pop('use_natural_foreign_keys', False)
        self.use_natural_primary_keys = options.pop('use_natural_primary_keys', False)

        self.start_serialization()
        self.first = True
        for obj in queryset:
            self.start_object(obj)
            concrete_model = obj._meta.concrete_model
            for field in concrete_model._meta.local_fields:
                if field.serialize:
                    if field.rel is None:
                        if self.selected_fields is None or field.attname in self.selected_fields:
                            self.handle_field(obj, field)
                    else:
                        if self.selected_fields is None or field.attname[:-3] in self.selected_fields:
                            self.handle_fk_field(obj, field)
            for field in concrete_model._meta.many_to_many:
                if field.serialize:
                    if self.selected_fields is None or field.attname in self.selected_fields:
                        self.handle_m2m_field(obj, field)
            # added this loop
            for field in self.selected_props:
                self.handle_prop(obj, field)
            self.end_object(obj)
            if self.first:
                self.first = False
        self.end_serialization()
        return self.getvalue()

    # added this function
    def handle_prop(self, obj, field):
        self._current[field] = getattr(obj, field)


class ExtPythonSerializer(ExtBaseSerializer, PythonSerializer):
    pass


class ExtJsonSerializer(ExtPythonSerializer, JsonSerializer):
    pass


def datetime_serializer(datetime_obj):
    return datetime_obj.isoformat()


def date_serializer(date_obj):
    return date_obj.isoformat()


SERIALIZERS = {
    datetime.datetime: datetime_serializer,
    datetime.date: date_serializer
}


def default(data):
    data_type = type(data)
    if data_type in SERIALIZERS:
        return SERIALIZERS[data_type](data)
    raise TypeError('Cannot serialize %r (type: %s)' % (data, data_type))


def jsonize(data_dict):
    dict_string = {}
    if 'view' in data_dict:
        del data_dict['view']
    for key, value in data_dict.items():
        if isinstance(value, QuerySet):
            dict_string[key] = ExtJsonSerializer().serialize(value,
                                                             fields=value.model._meta.get_all_field_names() + ['pk'],
                                                             props=[k for k, v in value.model.__dict__.iteritems()
                                                                    if isinstance(v, property)])
        else:
            dict_string[key] = json.dumps(value, default=default)
    json_str = '{'
    for key, value in dict_string.items():
        json_str += '"%s":%s,' % (key, value)
    json_str = json_str[:-1] + '}'
    return json_str
