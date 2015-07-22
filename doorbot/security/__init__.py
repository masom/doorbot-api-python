# -*- coding: utf-8 -*-

import bcrypt
import random
import uuid

safe_string_letters = 'abcdefghjkmnpqrstuvwxyzABCDEFGHJKMNPQRSTUVWXYZ23456789'


def generate_api_token():
    return str(uuid.uuid4())


def generate_password(length):
    return generate_random_string(length)


def password_crypt(password):
    return bcrypt.hashpw(password, bcrypt.gensalt())


def password_compare(hashed, password):
    '''Compare the hashed and raw passwords

    :returns: True or False
    :rtype: boolean
    '''

    if bcrypt.hashpw(password, hashed) == hashed:
        return True
    else:
        return False


def generate_random_string(length):
    '''Generate a random string with the given length

    :returns: A random string
    :rtype: string
    '''

    return "".join([
        random.choice(safe_string_letters) for i in xrange(length)
    ])
