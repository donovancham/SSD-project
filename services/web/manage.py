from flask.cli import FlaskGroup
from cmsapp import app, db

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

if __name__ == "__main__":
    cli()