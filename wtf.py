from flask_wtf import FlaskForm
from wtforms import  DateField, FloatField, SubmitField
from wtforms.validators import DataRequired, ValidationError


class RegistrationForm(FlaskForm):
    date =DateField('date', validators=[DataRequired()])
    value = FloatField("value", validators=[DataRequired()])
    p_date =DateField('p_date', validators=[DataRequired()])
    p_value = FloatField('p_value', validators=[DataRequired()])
    
    submit = SubmitField('Register')

    def validate_value(self, value):
        if value.data < 0:
            raise ValidationError("Please use a different ")

    def validate_p_value(self, p_value):
        if p_value.data < 0:
            raise ValidationError("Please use a different ")