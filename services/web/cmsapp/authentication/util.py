# -*- encoding: utf-8 -*-

import os
import hashlib
import binascii
from zxcvbn import zxcvbn



def hash_pass(password):
    """Hash a password for storing."""

    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                  salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash)  # return bytes


def verify_pass(provided_password, stored_password):
    """Verify a stored password against one provided by user"""

    stored_password = stored_password.decode('ascii')
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

def password_complexity_checker(password):
    """check complexity of password using zxcvbn"""


    complexity = zxcvbn(password)
    if complexity["score"] < 3:
            msg = ','.join(complexity["feedback"]["suggestions"])
            msg = "Password is not complex enough: " + msg
            return False,msg
    else:
        return True, "Password OK"