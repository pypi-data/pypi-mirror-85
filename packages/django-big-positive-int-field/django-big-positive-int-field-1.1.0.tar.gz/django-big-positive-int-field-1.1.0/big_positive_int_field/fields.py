from django.core import exceptions
from django.db import models
from django.utils.translation import ugettext_lazy as _


class BigPositiveIntegerField(models.TextField):
    """
    The field is responsible to store a big positive integer (~infinity), also includes 0 as default.
    """
    description = 'Big Positive Integer Field'

    def __init__(self, *args, **kwargs):
        self.default_error_messages = {
            'invalid': _('Enter a valid Positive Integer')
        }
        kwargs['default'] = kwargs.get('default', 0)
        kwargs['help_text'] = kwargs.get('help_text', self.default_error_messages['invalid'])

        super().__init__(*args, **kwargs)

    def to_python(self, value):
        if value is None or isinstance(value, str):
            return value
        return str(value)

    def get_prep_value(self, value):
        if value is None:
            return self.to_python(value)
        if not str(value).isdecimal():
            raise exceptions.ValidationError(self.default_error_messages['invalid'])
        return self.to_python(value)

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        try:
            return int(value)
        except Exception as e:
            return value
