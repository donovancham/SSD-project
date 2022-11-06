from flask.cli import FlaskGroup
from cmsapp import app, db
import click
import os

from cmsapp.authentication.models import User


cli = FlaskGroup(app)

# Additional argument to create db
@cli.command("create_db")
def create_db():
    db.create_all()
    db.session.commit()
  
@cli.command("delete_db")
def delete_db():
    db.drop_all()
    db.session.commit()
    
# @cli.command("seed_db")
# def seed_db():
#     db.session.add(User(email="michael@mherman.org"))
#     db.session.commit()


@cli.command("add_user")
@click.argument("role", nargs=1)
@click.argument("email", nargs=1)
def add_user(role, inputEmail):
    DOCTOR_USER = os.getenv('DOCTOR_USER')
    DOCTOR_PASS = os.getenv('DOCTOR_PASS')
    DOCTOR_NRIC = os.getenv('DOCTOR_NRIC')
    NURSE_USER = os.getenv('NURSE_USER')
    NURSE_PASS = os.getenv('NURSE_PASS')
    NURSE_NRIC = os.getenv('NURSE_NRIC')
    
    aDoctor = {
        'username': DOCTOR_USER,
        'nric': DOCTOR_NRIC,
        'password': DOCTOR_PASS,
        'userroles':"Doctor",
        'name':"Docter Raymond"
    }

    aNurse = {
        'username': NURSE_USER,
        'nric': NURSE_NRIC,
        'password': NURSE_PASS,
        'userroles':"Nurse",
        'name':"A Nurse"
    }


    if role.lower() == "doctor":
        newUser = User(username=aDoctor['username'], userrole=aDoctor['userroles'], password=aDoctor['password'], email=inputEmail, nric=aDoctor['nric'], name=aDoctor['name'], confirmed=True)
        db.session.add(newUser)
        # print("Username: {}".format(newUser.username))
        # print("Password: {}".format(aDoctor['password']))
        # print("Email: {}".format(newUser.email))


    elif role.lower() == "nurse":
        newUser = User(username=aNurse['username'], userrole=aNurse['userroles'], password=aNurse['password'], email=inputEmail, nric=aNurse['nric'], name=aNurse['name'], confirmed=True)
        db.session.add(newUser)
        # print("Username: {}".format(newUser.username))
        # print("Password: {}".format(aNurse['password']))
        # print("Email: {}".format(newUser.email))

    else:
        print("No user created")
        return 0

    db.session.commit()


if __name__ == "__main__":
    cli()
