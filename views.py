from __future__ import unicode_literals
from django.db.models.sql import Query

import six
import json
import datetime

from json import JSONEncoder

from django.core import serializers

from django.template import TemplateDoesNotExist, Template, TemplateSyntaxError
from django.template.loader import make_origin
from django.template.loaders.app_directories import Loader
from django.conf import settings
from django.db.models.query import QuerySet
from django.core import serializers

from django.template.response import TemplateResponse
from django.views.generic import TemplateView

from Naked.toolshed.shell import muterun_js

from jsonizer import jsonize

from students.models import Instructor
from users.models import User


class ReactJSONEncoder(JSONEncoder):

    def default(self, o):
        if isinstance(o, six.string_types + (dict,)):
            return o
        else:
            return o.__dict__


class ReactTemplate(Template):

    def __init__(self, path, *args, **kwargs):
        super(ReactTemplate, self).__init__(*args, **kwargs)
        self.path = path


class ReactTemplateLoader(Loader):

    def load_template(self, template_name, template_dirs=None):
        source, display_name = self.load_template_source(template_name, template_dirs)
        origin = make_origin(display_name, self.load_template_source, template_name, template_dirs)
        try:
            template = ReactTemplate(display_name, source, origin, template_name)
            return template, None
        except TemplateDoesNotExist:
            # If compiling the template we found raises TemplateDoesNotExist, back off to
            # returning the source and display name for the template we were asked to load.
            # This allows for correct identification (later) of the actual template that does
            # not exist.
            return source, display_name

    def load_template_source(self, template_name, template_dirs=None):
        for filepath in self.get_template_sources(template_name, template_dirs):
            try:
                with open(filepath, 'rb') as fp:
                    return (fp.read().decode(settings.FILE_CHARSET), filepath)
            except IOError:
                pass
        raise TemplateDoesNotExist(template_name)


class ReactResponse(TemplateResponse):

    use_tcp = True
    react_renderer_script = '/Users/vojtatranta/jezdimvcas/jvcis/dj/apps/core/templates/entry.js'
    template = None

    @property
    def rendered_content(self):
        self.template = self.resolve_template(self.template_name)
        del self.context_data['view']
        self.context_data['react_template_file'] = self.template.path
        return self.get_html_from_node_server() if self.use_tcp else self.get_html_from_node()

    def get_html_from_node(self):
        node_request = muterun_js(self.react_renderer_script, "'%s'" % jsonize(self.context_data))
        if node_request.stderr:
            raise TemplateSyntaxError(node_request.stderr)
        return node_request.stdout

    def get_html_from_node_server(self):
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        request = requests.post('http://localhost:3333', jsonize(self.context_data), headers=headers)
        if request.status_code > 500:
            raise TemplateSyntaxError(request.text)
        else:
            return request.text

    def jsonize(self, data_dict):
        dict_string = {}
        for key, value in data_dict.items():
            if isinstance(value, QuerySet):
                dict_string[key] = serializers.serialize('json', value)
            else:
                dict_string[key] = json.dumps(value)
        json_str = '{'
        for key, value in dict_string.items():
            json_str += '"%s":%s,' % (key, value)
        json_str = json_str[:-1] + '}'
        return json_str


class ReactTemplateView(TemplateView):

    response_class = ReactResponse
    template_name = 'react.jsx'

    def get_context_data(self, **kwargs):
        context_data = super(ReactTemplateView, self).get_context_data(**kwargs)
        context_data['title'] = 'Hello React world'
        context_data['app_name'] = 'Great app!'
        context_data['users'] = User.objects.all()
        context_data['today'] = datetime.date.today()
        return context_data
