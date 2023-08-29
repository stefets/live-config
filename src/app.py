from mako.template import Template
from mako.lookup import TemplateLookup

template = Template(filename='template.mako')
ports = {
    "midimix" : "24:0"
}
print(template.render(**ports))