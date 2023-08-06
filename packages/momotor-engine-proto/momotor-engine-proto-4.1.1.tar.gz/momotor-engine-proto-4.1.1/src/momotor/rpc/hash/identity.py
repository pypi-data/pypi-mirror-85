""" A :pep:`452` compatible implementation of an identity hashing object.

The identity hash stores the literal content as a hash:

>>> IdentityHash(b'any random data').digest() == b'any random data'
True

"""
import typing


class IdentityHash(object):
    #: identifier for the hashing function
    name = 'identity'

    def __init__(self, data: typing.Union[bytes, memoryview] = None):
        self._digest = b'' if data is None else bytes(data)

    def update(self, data: bytes):
        """ Extend the hash with `data`

        :param data: data to concatenate to the existing data
        """
        self._digest += data

    def digest(self) -> bytes:
        """ Get the current data

        :return: the current data
        """
        return self._digest

    def hexdigest(self) -> bytes:
        """ Get the current data as hex-encoded digest

        :return: the hex-encoded current data
        """
        import binascii
        return binascii.b2a_hex(self._digest)

    def copy(self) -> "IdentityHash":
        """ Create a copy of this hash object

        :return: Copy of the object
        """
        return IdentityHash(self._digest)

    @property
    def digest_size(self):
        return len(self._digest)

    @property
    def block_size(self):
        return NotImplemented


def new(data: typing.Union[bytes, memoryview] = None) -> IdentityHash:
    """ Create a identity hash object

    :param data: initial data for the hash
    :return: the identity hash object
    """
    return IdentityHash(data)


#: Digest size is variable
digest_size = None
