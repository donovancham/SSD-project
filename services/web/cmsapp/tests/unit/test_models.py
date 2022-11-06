from cmsapp.authentication.models import User, Appointment, Record
from datetime import datetime

def test_user_create(init_db):
    """
    GIVEN a User model
    WHEN new User is created
    THEN check email, username, NRIC is correct
    """
    # Given
    user = User(
        username = "patient1",
        userrole = "Patient",
        password = "pwd123",
        email = "email@email.email",
        nric = "349s",
        name = "Jacob",
    )
    
    # When
    init_db.session.add(user)
    
    # Then
    result = User.query.filter_by(email="email@email.email").first()
    assert result is user
    

def test_appointment_create(init_db):
    """
    GIVEN an Appointment model
    WHEN new Appointment is created
    THEN check appointmentDate, appointmentTime, patientName, 
    patientNRIC and appointmentDetail is correct
    """
    # Given

    nowDate = datetime.now.strftime("%Y-%m-%d")
    nowtime = datetime.now.strftime("%H:%M")
    inputDate = datetime.strptime(inputDate,'%Y-%m-%d').date()
    inputTime = datetime.strptime(inputTime,'%H:%M').time()

    inputDetail = "He's a little sick."
    inputNRIC = "123a"
    inputName = "Adam"
    
    appointment = Appointment(
        appointmentDate = inputDate, appointmentTime = inputTime, patientName = inputName, patientNRIC = inputNRIC, appointmentDetail = inputDetail
    )
    
    # When
    init_db.session.add(appointment)
    
    # Then
    result = Appointment.query.filter_by(patientNRIC="123a").first()
    assert result is appointment
