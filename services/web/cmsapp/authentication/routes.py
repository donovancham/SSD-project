# -*- encoding: utf-8 -*-
from flask_wtf.csrf import CSRFError
from flask import render_template, redirect, request, url_for
from flask_login import (
    current_user,
    login_user,
    logout_user,
    login_required
)

from cmsapp import db, login_manager
from cmsapp.authentication import blueprint
from cmsapp.authentication.forms import LoginForm, CreateAccountForm, BookApptForm, CreateRecordForm, OTPForm, PWResetForm, PWResetFuncForm
from cmsapp.authentication.models import Appointment, Users, Record
from cmsapp import csrf
from cmsapp.authentication.util import verify_pass, password_complexity_checker

# For 2FA
from cmsapp.authentication.cmstoken import generate_confirmation_token, confirm_token
from flask_mail import Message
from cmsapp.authentication.cmsemail import send_email
import pyotp
from cmsapp.authentication.util import hash_pass



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

            # Checks to see if the user's Email is verified
            if user.confirmed:

                email = user.email

                # Creates a new OTP based on a random secret
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

    #if "auth_otp" in request.form:
    if request.method == "POST":
        username = request.args['username']
        user = Users.query.filter_by(username=username).first()

        if int(request.form.get("otp")) == user.otp:
            # Reset OTP in db
            user.otp = None
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('authentication_blueprint.route_default'))

    return render_template('accounts/otp_auth.html', form=otp_form)


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:

        username = request.form['username']
        email = request.form['email']
        nric= request.form['nric']
        password= request.form['password']

        # Check password with zxcvbn
        complexity, msg = password_complexity_checker(password)
        if complexity == False:
            return render_template('accounts/register.html',
                                   msg=msg,
                                   success=False,
                                   form=create_account_form)
        
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
                        url_buffer = "authentication_blueprint.confirmation_success"

                        db.session.add(user)
                        db.session.commit()

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


@blueprint.route('/password_reset', methods=['GET','POST'])
def password_reset():
    reset_form = PWResetForm()

    if request.method == "POST":
        email = request.values.get('email')

        user = Users.query.filter_by(email=email).first()

        if user != None:
            user.reset_request = True
            db.session.add(user)
            db.session.commit()

            # Token Generation for Registration Confirmation
            token = generate_confirmation_token(email)

    	    # Confirmation URL
            confirm_url = url_for("authentication_blueprint.password_reset_func", token=token, _external=True)
            html = render_template("accounts/pw_reset.html", confirm_url=confirm_url)
            subject = "Password Reset 2FA"

            send_email(email, subject, html)
            return redirect(url_for('authentication_blueprint.pw_reset_sent'))

    return render_template('accounts/password_reset_prompt.html',form=reset_form)


@blueprint.route('/password_reset_func/<token>',methods=['GET','POST'])
def password_reset_func(token):
        pass_reset_func = PWResetFuncForm()
        email = confirm_token(token)

        if not email:
                return redirect(url_for('authentication_blueprint.pw_reset_invalid'))

        else:
                user = Users.query.filter_by(email=email).first_or_404()
                if user.reset_request:
                    if "password" in request.form:
                        new_pass = request.form.get("newpw")
                        confirm_pass = request.form.get("confirmpw")

                        if new_pass == confirm_pass:
                            user.password = hash_pass(confirm_pass)
                            user.reset_request = False
                            db.session.add(user)
                            db.session.commit()
                            return redirect(url_for('authentication_blueprint.password_resetted'))

                else:
                    return redirect(url_for('authentication_blueprint.pw_reset_invalid'))


                return render_template('accounts/password_reset_func.html', form=pass_reset_func)


@blueprint.route('/pw_reset_sent')
def pw_reset_sent():
    return render_template('accounts/pw_reset_sent.html')


@blueprint.route('/pw_reset_invalid')
def pw_reset_invalid():
    return render_template('accounts/pw_reset_invalid.html')


@blueprint.route('/password_reset_successful')
def password_resetted():
    return render_template('accounts/password_reset_successful.html')



