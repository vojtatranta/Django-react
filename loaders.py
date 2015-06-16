from django.template import TemplateDoesNotExist
from django.template.loader import make_origin
from django.template.loaders.app_directories import Loader

from template import ReactTemplate


class ReactTemplateLoader(Loader):

    def load_template(self, template_name, template_dirs=None):
        source, display_name = self.load_template_source(template_name, template_dirs)
        origin = make_origin(display_name, self.load_template_source, template_name, template_dirs)
        try:
            template = ReactTemplate(display_name, source, origin, template_name)
            return template, None
        except TemplateDoesNotExist:
            return source, display_name
