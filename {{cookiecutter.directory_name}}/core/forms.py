from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class GenericFilterFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(GenericFilterFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = 'genericFilterForm'
        self.form_method = 'GET'
        self.add_input(Submit('Filter', 'search'))


def custom_name_errors(field_name):
    name_errors = {'required': '{} is required when language provided'.format(field_name)}
    name_errors['invalid']: 'Enter a valid value'
    return name_errors


def custom_lang_errors(field_name):
    lang_errors = {'required': 'Language is required when {} provided'.format(field_name.lower())}
    lang_errors['invalid']: 'Enter a valid value'
    return lang_errors
