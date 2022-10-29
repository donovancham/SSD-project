# -*- encoding: utf-8 -*-

from flask_login import UserMixin

from cmsapp import db, login_manager

from cmsapp.authentication.util import hash_pass

class Users(db.Model, UserMixin):

    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.LargeBinary)
    userrole=db.Column(db.String(64))
    nric=db.Column(db.String(64), unique=True)
    name=db.Column(db.String(64))

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass(value)  # we need bytes here (not plain str)

            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)


@login_manager.user_loader
def user_loader(id):
    return Users.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = Users.query.filter_by(username=username).first()
    return user if user else None

class Appointment(db.Model):
    __tablename__ = 'Appointment'
    appointmentID = db.Column(db.Integer, primary_key=True)
    appointmentDate = db.Column(db.String(64), nullable = False)
    appointmentTime = db.Column(db.String(64), nullable = False)
    patientName = db.Column(db.String(64), nullable = False)
    patientNRIC = db.Column(db.String(64), nullable = False)
    appointmentDetail = db.Column(db.String(64), nullable = False)

class Record(db.Model):
    __tablename__ = 'Record'
    recordID = db.Column(db.Integer, primary_key=True)
    dateCreated = db.Column(db.String(64), nullable = False)
    createdBy = db.Column(db.String(64), nullable = False)
    patientName = db.Column(db.String(64), nullable = False)
    patientNRIC = db.Column(db.String(64), nullable = False)
    description = db.Column(db.String(64), nullable = False)
