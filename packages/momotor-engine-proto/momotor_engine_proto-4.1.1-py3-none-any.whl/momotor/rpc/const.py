from .auth.client import DEFAULT_PORT, DEFAULT_SSL_PORT
from .hash.const import MAX_HASH_LEN, MAX_IDENTITY_LENGTH
from .hash.funcs import SUPPORTED_HASH_FUNCS

#: Maximum supported chunk size for asset file transfers
CHUNK_SIZE = 8*1024*1024

#: Maximum length of a base58_ encoded hash supported by this version of the library
MAX_HASH_LEN = MAX_HASH_LEN

#: Maximum length of data that can be encoded in a hash of :py:data:`MAX_HASH_LEN` using identity encoding.
#: base58_'s efficiency is 0.732, the overhead is the size of the varint encoded length + 1 for the code byte
MAX_IDENTITY_LENGTH = MAX_IDENTITY_LENGTH

#: List of supported hashing functions, ordered from most to least preferred
SUPPORTED_HASH_FUNCS = SUPPORTED_HASH_FUNCS

#: The default port for non-SSL connections
DEFAULT_PORT = DEFAULT_PORT

#: The default port for SSL connections
DEFAULT_SSL_PORT = DEFAULT_SSL_PORT

__all__ = [
    'MAX_HASH_LEN', 'MAX_IDENTITY_LENGTH', 'SUPPORTED_HASH_FUNCS', 'CHUNK_SIZE',
    'DEFAULT_PORT', 'DEFAULT_SSL_PORT'
]
