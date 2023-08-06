import logging
import typing

from google.protobuf.message import Message

# noinspection PyUnresolvedReferences
# keep for backwards compatibility. These used to be exported in __all__
from grpclib.exceptions import StreamTerminatedError, GRPCError, ProtocolError

from momotor.rpc.asset.exceptions import UnexpectedEndOfStream
from momotor.rpc.proto.exception_pb2 import Exception as ExceptionMessage, INVALID_EXCEPTION, FORMAT, AUTH, JOB, \
    ASSET, ASSET_NOT_FOUND
from momotor.shared.doc import annotate_docstring

logger = logging.getLogger(__name__)

__all__ = [
    'RPCException',
    'FormatException',
    'AuthException',
    'JobException',
    'AssetException',
    'AssetNotFoundException',
    'raise_message_exception',
]


class RPCException(Exception):
    """ Base class for all protocol exceptions.

    When a subclass of RPCException is raised by an RPC method, the exception is caught and converted into
    a :py:class:`~google.protobuf.message.Message` containing the exception's `type_code` and `text`

    Should not be raised directly, but use one of the subclasses.

    :param text: textual explanation of the exception
    :param wire_message: the :py:class:`~momotor.rpc.proto.exception_pb2.Exception` message
                         to include in the RPC response
    """
    type_code = INVALID_EXCEPTION
    type_name = 'rpc'

    def __init__(self, text, wire_message=None):
        self.text = text
        self._wire_message = wire_message

    @property
    def wire_message(self):
        return self._wire_message or ExceptionMessage(type=self.type_code, text=self.text)

    def __str__(self):
        return 'RPC Exception ({0.type_name}) {0.text}'.format(self)


class FormatException(RPCException):
    """ Indicates an invalid (combination of) arguments
    """
    type_code = FORMAT
    type_name = 'format'


class AuthException(RPCException):
    """ Indicates an authentication error
    """
    type_code = AUTH
    type_name = 'auth'


class JobException(RPCException):
    """ Indicates an error with the job
    """
    type_code = JOB
    type_name = 'job'


class AssetException(RPCException):
    """ Indicates an error with an asset
    """
    type_code = ASSET
    type_name = 'asset'


class AssetNotFoundException(RPCException):
    """ Indicates the asset does not exist
    """
    type_code = ASSET_NOT_FOUND
    type_name = 'asset_not_found'


#: Mapping from exception codes as returned by the API to the exception classes
EXCEPTION_MAP = {
    cls.type_code: cls
    for cls in (
        FormatException,
        AuthException,
        JobException,
        AssetException,
        AssetNotFoundException,
    )
}


@annotate_docstring(logger=logger)
def raise_message_exception(message: typing.Optional[Message], *, log_level=logging.DEBUG):
    """ If the `message` has an exception field, convert it into an RPCException and raise it

    If `message` is `None`, raises :py:exc:`~momotor.rpc.asset.exceptions.UnexpectedEndOfStream`.

    If `message` has an `exception` field set, raises a subclass of :py:exc:`RPCException`

    Produces logging information on the ``{logger.name}`` logger

    :param message: The message to processes
    :param log_level: level to log the exception message on
    """
    if message is None:
        logger.log(log_level, "unexpected end of stream")
        raise UnexpectedEndOfStream

    try:
        has_exception = message.HasField('exception')
    except ValueError:
        has_exception = False

    if has_exception:
        # noinspection PyUnresolvedReferences
        exc_message: ExceptionMessage = message.exception
        exc_type = EXCEPTION_MAP.get(exc_message.type, RPCException)
        exc = exc_type(exc_message.text, exc_message)
        logger.log(log_level, f"received {exc}")
        raise exc
