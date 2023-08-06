from django.forms import widgets

def json_from_form(form):
    json_obj = {}
    form_field_name_order = form.fields.keys()

    json_obj['fields'] = []
    json_obj['multipart'] = form.is_multipart()

    for field_name in form_field_name_order:
        bound_field = form[field_name]
        widget = bound_field.field.widget

        field_obj = {'label': bound_field.label,
                     'name': bound_field.name,
                     'type': widget.__class__.__name__,
                     'id': bound_field.auto_id,
                     'attrs': widget.attrs}

        if isinstance(widget, widgets.Input):
            field_obj['input_type'] = widget.input_type

        if isinstance(widget, widgets.Select):
            field_obj['choices'] = [[str(_) for _ in a]
                                    for a in widget.choices]

        json_obj['fields'].append(field_obj)

    return json_obj
