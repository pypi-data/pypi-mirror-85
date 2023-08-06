import hashlib
import hmac
import random

#: Length of the challenge
CHALLENGE_LENGTH = 512
hash_func = hashlib.sha512

#: Valid characters for an API key
API_KEY_CHARSET = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

#: Default length of an API key
API_KEY_LENGTH = 24

#: Valid characters for an API secret
API_SECRET_CHARSET = API_KEY_CHARSET + '!@$^&-_+./?'

#: Default length of an API secret
API_SECRET_LENGTH = 64

#: Valid characters for the salt used
SALT_CHARSET = API_SECRET_CHARSET

#: Length of the salt
SALT_LENGTH = 8


def gen_key(charset: str, length: int) -> str:
    """ Generate a key of `length` using characters in `charset`

    :param charset: Characters to use
    :param length: Length of the string
    :return: the generated key
    """
    return ''.join(random.choice(charset) for _ in range(length))


def gen_api_key() -> str:
    """ Generate a random API key

    :return: the generated key
    """
    return gen_key(API_KEY_CHARSET, API_KEY_LENGTH)


def gen_api_secret() -> str:
    """ Generate a random secret

    :return: the generated secret
    """
    return gen_key(API_SECRET_CHARSET, API_SECRET_LENGTH)


def gen_salt() -> str:
    """ Generate a random salt

    :return: the generated salt
    """
    return gen_key(SALT_CHARSET, SALT_LENGTH)


def gen_challenge() -> bytes:
    """ Generate a random challenge

    :return: the generated challenge
    """
    return bytes(random.randint(0, 255) for _ in range(CHALLENGE_LENGTH))


def constant_time_compare(val1: bytes, val2: bytes):
    """ Returns `True` if the two strings are equal, `False` otherwise.

    The time taken is independent of the number of characters that match.

    (Borrowed from `Django <http://djangoproject.org/>`_)
    """
    if len(val1) != len(val2):
        return False
    result = 0
    for x, y in zip(val1, val2):
        result |= x ^ y
    return result == 0


def calculate_challenge_response(api_key: str, api_secret: str, salt: str, challenge: bytes) -> bytes:
    """ Calculate the response to a challenge request

    :param api_key: The API key
    :param api_secret: The API secret
    :param salt: The salt
    :param challenge: The challenge
    :return: The challenge response
    """
    key = '{}{}{}'.format(api_key, salt, api_secret)

    block_size = hash_func().block_size

    # Pad key with salt until it is block_size long
    while len(key) < block_size:
        key = (key + salt)[:block_size]

    # Calculate the response
    return hmac.new(key.encode('ascii'), challenge, hash_func).digest()
