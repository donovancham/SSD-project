# -*- encoding: utf-8 -*-

from flask import render_template, redirect, request, url_for, flash
from flask_login import (
    current_user,
    login_user,
    logout_user
)

from apps import db, login_manager
from apps.authentication import blueprint
from apps.authentication.forms import LoginForm, CreateAccountForm, BookApptForm, CreateRecordForm
from apps.authentication.models import Appointment, Users, Record

from apps.authentication.util import verify_pass

import sys


@blueprint.route('/')
def route_default():
    return redirect(url_for('authentication_blueprint.login'))


# Login & Registration

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:

        # read form data
        username = request.form['username']
        password = request.form['password']

        # Locate user
        user = Users.query.filter_by(username=username).first()

        # Check the password
        if user and verify_pass(password, user.password):

            login_user(user)
            return redirect(url_for('authentication_blueprint.route_default'))

        # Something (user or pass) is not ok
        return render_template('accounts/login.html',
                               msg='Wrong user or password',
                               form=login_form)

    if not current_user.is_authenticated:
        return render_template('accounts/login.html',
                               form=login_form)
    return redirect(url_for('home_blueprint.index'))


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:

        username = request.form['username']
        email = request.form['email']
        nric= request.form['nric']

        # Check usename exists
        user = Users.query.filter_by(username=username).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Username already registered',
                                   success=False,
                                   form=create_account_form)

        # Check email exists
        user = Users.query.filter_by(email=email).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Email already registered',
                                   success=False,
                                   form=create_account_form)
        # Check nric exists
        user = Users.query.filter_by(nric=nric).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Nric already registered',
                                   success=False,
                                   form=create_account_form)

        # else we can create the user
        user = Users(**request.form)
        db.session.add(user)
        db.session.commit()
        
        # Delete user from session
        logout_user()        

        return render_template('accounts/register.html',
                               msg='Account created successfully.',
                               success=True,
                               form=create_account_form)

    else:
        return render_template('accounts/register.html', form=create_account_form)


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('authentication_blueprint.login'))


@blueprint.route('/bookAppointment.html', methods=['GET', 'POST'])
def bookAppt():
    form = BookApptForm()
    if request.method == "POST":
        #if form.validate_on_submit():
            inputDate = request.form['inputDate']
            inputTime = request.form['inputTime']
            inputDetail = request.form['inputDetail']

            inputNRIC = request.form['inputNRIC']
            inputName = request.form['inputName']

            newAppt = Appointment(appointmentDate = inputDate, appointmentTime = inputTime, patientName = inputName, patientNRIC = inputNRIC, appointmentDetail = inputDetail)
            db.session.add(newAppt)
            db.session.commit()

            return redirect('/viewAppointment.html')

    return render_template('home/bookAppointment.html', segment="bookAppointment", form=form)

@blueprint.route('/createRecord.html', methods=['GET', 'POST'])
def createRecord():
    form = CreateRecordForm()
    if request.method == "POST":
        #if form.validate_on_submit():
            defaultDate = request.form['defaultDate']
            inputNRIC = request.form['inputNRIC']
            inputDescription = request.form['inputDescription']

            # inputName = request.form['inputName']
            inputName = ""
            inputCreatedBy = request.form['inputCreatedBy']

            checkUsers = Appointment.query.all()
            for eachUser in checkUsers:
                if eachUser.patientNRIC == inputNRIC:
                    inputName = eachUser.patientName

            if (inputName == ""):
                print("No such NRIC in User Database")
            else:
                newRecord = Record(dateCreated = defaultDate, createdBy = inputCreatedBy, patientName = inputName, patientNRIC = inputNRIC, description = inputDescription)
                db.session.add(newRecord)
                db.session.commit()
                return redirect('/viewRecord.html')

    return render_template('home/createRecord.html', segment="createRecord", form=form)


@blueprint.route('/viewAppointment.html', methods=['GET', 'POST'])
def viewAppt():
    data = Appointment.query.all()
    if request.method == "POST":
        inputID = request.form["inputID"]
        entry = Appointment.query.get_or_404(int(inputID))
        db.session.delete(entry)
        db.session.commit()
        print("Entry deleted")
        return redirect("/viewAppointment.html")

    return render_template('home/viewAppointment.html', segment="viewAppointment", data=data)

@blueprint.route('/changepassword.html')
def changepassword():

    return render_template('home/changepassword.html')

@blueprint.route('/viewRecord.html', methods=['GET', 'POST'])
def viewRecord():
    data = Record.query.all()
    if request.method == "POST":
        inputID = request.form["inputID"]
        entry = Record.query.get_or_404(int(inputID))
        db.session.delete(entry)
        db.session.commit()
        print("Entry deleted")
        return redirect("/viewRecord.html")

    return render_template('home/viewRecord.html', segment="viewRecord", data=data)

# Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500