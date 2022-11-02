from flask_mail import Message

from cmsapp import mail

def send_email(to, subject, template):
        aSender = "Team10@3203SSGTeam10.com"
        msg = Message(
                subject,
                recipients=[to],
                html=template,
                sender=aSender
        )
        mail.send(msg)
