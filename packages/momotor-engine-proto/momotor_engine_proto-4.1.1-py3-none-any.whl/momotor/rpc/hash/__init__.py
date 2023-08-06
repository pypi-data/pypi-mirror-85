import typing

import base58
from multihash import coerce_code, encode as multihash_encode, Multihash, decode as multihash_decode

from momotor.rpc.exception import AssetException

from .const import MAX_HASH_LEN, MAX_IDENTITY_LENGTH
from .funcs import get_algorithm_by_code, get_code_by_hash_obj, SUPPORTED_HASH_FUNCS
from .identity import IdentityHash

__all__ = ['new', 'encode', 'encode_content', 'decode', 'is_identity_code', 'is_identity']

ID_HASH_CODE = coerce_code('id')  # deprecated, use is_identity_code()


def new(content: typing.Union[bytes, memoryview] = None,
        *, supported_funcs: typing.Iterable[int] = None, func_code: typing.Union[int, str] = SUPPORTED_HASH_FUNCS[0]):
    """ Construct a new hash object for best matching algorithm, like hashlib.new()

    :param content: Initial content to add to hash
    :param supported_funcs: List of multihash function codes to select the best hash from
    :param func_code: Multihash function code to use, only used if `supported_funcs` is not provided.
    Defaults to SUPPORTED_HASH_FUNCS[0]
    :return: the selected hash function
    :raises: ValueError if none of the codes in `supported_funcs` is supported locally
    """
    supported_funcs = set(supported_funcs or [])
    if supported_funcs:
        for func_code in SUPPORTED_HASH_FUNCS:
            if func_code in supported_funcs:
                break
        else:
            raise ValueError("No matching hash functions")
    else:
        func_code = coerce_code(func_code)

    fn = get_algorithm_by_code(func_code)()
    if content is not None:
        fn.update(content)

    return fn


def encode(hash_func) -> bytes:
    """ Multihash encoding of hash_func

    :param hash_func: hashing function
    :return: base58 encoded multihash value for digest of hash_func
    """
    encoded = base58.b58encode(
        multihash_encode(hash_func.digest(), get_code_by_hash_obj(hash_func))
    )

    if len(encoded) > MAX_HASH_LEN:
        raise ValueError("Hash value too long")

    return encoded


def encode_content(content: typing.Union[bytes, memoryview], *, use_identity=None) -> bytes:
    """ Return encoded multihash of content with the preferred algorithm in the required encoding

    :param content: content to be encoded
    :param use_identity: True to force use of identity encoding, False to force use of hashing. None (default) to
    use identity encoding automatically if content length fits
    :return: base58 encoded multihash value for content
    """
    if use_identity and len(content) > MAX_IDENTITY_LENGTH:
        raise ValueError("Content value too long for identity encoding")
    elif use_identity is None:
        use_identity = len(content) <= MAX_IDENTITY_LENGTH

    if use_identity:
        return encode(IdentityHash(content))
    else:
        return encode(new(content))


def _decode_hash(hash_value: typing.Union[bytes, memoryview]) -> Multihash:
    try:
        b = base58.b58decode(bytes(hash_value))
    except ValueError:
        raise ValueError("illegal hash value")

    return multihash_decode(b)


def decode(hash_value: typing.Union[bytes, memoryview]) -> typing.Tuple[bytes, int]:
    """ Decode multihash value in required encoding and return the digest or content, and the hash function code

    :param hash_value: base58 encoded multihash value
    :return: tuple containing decoded hash digest and multihash function code
    :raises: AssetException if the hash is not a valid encoded multihash or uses an unsupported hashing function
    """
    try:
        mh = _decode_hash(hash_value)
    except ValueError as e:
        raise AssetException(str(e))
    else:
        if not is_identity_code(mh.code) and mh.code not in SUPPORTED_HASH_FUNCS:
            from multihash.constants import CODE_HASHES
            raise AssetException(f"Unsupported hash code {mh.code} ({CODE_HASHES.get(mh.code, '?')})")

        return mh.digest, mh.code


_ID_HASH_CODE = coerce_code('id')


def is_identity_code(hash_code: int):
    return hash_code == _ID_HASH_CODE


def is_identity(hash_value: typing.Union[bytes, memoryview]) -> bool:
    """ Return True if hash_value encodes identity encoded content

    :param hash_value: base58 encoded multihash value
    :return: True if hash_value contains identity encoded content
    """
    try:
        return is_identity_code(_decode_hash(hash_value).code)
    except ValueError:
        return False
