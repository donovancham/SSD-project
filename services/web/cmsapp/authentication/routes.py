# -*- encoding: utf-8 -*-
from flask_wtf.csrf import CSRFError
from flask import render_template, redirect, request, url_for, session
from flask_login import (
    current_user,
    login_user,
    logout_user,
    login_required,
    login_manager
)

from cmsapp import db, login_manager, authorize, talisman
from cmsapp.authentication import blueprint
from cmsapp.authentication.forms import LoginForm, CreateAccountForm, BookApptForm, CreateRecordForm, OTPForm, PWResetForm, PWResetFuncForm
from cmsapp.authentication.models import Appointment, User, Record, Role, Group
from cmsapp.authentication.util import verify_pass, password_complexity_checker

# For 2FA
from cmsapp.authentication.cmstoken import generate_confirmation_token, confirm_token
from flask_mail import Message
from cmsapp.authentication.cmsemail import send_email
import pyotp
from cmsapp.authentication.util import hash_pass

from base64 import b64encode
from os import urandom
import datetime


@blueprint.route('/')
@talisman()
def route_default():
    return redirect(url_for('authentication_blueprint.login'))


# Login & Registration

@blueprint.route('/login', methods=['GET', 'POST'])
@talisman()
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:
        # read form data
        username = request.form['username'].upper()
        password = request.form['password']

        # Locate user
        user = User.query.filter_by(username=username).first()

        # Check the password
        if user and verify_pass(password, user.password):

            # Checks to see if the user's Email is verified
            if user.confirmed:

                email = user.email.upper()

                # Creates a new OTP based on a random secret
                secret = pyotp.random_base32()
                totp = pyotp.TOTP(secret, interval=320)
                OTP_Pin = totp.now()

                user.otp = secret
                db.session.add(user)
                db.session.commit()

                html = render_template("accounts/2fa.html", a_otp=OTP_Pin)
                subject = "Login OTP"
                send_email(email, subject, html)

                return redirect(url_for('authentication_blueprint.login_2FA', username=username))
            else:
                return redirect(url_for('authentication_blueprint.account_not_verified'))
        # Something (user or pass) is not ok
        return render_template('accounts/login.html',
                               msg='Wrong user or password',
                               form=login_form)

    if not current_user.is_authenticated:
        return render_template('accounts/login.html',
                               form=login_form)
    return redirect(url_for('authentication_blueprint.viewAppt'))


@blueprint.route('/login_2fa', methods=['GET', 'POST'])
@talisman()
def login_2FA():
    otp_form = OTPForm(request.form)

    # if "auth_otp" in request.form:
    if request.method == "POST":
        username = request.args['username']
        user = User.query.filter_by(username=username).first()

        input_otp = request.form.get("otp")

        if pyotp.TOTP(user.otp, interval=320).verify(input_otp):
            # Reset OTP secret in db
            user.otp = None
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('authentication_blueprint.viewAppt'))

    return render_template('accounts/otp_auth.html', form=otp_form)


