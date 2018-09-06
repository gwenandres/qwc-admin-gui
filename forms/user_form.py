from flask_wtf import FlaskForm
from wtforms import FieldList, FormField, HiddenField, SelectField, \
    StringField, SubmitField, TextAreaField, ValidationError, PasswordField
from wtforms.validators import DataRequired, Optional, Email, EqualTo


class GroupForm(FlaskForm):
    """Subform for groups"""
    group_id = HiddenField(validators=[DataRequired()])
    group_name = HiddenField(validators=[Optional()])


class RoleForm(FlaskForm):
    """Subform for roles"""
    role_id = HiddenField(validators=[DataRequired()])
    role_name = HiddenField(validators=[Optional()])


class UserForm(FlaskForm):
    """Main form for User GUI"""
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])
    email = StringField('Email', validators=[Optional(), Email()])
    password = PasswordField('Password')
    password2 = PasswordField(
        'Repeat Password', validators=[EqualTo('password')])
    groups = FieldList(FormField(GroupForm))
    group = SelectField(
        coerce=int, validators=[Optional()]
    )
    roles = FieldList(FormField(RoleForm))
    role = SelectField(
        coerce=int, validators=[Optional()]
    )

    submit = SubmitField('Save')

    def __init__(self, config_models, **kwargs):
        """Constructor

        :param ConfigModels config_models: Helper for ORM models
        """
        self.config_models = config_models
        self.User = self.config_models.model('users')

        # store any provided role object
        self.obj = kwargs.get('obj')

        super(UserForm, self).__init__(**kwargs)

    def validate_name(self, field):
        # check if role name exists
        session = self.config_models.session()
        query = session.query(self.User).filter_by(name=field.data)
        if self.obj:
            # ignore current role
            query = query.filter(self.User.id != self.obj.id)
        user = query.first()
        session.close()
        if user is not None:
            raise ValidationError('Name has already been taken.')

    def validate_email(self, email):
        session = self.config_models.session()
        query = session.query(self.User).filter_by(email=email.data)
        user = query.first()
        session.close()
        if user is not None and user != current_user:
            raise ValidationError('Please use a different email address.')