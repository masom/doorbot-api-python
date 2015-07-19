from wtforms import Form, StringField, validators


class RegistrationForm(Form):
    contact_name = StringField(
        'Contact Name', [validators.Length(min=4, max=255)]
    )

    contact_email = StringField(
        'Contact Email', [validators.Email(), validators.Length(max=255)]
    )

    contact_phone_number = StringField(
        'Contact Phone Number', [validators.Length(min=7, max=20)]
    )

    host = StringField('Desired subdomain', [validators.Length(min=3, max=25)])
    name = StringField('Account name', [validators.Length(min=3, max=50)])
