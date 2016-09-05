import os.path
import jinja2
import datetime
from PIL import Image
from cStringIO import StringIO

def dorender(handler, tname='/index.html', values={}):
    templates_dir = os.path.join(
            os.path.dirname(__file__),
            os.pardir,
            'templates')
    JINJA_ENVIRONMENT = jinja2.Environment(
            loader=jinja2.FileSystemLoader(templates_dir),
            extensions=['jinja2.ext.autoescape'],
            autoescape=True)
    def timeJST(value):
        return (value + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S').decode('utf-8')
    JINJA_ENVIRONMENT.filters.update({
        'timeJST':timeJST
    })
    template = JINJA_ENVIRONMENT.get_template(tname[1:])
    handler.response.write(template.render(values))
