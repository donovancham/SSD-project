# -*- encoding: utf-8 -*-

from flask_login import UserMixin

from cmsapp import db, login_manager

from cmsapp.authentication.util import hash_pass

from flask_authorize import RestrictionsMixin, AllowancesMixin
from flask_authorize import PermissionsMixin

# mapping tables
UserGroup = db.Table(
    'user_group', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('Users.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('Groups.id'))
)


UserRole = db.Table(
    'user_role', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('Users.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('Roles.id'))
)

# Group and Role table for RBAC 
class Group(db.Model, RestrictionsMixin):
    __tablename__ = 'Groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    users = db.relationship('User', secondary=UserGroup)

class Role(db.Model, RestrictionsMixin):
    __tablename__ = 'Roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    users = db.relationship('User', secondary=UserRole)

# User table
class User(db.Model, UserMixin):

    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True, index=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.LargeBinary)
    # userrole=db.Column(db.String(64))
    roles=db.relationship('Role', secondary=UserRole)
    groups = db.relationship('Group', secondary=UserGroup)
    nric=db.Column(db.String(64), unique=True)
    name=db.Column(db.String(64))

    # For 2FA
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    otp = db.Column(db.Integer)
    reset_request = db.Column(db.Boolean, nullable=False, default=False)


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
    return User.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    return user if user else None

class Appointment(db.Model):
    __tablename__ = 'Appointment'
    __permissions__ = dict(
        owner=['read', 'update', 'delete'],
        group=['read', 'update'],
        other=['read']
    )
    
    appointmentID = db.Column(db.Integer, primary_key=True)
    appointmentDate = db.Column(db.String(64), nullable = False)
    appointmentTime = db.Column(db.String(64), nullable = False)
    patientName = db.Column(db.String(64), nullable = False)
    patientNRIC = db.Column(db.String(64), nullable = False)
    appointmentDetail = db.Column(db.String(64), nullable = False)

class Record(db.Model, PermissionsMixin):
    __tablename__ = 'Record'
    __permissions__ = dict(
        owner=['read', 'update', 'delete'],
        group=['read', 'update'],
        other=['read']
    )

    recordID = db.Column(db.Integer, primary_key=True)
    dateCreated = db.Column(db.String(64), nullable = False)
    createdBy = db.Column(db.String(64), nullable = False)
    patientName = db.Column(db.String(64), nullable = False)
    patientNRIC = db.Column(db.String(64), nullable = False)
    description = db.Column(db.String(64), nullable = False)
