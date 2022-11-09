from flask.cli import FlaskGroup
from cmsapp import app, db
import click
from cmsapp.authentication.models import User, Role, Group

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


@cli.command("add_user")
@click.option('--role', type=str, required=True)
@click.option('--username', type=str, required=True)
@click.option('--password', type=str, required=True)
@click.option('--nric', type=str, required=True)
@click.option('--name', type=str, required=True)
@click.argument('email', nargs=1, type=str, required=True)
def add_user(role: str, username: str, password: str, nric: str, name: str, email: str):

    if role.lower() == "doctor":
        newUser = User(
            username=username.upper(), 
            userrole="Doctor", 
            password=password, 
            email=email.upper(), 
            nric=nric.upper(), 
            name=name.upper(), 
            confirmed=True
        )
        
        db.session.add(newUser)
        
        # Update role permission
        roles = ['Doctor']
        q = Role.query.filter_by(name=roles[0]).first()
        if q:
            roles.append(q)
        else:
            roles.append(Role(name="Doctor"))
        
        db.session.add(roles[-1])
        newUser.roles.append(roles[-1])
        db.session.flush()
        
        # Update role group
        groups = ['DoctorGroup']
        
        q = Group.query.filter_by(name=groups[0]).first()
        if q:
            groups.append(q)
        else:
            groups.append(Group(name="DoctorGroup"))
        
        db.session.add(groups[-1])
        newUser.groups.append(groups[-1])
        db.session.flush()


    elif role.lower() == "nurse":
        newUser = User(
            username=username.upper(), 
            userrole="Nurse", 
            password=password, 
            email=email.upper(), 
            nric=nric.upper(), 
            name=name.upper(), 
            confirmed=True
        )
        
        db.session.add(newUser)
        
        # Update role permissions
        roles = ['Nurse']
        q = Role.query.filter_by(name=roles[0]).first()
        if q:
            roles.append(q)
        else:
            roles.append(Role(name="Nurse"))
        
        db.session.add(roles[-1])
        newUser.roles.append(roles[-1])
        db.session.flush()
        
        # Update role group
        groups = ['NurseGroup']
        
        q = Group.query.filter_by(name=groups[0]).first()
        if q:
            groups.append(q)
        else:
            groups.append(Group(name="NurseGroup"))
        
        db.session.add(groups[-1])
        newUser.groups.append(groups[-1])
        db.session.flush()

    else:
        print("No user created")
        return 0

    db.session.commit()


if __name__ == "__main__":
    cli()