from wsgiref.validate import validator
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, DecimalField, BooleanField
from wtforms.validators import Length, DataRequired, ValidationError


class MyValidator(object):
    def __call__(self, form, field):
        all_names = [form.name1.data, form.name2.data, form.name3.data, form.name4.data]
        my_list = []
        duplicates = []
        for i in all_names:
            if i not in my_list:
                my_list.append(i)
            else:
                duplicates.append(i)
        if field.data in duplicates:
            raise ValidationError(
                f"Name {field.data} is used. Please input another name"
            )


class mj_form(FlaskForm):

    name1 = StringField(
        label="Player 1", validators=[Length(max=30), DataRequired(), MyValidator()]
    )
    name2 = StringField(
        label="Player 2", validators=[Length(max=30), DataRequired(), MyValidator()]
    )
    name3 = StringField(
        label="Player 3", validators=[Length(max=30), DataRequired(), MyValidator()]
    )
    name4 = StringField(
        label="Player 4", validators=[Length(max=30), DataRequired(), MyValidator()]
    )
    buy_in = IntegerField(label="Buy In Amount", validators=[DataRequired()])
    per_tai = DecimalField(label="Price per tai", validators=[DataRequired()])
    shooter = BooleanField(label="Shooter")
    submit = SubmitField(label="Done")


class mj_players(FlaskForm):
    submit = SubmitField(label="Confirm")


class gang(FlaskForm):
    submit = SubmitField(label="Confirm")
