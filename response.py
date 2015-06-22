import requests

from os.path import relpath

from Naked.toolshed.shell import muterun_js

from django.template import TemplateSyntaxError
from django.template.response import TemplateResponse

from .jsonizer import jsonize

import config


class ReactResponse(TemplateResponse):

    use_tcp = True
    react_renderer_script_path = config.REACT_RENDERING_SCRIPT
    node_server_url = config.NODE_SERVER_URL
    template = None

    def __init__(self, base_template='', *args, **kwargs):
        self.base_template_name = base_template
        super(ReactResponse, self).__init__(*args, **kwargs)

    def get_templates_path_dict(self, path):
        print path, config.ENTRY_JS_FILE
        print relpath(path, config.ENTRY_JS_FILE)
        return {
            'absolute': path,
            'relative': relpath(path, config.ENTRY_JS_FILE) if config.ENTRY_JS_FILE else path
        }

    @property
    def rendered_content(self):
        self.template = self.resolve_template(self.template_name)
        self.context_data.update({
            'react_template_file_path': self.get_templates_path_dict(self.template.path),
            'react_base_template_file_path': self.get_templates_path_dict(
                self.resolve_template(self.base_template_name).path)
        })
        return self.get_html_from_node_server() if self.use_tcp else self.get_html_from_node()

    def context_data_to_json(self, data):
        return jsonize(data)

    def get_html_from_node(self):
        node_request = muterun_js(self.react_renderer_script_path, "'%s'" % jsonize(self.context_data))
        if node_request.stderr:
            raise TemplateSyntaxError(node_request.stderr)
        return node_request.stdout

    def get_html_from_node_server(self):
        request = requests.post(self.node_server_url, jsonize(self.context_data), headers={
            'Content-type': 'application/json', 'Accept': 'text/plain'})
        if request.status_code > 500:
            raise TemplateSyntaxError(request.text)
        else:
            return request.text
