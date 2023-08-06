from typing import List

from google.protobuf.message import Message

from momotor.rpc.exception import FormatException


def validate_oneof(message: Message, oneof_group: str, expect_oneof: str):
    """ Generic validator used by the specific validators to check the expected oneOf group field

    :param message: Message to validate
    :param oneof_group: oneOf group to validate
    :param expect_oneof: expected field in the `oneof_group`
    :raises FormatException: When the oneof group has the wrong field
    """
    which_oneof = message.WhichOneof(oneof_group)

    if which_oneof != expect_oneof:
        raise FormatException(f'Unexpected oneof group {oneof_group} field {which_oneof}, expected {expect_oneof}')


def validate_required(message: Message, fields: List[str]):
    """ Generic validator used by the specific validators to check that one or more required fields are included

    :param message: Message to validate
    :param fields: List of field required field names
    :raises FormatException: When one of the fields is missing
    """
    for field in fields:
        try:
            # Check for oneOf and message type fields
            message.HasField(field)
        except ValueError as exc:
            # Check for normal fields
            if not getattr(message, field):
                raise FormatException(str(exc))


# def validate_not_allowed(message: Message, fields: List[str]):
#     for field in fields:
#         try:
#             # Check for oneOf and message type fields
#             if message.HasField(field):
#                 raise FormatException(f'Unexpected field {field}')
#         except ValueError:
#             # Check for normal fields
#             if getattr(message, field):
#                 raise FormatException(f'Unexpected field {field}')