@blueprint.route('/register', methods=['GET', 'POST'])
@talisman()
def register():
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:

        username = request.form['username'].upper()
        email = request.form['email'].upper()
        nric = request.form['nric'].upper()
        password = request.form['password']
        userroles = "Patient"
        name = request.form['name'].upper()

        # Check password with zxcvbn
        complexity, msg = password_complexity_checker(password)
        if complexity == False:
            return render_template('accounts/register.html',
                                   msg=msg,
                                   success=False,
                                   form=create_account_form)

        # Check usename exists
        user = User.query.filter_by(username=username).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Username already registered',
                                   success=False,
                                   form=create_account_form)

        # Check email exists
        user = User.query.filter_by(email=email).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Email already registered',
                                   success=False,
                                   form=create_account_form)
        # Check nric exists
        user = User.query.filter_by(nric=nric).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='NRIC already registered',
                                   success=False,
                                   form=create_account_form)

        # else we can create the user
        user = User(username=username, userrole=userroles,
                    password=password, email=email, nric=nric, name=name)
        db.session.add(user)

        # Check user group and role and configure role in db\
        user = User.query.filter_by(username=username).first()

        if userroles == 'Patient':
            roles = ['Patient']
            q = Role.query.filter_by(name=roles[0]).first()
            if q:
                roles.append(q)
            else:
                roles.append(Role(name="Patient"))
            db.session.add(roles[-1])
            user.roles.append(roles[-1])
            db.session.flush()

        # configure  groups
        if userroles == 'Patient':
            groups = ['PatientGroup']
            q = Group.query.filter_by(name=groups[0]).first()
            if q:
                groups.append(q)
            else:
                groups.append(Group(name="PatientGroup"))
            db.session.add(groups[-1])
            user.groups.append(groups[-1])
            db.session.flush()

        db.session.commit()

        # Token Generation for Registration Confirmation
        token = generate_confirmation_token(email)

        # Confirmation URL
        confirm_url = url_for(
            "authentication_blueprint.confirm_email", token=token, _external=True)
        html = render_template("accounts/activation.html",
                               confirm_url=confirm_url)
        subject = "Email Verification"

        send_email(email, subject, html)

        # Delete user from session
        logout_user()

        return render_template('accounts/register.html',
                               msg='Account created successfully.\nClick the link in your email to activate your account',
                               success=True,
                               form=create_account_form)

    else:
        return render_template('accounts/register.html', form=create_account_form)


# for 2FA confirmation
@blueprint.route('/confirm/<token>', methods=['GET'])
@talisman()
def confirm_email(token):

    url_buffer = ""

    email = confirm_token(token)

    if not email:
        url_buffer = "authentication_blueprint.confirmation_invalid"
    else:
        user = User.query.filter_by(email=email).first_or_404()

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
@talisman()
def confirmation_success():
    return render_template('accounts/account_confirmation_success.html')


@blueprint.route('/confirmation_confirmed')
@talisman()
def confirmation_confirmed():
    return render_template('accounts/account_confirmation_confirmed.html')


@blueprint.route('/confirmation_invalid')
@talisman()
def confirmation_invalid():
    return render_template('accounts/account_confirmation_invalid.html')


@blueprint.route('/not_verified')
@talisman()
def account_not_verified():
    return render_template('accounts/not_verified.html')


@blueprint.route('/logout')
@talisman()
def logout():
    logout_user()
    return redirect(url_for('authentication_blueprint.login'))


@blueprint.route('/password_reset', methods=['GET', 'POST'])
@talisman()
def password_reset():
    reset_form = PWResetForm()

    if request.method == "POST":
        email = request.values.get('email').upper()

        user = User.query.filter_by(email=email).first()

        if user != None:
            user.reset_request = True
            db.session.add(user)
            db.session.commit()

            # Token Generation for Registration Confirmation
            token = generate_confirmation_token(email)

            # Confirmation URL
            confirm_url = url_for(
                "authentication_blueprint.password_reset_func", token=token, _external=True)
            html = render_template(
                "accounts/pw_reset.html", confirm_url=confirm_url)
            subject = "Password Reset 2FA"

            send_email(email, subject, html)
            return redirect(url_for('authentication_blueprint.pw_reset_sent'))

    return render_template('accounts/password_reset_prompt.html', form=reset_form)


@blueprint.route('/password_reset_func/<token>', methods=['GET', 'POST'])
@talisman()
def password_reset_func(token):
    pass_reset_func = PWResetFuncForm()
    email = confirm_token(token)

    if not email:
        return redirect(url_for('authentication_blueprint.pw_reset_invalid'))

    else:
        user = User.query.filter_by(email=email).first_or_404()
        if user.reset_request:
            if "password" in request.form:
                new_pass = request.form.get("newpw")
                confirm_pass = request.form.get("confirmpw")

                if new_pass == confirm_pass:
                    # Check password with zxcvbn
                    complexity, msg = password_complexity_checker(new_pass)
                    if complexity == False:
                        return render_template('accounts/password_reset_func.html', form=pass_reset_func, msg=msg)

                    user.password = hash_pass(confirm_pass)
                    user.reset_request = False
                    db.session.add(user)
                    db.session.commit()
                    return redirect(url_for('authentication_blueprint.password_resetted'))

        else:
            return redirect(url_for('authentication_blueprint.pw_reset_invalid'))

    return render_template('accounts/password_reset_func.html', form=pass_reset_func)


