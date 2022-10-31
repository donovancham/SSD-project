# -*- encoding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, TimeField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Email

# login and registration


class LoginForm(FlaskForm):
    username = StringField('Username',
                         id='username_login',
                         validators=[DataRequired()])
    password = PasswordField('Password',
                             id='pwd_login',
                             validators=[DataRequired()])


class CreateAccountForm(FlaskForm):
    username = StringField('Username', 
                           id='username_create', 
                           validators=[DataRequired()])
    email = StringField('Email', 
                        id='email_create', 
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', 
                             id='pwd_create',
                             validators=[DataRequired(), Length(min=6, max=40)])
    userrole = SelectField("userrole", validators=[DataRequired()],
                                            choices =['Doctor', 'Patient', 'Nurse'])   
    nric = StringField('nric', 
                           id='nric_create', 
                           validators=[DataRequired(), Length(min=4, max=4)])   
    name = StringField('name', 
                           id='name_create', 
                           validators=[DataRequired()])

                             

class BookApptForm(FlaskForm):
    inputDate = DateField(label='inputDate:', validators=[ DataRequired()])
    inputTime = SelectField("inputTime", validators=[DataRequired()],
                                            choices =['08:00', '08:30', '09:00', '09:30', '10:00', '10:30',
                                            '11:00', '11:30', '12:00', '12:30', '13:00', '13:30',
                                            '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00'])
    inputDetail = SelectField("inputDetail", validators=[DataRequired()],
                                            choices =['Eye Checkup', 'Heart Checkup', 'Body Checkup'])
    inputNRIC = StringField('inputNRIC', id='inputNRIC', validators=[DataRequired()])
    inputName = StringField('inputName', id='inputName', validators=[DataRequired()])

class CreateRecordForm(FlaskForm):
    defaultDate = StringField('defaultDate', id='defaultDate', validators=[DataRequired()])
    inputNRIC = StringField('inputNRIC', id='inputNRIC', validators=[DataRequired()])
    inputDescription = StringField('inputDescription', id='inputDescription', validators=[DataRequired()])
    inputCreatedBy = StringField('inputCreatedBy', id='inputCreatedBy', validators=[DataRequired()])