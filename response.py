import requests

from Naked.toolshed.shell import muterun_js

from django.template import TemplateSyntaxError
from django.template.response import TemplateResponse

from jsonizer import jsonize


class ReactResponse(TemplateResponse):

    use_tcp = True
    react_renderer_script_path = ''
    template = None

    @property
    def rendered_content(self):
        self.template = self.resolve_template(self.template_name)
        del self.context_data['view']
        self.context_data['react_template_file'] = self.template.path
        return self.get_html_from_node_server() if self.use_tcp else self.get_html_from_node()

    def context_data_to_json(self, data):
        return jsonize(data)

    def get_html_from_node(self):
        node_request = muterun_js(self.react_renderer_script_path, "'%s'" % self.context_data_to_json(self.context_data))
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
