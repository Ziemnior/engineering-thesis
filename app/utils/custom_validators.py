from wtforms import ValidationError


class GreaterThan:
    def __init__(self, fieldname, message=None):
        self.fieldname = fieldname
        self.message = message

    def __call__(self, form, field):
        try:
            other = form[self.fieldname]
        except KeyError:
            raise ValidationError(field.gettext("Invalid field name {}").format(self.fieldname))
        if field.data != '' and field.data < other.data:
            d = {'other_label': hasattr(other, 'label') and other.label.text or self.fieldname,
                 'other_name': self.fieldname}
            if self.message is None:
                self.message = field.gettext('Field must be greater than %(other_name)s.')
            raise ValidationError(self.message % d)
