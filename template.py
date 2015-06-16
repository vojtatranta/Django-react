from django.template import Template


class ReactTemplate(Template):

    def __init__(self, path, *args, **kwargs):
        super(ReactTemplate, self).__init__(*args, **kwargs)
        self.path = path
