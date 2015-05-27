# -*- coding: utf-8 -*-

import random
import uuid

safe_string_letters = 'abcdefghjkmnpqrstuvwxyzABCDEFGHJKMNPQRSTUVWXYZ23456789'

def generate_api_token():
    return uuid.uuid4().hex()


def generate_password(length):
    return generate_random_string(length)

def password_crypt(password):
    pass

def password_compare(hash, password):
    pass

def generate_random_string(length):

    return "".join([
        random.choice(safe_string_letters) for i in xrange(length)
    ])
