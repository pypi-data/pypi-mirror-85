import hashlib
import typing

from multihash import coerce_code

from .identity import IdentityHash

_MH_NAME_TO_ALGO_NAME = {
    'sha1': 'sha1',
    'sha2-256': 'sha256',
    'sha2-512': 'sha512',
    'sha3-224': 'sha3_224',
    'sha3-256': 'sha3_256',
    'sha3-384': 'sha3_384',
    'sha3-512': 'sha3_512',
}

_MH_NAME_TO_ALGO = {
    'id': IdentityHash
}
for mhname, hlname in _MH_NAME_TO_ALGO_NAME.items():
    algo = getattr(hashlib, hlname, None)
    _MH_NAME_TO_ALGO[mhname] = algo

_MH_CODE_TO_ALGO = {
    coerce_code(name): algo for name, algo in _MH_NAME_TO_ALGO.items()
}
_HASH_NAME_TO_CODE = {
    func().name: coerce_code(name) for name, func in _MH_NAME_TO_ALGO.items() if func
}


def get_algorithm_by_code(code: typing.Union[str, int]) -> object:
    """ Get a :pep:`452` compatible hashing object by its `multihash code`_ or name

    :param code: `multihash code`_ or name
    :return: :pep:`452` compatible hashing object
    """
    return _MH_CODE_TO_ALGO[coerce_code(code)]


def get_code_by_hash_obj(hash_obj) -> int:
    """ Get the `multihash code`_ for a :pep:`452` compatible hashing object

    :param hash_obj: :pep:`452` compatible hashing object
    :return: `multihash code`_
    """
    return _HASH_NAME_TO_CODE[hash_obj.name]


#: List of preferred hashing functions, from most to least preferred
PREFERRED_FUNCS = [
    'sha3-512',
    'sha3-384',
    'sha2-512',
    'sha3-256',
    'sha3-224',
    'sha2-256',
    'sha1',
]

SUPPORTED_HASH_FUNCS = [
    coerce_code(name) for name in PREFERRED_FUNCS
    if _MH_NAME_TO_ALGO.get(name) is not None
]

__all__ = ['SUPPORTED_HASH_FUNCS', 'get_algorithm_by_code', 'get_code_by_hash_obj']
