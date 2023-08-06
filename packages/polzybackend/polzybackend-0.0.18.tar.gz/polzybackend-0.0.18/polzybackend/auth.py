from random import choice
import uuid
import string

ACCESS_KEY_LENGTH = 64
EXPIRED_HOURS = 24

def get_uuid():
    return uuid.uuid4().bytes

def generate_token(length=ACCESS_KEY_LENGTH):
    simbols = string.ascii_letters + string.digits + '!#$%&*+-<=>?@'
    return ''.join(choice(simbols) for i in range(length))

def get_expired(hours=EXPIRED_HOURS, days=0):
    return datetime.utcnow() + timedelta(hours=hours, days=days)