@blueprint.route('/pw_reset_sent')
@talisman()
def pw_reset_sent():
    return render_template('accounts/pw_reset_sent.html')


@blueprint.route('/pw_reset_invalid')
@talisman()
def pw_reset_invalid():
    return render_template('accounts/pw_reset_invalid.html')


@blueprint.route('/password_reset_successful')
@talisman()
def password_resetted():
    return render_template('accounts/password_reset_successful.html')


@blueprint.route('/bookAppointment.html', methods=['GET', 'POST'])
@talisman()
@login_required
def bookAppt():
    if current_user.userrole == "Doctor":
        return redirect("/page-500.html")
    else:
        form = BookApptForm()

        if request.method == "POST":
            inputDate = request.form['inputDate']
            inputTime = request.form['inputTime']
            inputDetail = request.form['inputDetail']

            if current_user.userrole == "Nurse":
                inputNRIC = request.form['inputNRIC'].upper()
            elif current_user.userrole == "Patient":
                inputNRIC = current_user.nric
            
            if User.query.filter_by(nric=inputNRIC).first() is None:
                return render_template('home/bookAppointment.html', segment="bookAppointment", form=form, msg="Invalid NRIC")

            try:
                inputDate = datetime.datetime.strptime(inputDate, '%Y-%m-%d').date()
                inputTime = datetime.datetime.strptime(inputTime, '%H:%M').time()
                
                if current_user.userrole == "Patient":
                    allAppointments = Appointment.query.filter_by(patientNRIC=current_user.nric)
                    if allAppointments is not None:
                        for aEntry in allAppointments:
                            if aEntry.appointmentDate == inputDate and aEntry.appointmentTime == inputTime:
                                return render_template('home/bookAppointment.html', segment="bookAppointment", form=form, msg="Appointment already exists")
                            
                    newAppt = Appointment(appointmentDate=inputDate, appointmentTime=inputTime,
                                      patientName=current_user.name, patientNRIC=current_user.nric, appointmentDetail=inputDetail)
                    db.session.add(newAppt)
                    db.session.commit()
                
                if current_user.userrole == "Nurse":
                    allAppointments = Appointment.query.filter_by(patientNRIC=inputNRIC)
                    if allAppointments is not None:
                        for aEntry in allAppointments:
                            if aEntry.appointmentDate == inputDate and aEntry.appointmentTime == inputTime:
                                return render_template('home/bookAppointment.html', segment="bookAppointment", form=form, msg="Appointment already exists")
                    
                    user = User.query.filter_by(nric=inputNRIC).first()
                    
                    newAppt = Appointment(appointmentDate=inputDate, appointmentTime=inputTime,
                                      patientName=user.name, 
                                      patientNRIC=user.nric, appointmentDetail=inputDetail)
                    db.session.add(newAppt)
                    db.session.commit()

                return redirect('/viewAppointment.html')
            except:
                return render_template('home/bookAppointment.html', segment="bookAppointment", form=form)

        return render_template('home/bookAppointment.html', segment="bookAppointment", form=form)


