from __future__ import unicode_literals

from django.views.generic import TemplateView

from .response import ReactResponse


class ReactTemplateView(TemplateView):

    base_template_name = ''
    response_class = ReactResponse

    def render_to_response(self, context, **response_kwargs):
        response_kwargs.setdefault('content_type', self.content_type)
        return self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=context,
            base_template=self.base_template_name,
            **response_kwargs
        )
