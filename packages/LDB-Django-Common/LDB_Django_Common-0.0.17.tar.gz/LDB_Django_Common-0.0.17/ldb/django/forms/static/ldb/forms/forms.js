/* Widgets:
 *   TextInput - supported
 *   NumberInput - supported
 *   EmailInput - supported
 *   URLInput - supported
 *   PasswordInput - supported
 *   HiddenInput - supported
 *   DateInput - supported
 *   DateTimeInput - supported
 *   TimeInput - supported
 *   Textarea
 *
 *   CheckboxInput
 *   Select - supported
 *   NullBooleanSelect
 *   SelectMultiple
 *   RadioSelect - supported
 *   CheckboxSelectMultiple
 *
 *   FileInput
 *   ClearableFileInput
 *
 *   MultipleHiddenInput
 *   SplitDateTimeWidget
 *   SplitHiddenDateTimeWidget
 *   SelectDateWidget
 *
 * TODO: Handle initial values
 */

var ldb = ldb || {};
ldb.django = ldb.django || {};
ldb.django.forms = ldb.django.forms || {};

ldb.django.forms.create_input = function(input_obj) {
    var input_node, label_node, i;
    var safe_attrs = ['maxlength', 'min', 'max', 'step'];

    label_node = $('<label />');

    label_node.text(input_obj.label);
    label_node.attr('for', input_obj.id);

    switch(input_obj.type) {
        case 'Select':
            var select_node = $('<select />');
            var option_node;

            select_node.attr('name', input_obj.name);
            select_node.attr('id', input_obj.id);

            for(i=0; i<input_obj.choices.length; ++i) {
                option_node = $('<option />');
                option_node.attr('value', input_obj.choices[i][0]);
                option_node.text(input_obj.choices[i][1]);

                select_node.append(option_node);
            }

            return [label_node, select_node];

        case 'RadioSelect':
            var formset_node = $('<fieldset />');
            var legend_node = $('<legend />');
            var radio_node, label_node, radio_id;

            formset_node.attr('id', input_obj.id);

            legend_node.text(input_obj.label);
            formset_node.append(legend_node);

            for(i=0; i<input_obj.choices.length; ++i) {
                radio_id = input_obj.id + '_' + i;

                label_node = $('<label />');
                label_node.attr('for', radio_id);
                label_node.text(input_obj.choices[i][1]);

                radio_node = $('<input type="radio" />');
                radio_node.attr('name', input_obj.name);
                radio_node.attr('value', input_obj.choices[i][0]);
                radio_node.attr('id', radio_id);

                formset_node.append(label_node);
                formset_node.append(radio_node);
            }

            return formset_node;

        case 'CheckboxInput':
            input_obj.input_type = 'checkbox';

            break;
    }

    if('input_type' in input_obj) {
        input_node = $('<input />');

        input_node.attr('name', input_obj.name);
        input_node.attr('id', input_obj.id);
        input_node.attr('type', input_obj.input_type);

        for(var attr in input_obj.attrs) {
            if(safe_attrs.indexOf(attr) !== -1) {
                input_node.attr(attr, input_obj.attrs[attr]);
            }
        }

        return [label_node, input_node];
    }
}

ldb.django.forms.create_form = function(form_obj, method, action) {
    var fields = form_obj.fields;
    var i;
    var form = $("<form />");

    form.attr('method', method);
    if(action !== undefined) {
        form.attr('action', action);
    }
    if(form_obj.multipart) {
        form.attr('enctype', 'multipart/form-data');
    }

    for(i=0; i<fields.length; ++i) {
        form.append(ldb.django.forms.create_input(fields[i]));
    }

    return form;
}
