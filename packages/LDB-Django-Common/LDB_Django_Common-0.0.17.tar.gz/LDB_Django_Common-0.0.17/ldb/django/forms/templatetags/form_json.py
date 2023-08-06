import json

from django import template

from ldb.django.forms import json as form_json_

register = template.Library()

@register.simple_tag
def form_json(form):
    return json.dumps(form_json_.json_from_form(form))
