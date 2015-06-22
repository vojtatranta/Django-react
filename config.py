from os import path

from django.conf import settings

NODE_SERVER_URL = getattr(settings, 'NODE_SERVER_URL', 'http://localhost:3333')

REACT_RENDERING_SCRIPT = getattr(settings, 'REACT_RENDERING_SCRIPT', path.abspath(path.join(path.dirname(__file__),
                                                                                            'js', 'entry.coffee')))

'''
Set location of you file that bundles all frontend dependencies, so that Django could create relative path
of React template file.
eg.: /var/User/project/app/js/main.js
By default it is None and Django passes absolute path to matched template
'''
ENTRY_JS_FILE = getattr(settings, 'ENTRY_JS_FILE', None)
