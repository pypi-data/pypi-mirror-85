from momotor.rpc.proto.auth_pb2 import AuthenticateResponse
from momotor.rpc.validate.base import validate_oneof, validate_required


def validate_authenticate_response(message: AuthenticateResponse, *, expect_oneof: str):
    """ Validate :py:class:`~momotor.rpc.proto.auth_pb2.AuthenticateResponse` message

    :param message: The message to validate
    :param expect_oneof: Expected `request` field (``challenge`` or ``authToken``)
    :raises FormatException: When the message is invalid
    """
    validate_oneof(message, 'response', expect_oneof)
    if expect_oneof == 'challenge':
        validate_required(message.challenge, ['value', 'salt'])
