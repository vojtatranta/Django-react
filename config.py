from os import path

from django.conf import settings

NODE_SERVER_URL = getattr(settings, 'NODE_SERVER_URL', 'http://localhost:3333')
REACT_RENDERING_SCRIPT = getattr(settings, 'REACT_RENDERING_SCRIPT', path.abspath(path.join(path.dirname(__file__),
                                                                                            'js', 'entry.js')))
