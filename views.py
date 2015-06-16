from __future__ import unicode_literals

from django.views.generic import TemplateView

from .response import ReactResponse


class ReactTemplateView(TemplateView):

    response_class = ReactResponse
