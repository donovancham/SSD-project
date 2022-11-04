from itsdangerous import URLSafeTimedSerializer
import os


def generate_confirmation_token(email):
	serializer = URLSafeTimedSerializer( os.getenv("TOKEN_SECRET_KEY") )
	return serializer.dumps( email, salt=os.getenv("GENERATE_TOKEN_SALT") )


def confirm_token(token, expiration=3600):
	serializer = URLSafeTimedSerializer( os.getenv("TOKEN_SECRET_KEY") )
	try:
		email = serializer.loads(
			token,
			salt=os.getenv("GENERATE_TOKEN_SALT"),
			max_age=expiration
		)
	except:
		return False
	return email
