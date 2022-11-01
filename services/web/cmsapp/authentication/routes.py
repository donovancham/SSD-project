# -*- encoding: utf-8 -*-

from flask import render_template, redirect, request, url_for
from flask_login import (
    current_user,
    login_user,
    logout_user
)

from cmsapp import db, login_manager
from cmsapp.authentication import blueprint
from cmsapp.authentication.forms import LoginForm, CreateAccountForm, BookApptForm, CreateRecordForm, OTPForm
from cmsapp.authentication.models import Appointment, Users, Record

from cmsapp.authentication.util import verify_pass

# For 2FA
from cmsapp.authentication.cmstoken import generate_confirmation_token, confirm_token
from flask_mail import Message
from cmsapp.authentication.cmsemail import send_email
import pyotp


import sys
import datetime


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
            if user.confirmed:

                email = user.email

                secret = pyotp.random_base32()
                totp = pyotp.TOTP(secret)
                OTP_Pin = totp.now()

                user.otp = OTP_Pin
                db.session.add(user)
                db.session.commit()


       	        html = render_template("accounts/2fa.html", a_otp=OTP_Pin)
                subject = "Login OTP"
                send_email(email, subject, html)

                return redirect(url_for('authentication_blueprint.login_2FA',username=username))
            else:
                return redirect(url_for('authentication_blueprint.account_not_verified'))
        # Something (user or pass) is not ok
        return render_template('accounts/login.html',
                               msg='Wrong user or password',
                               form=login_form)

    if not current_user.is_authenticated:
        return render_template('accounts/login.html',
                               form=login_form)
    return redirect(url_for('home_blueprint.index'))


@blueprint.route('/login_2fa',methods=['GET','POST'])
def login_2FA():

    otp_form = OTPForm(request.form)

    if "auth_otp" in request.form:
        username = request.args['username']
        user = Users.query.filter_by(username=username).first()

        if int(request.form.get("otp")) == user.otp:
            login_user(user)

            # Reset OTP in db
            user.otp = None
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('authentication_blueprint.route_default'))

    return render_template('accounts/otp_auth.html', form=otp_form)




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

	# Token Generation for Registration Confirmation
        token = generate_confirmation_token(email)

	# Confirmation URL
        confirm_url = url_for("authentication_blueprint.confirm_email", token=token, _external=True)
        html = render_template("accounts/activation.html", confirm_url=confirm_url)
        subject = "Email Verification"

        send_email(email, subject, html)


        # Delete user from session
        logout_user()


        return render_template('accounts/register.html',
                               msg='Account created successfully.',
                               success=True,
                               form=create_account_form)

    else:
        return render_template('accounts/register.html', form=create_account_form)


# for 2FA confirmation
@blueprint.route('/confirm/<token>', methods=['GET'])
def confirm_email(token):

        url_buffer = ""

        email = confirm_token(token)
        if not email:
                url_buffer = "authentication_blueprint.confirmation_invalid"
        else:
                user = Users.query.filter_by(email=email).first_or_404()
                if user.confirmed:
                        url_buffer = "authentication_blueprint.confirmation_confirmed"
                else:
                        user.confirmed = True
                        user.confirmed_on = datetime.datetime.now()
                        db.session.add(user)
                        db.session.commit()
                        url_buffer = "authentication_blueprint.confirmation_success"
        return redirect(url_for(url_buffer))


@blueprint.route('/confirmation_success')
def confirmation_success():
    return render_template('accounts/account_confirmation_success.html')

@blueprint.route('/confirmation_confirmed')
def confirmation_confirmed():
    return render_template('accounts/account_confirmation_confirmed.html')

@blueprint.route('/confirmation_invalid')
def confirmation_invalid():
    return render_template('accounts/account_confirmation_invalid.html')

@blueprint.route('/not_verified')
def account_not_verified():
    return render_template('accounts/not_verified.html')

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

            inputName = request.form['inputName']
            inputCreatedBy = request.form['inputCreatedBy']

            newRecord = Record(dateCreated = defaultDate, createdBy = inputCreatedBy, patientName = inputName, patientNRIC = inputNRIC, description = inputDescription)
            db.session.add(newRecord)
            db.session.commit()
            return redirect('/viewRecord.html')

    return render_template('home/createRecord.html', segment="createRecord", form=form)


@blueprint.route('/viewAppointment.html')
def viewAppt():
    data = Appointment.query.all()

    return render_template('home/viewAppointment.html', segment="viewAppointment", data=data)

@blueprint.route('/changepassword.html')
def changepassword():

    return render_template('home/changepassword.html')

@blueprint.route('/viewRecord.html')
def viewRecord():
    data = Record.query.all()

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
