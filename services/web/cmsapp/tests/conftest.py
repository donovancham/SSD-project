import pytest
from cmsapp import create_app, db
from cmsapp.authentication.models import User

@pytest.fixture(scope="session")
def flask_app():
    # Initial setup
    app = create_app()
    
    testing_client = app.test_client()
    
    ctx = app.test_request_context()
    ctx.push()

    yield testing_client
    
    # Teardown processes
    ctx.pop()
  
  
@pytest.fixture(scope="session")
def init_db():
    # Create db and tables
    db.create_all()
    
    # Insert user data
    username = ["patient", "nurse", "doctor"]
    email = ["patient_abc_defg@gmail.com", "nurse@hospitao.com", "doctor@hospitao.ocm"]
    nric = ["123a", "234b", "345c"]
    password = ["pw1", "pw2", "pw3"]
    userroles = ["Patient", "Nurse", "Doctor"]
    name = ["Adam", "Betty", "Carl"]
    
    # Loop and add the 3 users
    for i in range(0,3):
        user = User(
            username = username[i],
            userrole = userroles[i],
            password = password[i],
            email = email[i],
            nric = nric[i],
            name = name[i],
        )
        
        # Add existing appointment for patient
        # Add existing record for patient
        
        db.session.add(user)
    
    yield db
    
    db.session.commit()
    db.drop_all()