@blueprint.route('/createRecord.html', methods=['GET', 'POST'])
@talisman()
@login_required
def createRecord():
    form = CreateRecordForm()
    # RBAC check if user is a Doctor
    if not authorize.has_role("Doctor"):
        return redirect("/page-403.html")

    if current_user.userrole == "Doctor":
        msg = ""
        if request.method == "POST":
            defaultDate = request.form['defaultDate']
            inputNRIC = request.form['inputNRIC'].upper()
            inputDescription = request.form['inputDescription']

            inputName = ""
            inputCreatedBy = request.form['inputCreatedBy']
            
            if User.query.filter_by(nric=inputNRIC).first() is None:
                render_template('home/createRecord.html', segment="createRecord", form=form, msg=msg)

            checkUsers = Appointment.query.all()
            for eachUser in checkUsers:
                if eachUser.patientNRIC == inputNRIC:
                    inputName = eachUser.patientName

            if (inputName == ""):
                msg = "Incorrect NRIC"
            else:
                try:
                    defaultDate = datetime.datetime.strptime(defaultDate, '%Y-%m-%d').date()
                    newRecord = Record(dateCreated=defaultDate, createdBy=inputCreatedBy,
                                    patientName=inputName, patientNRIC=inputNRIC, description=inputDescription)
                    db.session.add(newRecord)
                    db.session.commit()
                    return redirect('/viewRecord.html')
                except:
                    return render_template('home/createRecord.html', segment="createRecord", form=form, msg="Incorrect date.")

        return render_template('home/createRecord.html', segment="createRecord", form=form, msg=msg)
    else:
        return redirect("/page-500.html")


@blueprint.route('/viewAppointment.html', methods=['GET', 'POST'])
@talisman()
@login_required
def viewAppt():
    data = None
    if current_user.userrole == "Patient":
        data = Appointment.query.filter_by(patientNRIC=current_user.nric)
    elif current_user.userrole == "Nurse" or current_user.userrole == "Doctor":
        data = Appointment.query.all()
    
    if data == None:
        return redirect("/viewAppointment.html")
    
    mask = {}
    for apt in data:
        random_bytes = urandom(64)
        token = b64encode(random_bytes).decode('utf-8')
        mask[apt.appointmentID] = token
    
    form = BookApptForm()
    if request.method == "POST":
        # RBAC check if user is a Patient or Nurse
        if not authorize.has_role("Nurse") and not authorize.has_role("Patient"):
            return redirect("/page-403.html")
        
        if "deleteApptBtn" in request.form:
            try:
                mask = session['currentmask']
                inputID = list(mask.keys())[list(mask.values()).index(request.form["inputID"])]
                entry = Appointment.query.get_or_404(int(inputID))
                db.session.delete(entry)
                db.session.commit()
            except:
                return render_template('home/viewAppointment.html', segment="viewAppointment", data=data, form=form, mask=mask, msg="Error deleting data.")

        elif "updateApptBtn" in request.form:
            mask = session['currentmask']
            inputID = list(mask.keys())[list(mask.values()).index(request.form["inputID"])]
            data: Appointment = Appointment.query.get(int(inputID))
            session['update_appointment'] = data.appointmentID
            return render_template('home/updateAppointment.html', segment="updateAppointment", data=data, form=form, mask=mask)

        return redirect("/viewAppointment.html")
    else:
        session['update_appointment'] = None
    
    session['currentmask'] = mask

    return render_template('home/viewAppointment.html', segment="viewAppointment", data=data, form=form, mask=mask)


