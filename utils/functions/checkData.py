import jwt
from rest_framework.exceptions import AuthenticationFailed


def is_there_events_file_uploaded(objects):
    for obj in objects:
        if obj.is_event_file:
            return True
    return False


def is_there_devices_file_uploaded(objects):
    for obj in objects:
        if not obj.is_event_file:
            return True
    return False


def check_auth_token(token):
    if not token:
        raise AuthenticationFailed("Unauthenticated")

    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')

    if not payload:
        raise AuthenticationFailed('Unauthenticated!')