@blueprint.route('/bookAppointment.html', methods=['GET', 'POST'])
@login_required
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
@login_required
def createRecord():
    form = CreateRecordForm()
    if current_user.userrole == "Doctor":
        msg = ""
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
                    msg = "Incorrect NRIC"
                else:
                    newRecord = Record(dateCreated = defaultDate, createdBy = inputCreatedBy, patientName = inputName, patientNRIC = inputNRIC, description = inputDescription)
                    db.session.add(newRecord)
                    db.session.commit()
                    return redirect('/viewRecord.html')

        return render_template('home/createRecord.html', segment="createRecord", form=form, msg=msg)
    else:
        return redirect("/page-500.html")


@blueprint.route('/viewAppointment.html', methods=['GET', 'POST'])
@login_required
def viewAppt():
    data = Appointment.query.all()
    form = BookApptForm()
    if request.method == "POST":
        if "deleteApptBtn" in request.form:
            inputID = request.form["inputID"]
            entry = Appointment.query.get_or_404(int(inputID))
            db.session.delete(entry)
            db.session.commit()
            print("Entry deleted")

        elif "updateApptBtn" in request.form:
            inputID = request.form["inputID"]
            data = Appointment.query.get(int(inputID))
            return render_template('home/updateAppointment.html', segment="updateAppointment", data=data, form=form)

        return redirect("/viewAppointment.html")

    return render_template('home/viewAppointment.html', segment="viewAppointment", data=data, form=form)

@blueprint.route('/changepassword.html')
@login_required
def changepassword():

    return render_template('home/changepassword.html')

@blueprint.route('/viewRecord.html', methods=['GET', 'POST'])
@login_required
def viewRecord():
    form = CreateRecordForm()
    data = Record.query.all()
    if request.method == "POST":
        if "deleteApptBtn" in request.form:
            inputID = request.form["inputID"]
            entry = Record.query.get_or_404(int(inputID))
            db.session.delete(entry)
            db.session.commit()
            print("Entry deleted")
            
        elif "updateApptBtn" in request.form:
            inputID = request.form["inputID"]
            data = Record.query.get(int(inputID))
            return render_template('home/updateRecord.html', segment="updateRecord", data=data, form=form)

        return redirect("/viewRecord.html")

    return render_template('home/viewRecord.html', segment="viewRecord", data=data, form=form)

@blueprint.route('/updateRecord.html', methods=['GET', 'POST'])
@login_required
def updateRecord():
    form = CreateRecordForm()
    data = Record.query.all()
    if request.method == "POST":
        inputID = request.form["inputID"]
        defaultDate = request.form['defaultDate']
        inputNRIC = request.form['inputNRIC']
        inputDescription = request.form['inputDescription']
        inputName = request.form['inputName']
        inputCreatedBy = request.form['inputCreatedBy']

        entry = Record.query.get(int(inputID))
        entry.dateCreated = defaultDate
        entry.createdBy = inputCreatedBy
        entry.patientNRIC = inputNRIC
        entry.description = inputDescription
        entry.patientName = inputName

        db.session.commit()
        print("Entry updated")

        return redirect("/viewRecord.html")

    return render_template('home/updateRecord.html', segment="updateRecord", data=data, form=form)

@blueprint.route('/updateAppointment.html', methods=['GET', 'POST'])
@login_required
def updateAppt():
    form = BookApptForm()
    data = Appointment.query.all()
    if request.method == "POST":
        inputID = request.form["inputID"]
        inputDate = request.form['inputDate']
        inputTime = request.form['inputTime']
        inputDetail = request.form['inputDetail']
        inputNRIC = request.form['inputNRIC']
        inputName = request.form['inputName']

        entry = Appointment.query.get(int(inputID))
        entry.appointmentDate = inputDate
        entry.appointmentTime = inputTime
        entry.patientNRIC = inputNRIC
        entry.appointmentDetail = inputDetail
        entry.patientName = inputName

        db.session.commit()
        print("Entry updated")

        return redirect("/viewAppointment.html")

    return render_template('home/updateAppointment.html', segment="update", data=data, form=form)

# Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('home/page-403.html'), 403


#@blueprint.errorhandler(400)
#def input_forbidden(error):
#    return render_template('home/page-400.html'), 400


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500

@blueprint.errorhandler(CSRFError)
def csrf_error(reason):
    return render_template('home/page-403.html'), 403