@blueprint.route('/viewRecord.html', methods=['GET', 'POST'])
@talisman()
@login_required
def viewRecord():
    data = None
    if current_user.userrole == "Patient":
        data = Record.query.filter_by(patientNRIC=current_user.nric)
    elif current_user.userrole == "Nurse" or current_user.userrole == "Doctor":
        data = Record.query.all()
    
    if data == None:
        return redirect("/viewRecord.html")
    
    mask = {}
    for apt in data:
        random_bytes = urandom(64)
        token = b64encode(random_bytes).decode('utf-8')
        mask[apt.recordID] = token
    
    form = CreateRecordForm()
    if request.method == "POST":
        # RBAC check if user is a Doctor
        if not authorize.has_role("Doctor"):
            return redirect("/page-403.html")
        
        if "deleteApptBtn" in request.form:
            try:
                mask = session['currentmask']
                inputID = list(mask.keys())[list(mask.values()).index(request.form["inputID"])]
                entry = Record.query.get_or_404(int(inputID))
                db.session.delete(entry)
                db.session.commit()
            except:
                return render_template('home/viewRecord.html', segment="viewAppointment", data=data, form=form, mask=mask, msg="Error deleting data.")

        elif "updateApptBtn" in request.form:
            mask = session['currentmask']
            inputID = list(mask.keys())[list(mask.values()).index(request.form["inputID"])]
            data = Record.query.get(int(inputID))
            session['update_record'] = data.recordID
            return render_template('home/updateRecord.html', segment="updateRecord", data=data, form=form, mask=mask)

        return redirect("/viewRecord.html")
    else:
        session['update_record'] = None
    
    session['currentmask'] = mask
    
    return render_template('home/viewRecord.html', segment="viewRecord", data=data, form=form, mask=mask)


@blueprint.route('/updateRecord.html', methods=['GET', 'POST'])
@talisman()
@login_required
def updateRecord():
    # RBAC check if user is a Doctor
    if not authorize.has_role("Doctor"):
        return redirect("/page-403.html")

    form = CreateRecordForm()
    data = Record.query.get(int(session['update_record']))
    if data == None:
        return redirect("/viewRecord.html")
    if request.method == "POST":
        try:
            defaultDate = request.form['defaultDate']
            inputDescription = request.form['inputDescription']

            entry = Record.query.get(int(data.recordID))
            entry.dateCreated = datetime.datetime.strptime(defaultDate, '%Y-%m-%d').date()
            entry.createdBy = data.createdBy
            entry.patientNRIC = data.patientNRIC
            entry.description = inputDescription
            entry.patientName = data.patientName

            db.session.commit()

            return redirect("/viewRecord.html")
        except:
            return render_template('home/updateRecord.html', segment="update", data=data, form=form, msg="Invalid date entered.")

    return render_template('home/updateRecord.html', segment="updateRecord", data=data, form=form)


@blueprint.route('/updateAppointment.html', methods=['GET', 'POST'])
@talisman()
@login_required
def updateAppt():
    # RBAC check if user is a Nurse of Patient
    if not authorize.has_role("Patient") and not authorize.has_role("Nurse"):
        return redirect("/page-403.html")
    form = BookApptForm()
    data = Appointment.query.get(int(session['update_appointment']))
    if data == None:
        return redirect("/viewAppointment.html")
    if request.method == "POST":
        inputDate = request.form['inputDate']
        inputTime = request.form['inputTime']
        inputDetail = request.form['inputDetail']

        try:
            inputDate = datetime.datetime.strptime(inputDate, '%Y-%m-%d').date()
            inputTime = datetime.datetime.strptime(inputTime, '%H:%M').time()
            
            allAppointments = Appointment.query.filter_by(patientNRIC=data.patientNRIC)

            if allAppointments is not None:
                for aEntry in allAppointments:
                    if aEntry.appointmentDate == inputDate and aEntry.appointmentTime == inputTime:
                        return render_template('home/updateAppointment.html', segment="update", data=data, form=form, msg="This timeslot is taken!")

            entry = Appointment.query.get(int(data.appointmentID))
            entry.appointmentDate = inputDate
            entry.appointmentTime = inputTime
            entry.patientNRIC = data.patientNRIC
            entry.appointmentDetail = inputDetail
            entry.patientName = data.patientName

            db.session.commit()

            return redirect("/viewAppointment.html")
        except:
            return render_template('home/updateAppointment.html', segment="update", data=data, form=form, msg="Invalid date entered.")

    return render_template('home/updateAppointment.html', segment="update", data=data, form=form)

# Errors


@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('home/page-403.html'), 403


# @blueprint.errorhandler(400)
# def input_forbidden(error):
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