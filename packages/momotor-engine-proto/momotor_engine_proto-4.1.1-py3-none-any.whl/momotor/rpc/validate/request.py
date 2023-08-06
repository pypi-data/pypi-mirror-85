from momotor.rpc.exception import FormatException
from momotor.rpc.proto.asset_pb2 import UploadAssetRequest, DownloadAssetRequest
from momotor.rpc.proto.auth_pb2 import AuthenticateRequest
from momotor.rpc.proto.job_pb2 import CreateJobRequest, StartJobRequest, GetJobRequest, JobStatusRequest, \
    EndJobRequest, TEST_RECIPE, VERIFY_PRODUCT
from momotor.rpc.proto.shared_pb2 import SharedLockRequest
from momotor.rpc.proto.worker_pb2 import UpdateTaskStatusRequest
from momotor.rpc.validate.base import validate_oneof, validate_required
from momotor.rpc.validate.query import validate_query_field

__all__ = [
    'validate_authenticate_request',
    'validate_create_job_request',
    'validate_download_asset_request',
    'validate_end_job_request',
    'validate_job_status_request',
    'validate_start_job_request',
    'validate_upload_asset_request',
    'validate_get_job_request',
    'validate_update_status_request',
    # 'validate_shared_value_request',
    'validate_shared_lock_request',
]


def validate_authenticate_request(message: AuthenticateRequest, *, expect_oneof: str):
    """ Validate :py:class:`~momotor.rpc.proto.auth_pb2.AuthenticateRequest` message

    :param message: The message to validate
    :param expect_oneof: Expected `request` field (``apiKey`` or ``challengeResponse``)
    :raises FormatException: When the message is invalid
    """
    validate_oneof(message, 'request', expect_oneof)


def validate_create_job_request(message: CreateJobRequest):
    """ Validate :py:class:`~momotor.rpc.proto.job_pb2.CreateJobRequest` message

    :param message: The message to validate
    :raises FormatException: When the message is invalid
    """
    validate_required(message, ['type'])

    if message.type not in {TEST_RECIPE, VERIFY_PRODUCT}:
        raise FormatException("ConnectRequest: type invalid")


def validate_upload_asset_request(message: UploadAssetRequest, *, expect_oneof: str):
    """ Validate :py:class:`~momotor.rpc.proto.asset_pb2.UploadAssetRequest` message

    :param message: The message to validate
    :param expect_oneof: Expected `request` field (``assetData`` or ``chunk``)
    :raises FormatException: When the message is invalid
    :raises AssetException: When the query is invalid
    """
    validate_oneof(message, 'request', expect_oneof)
    if expect_oneof == 'assetData':
        validate_query_field(message.assetData)


def validate_start_job_request(message: StartJobRequest):
    """ Validate :py:class:`~momotor.rpc.proto.job_pb2.StartJobRequest` message

    :param message: The message to validate
    :raises FormatException: When the message is invalid
    """
    pass


def validate_job_status_request(message: JobStatusRequest):
    """ Validate :py:class:`~momotor.rpc.proto.job_pb2.JobStatusRequest` message

    :param message: The message to validate
    :raises FormatException: When the message is invalid
    """
    pass


def validate_download_asset_request(message: DownloadAssetRequest, *, expect_oneof: str):
    """ Validate :py:class:`~momotor.rpc.proto.asset_pb2.DownloadAssetRequest` message

    :param message: The message to validate
    :param expect_oneof: Expected `request` field (``query`` or ``accepted``)
    :raises FormatException: When the message is invalid
    :raises AssetException: When the query is invalid
    """
    validate_oneof(message, 'request', expect_oneof)
    if expect_oneof == 'query':
        validate_query_field(message)


def validate_end_job_request(message: EndJobRequest):
    """ Validate :py:class:`~momotor.rpc.proto.job_pb2.EndJobRequest` message

    :param message: The message to validate
    :raises FormatException: When the message is invalid
    """
    pass


def validate_get_job_request(message: GetJobRequest):
    """ Validate :py:class:`~momotor.rpc.proto.job_pb2.GetJobRequest` message

    :param message: The message to validate
    :raises FormatException: When the message is invalid
    """
    validate_required(message, ['version'])


def validate_update_status_request(message: UpdateTaskStatusRequest):
    """ Validate :py:class:`~momotor.rpc.proto.worker_pb2.UpdateTaskStatusRequest` message

    :param message: The message to validate
    :raises FormatException: When the message is invalid
    """
    pass


# def validate_shared_value_request(message: SharedValueRequest):
#     validate_required(message, ['action', 'key'])
#
#     if message.action not in {SET_VALUE_ACTION, GET_VALUE_ACTION, DELETE_VALUE_ACTION}:
#         raise FormatException("SharedValueRequest: action invalid")
#
#     if message.action != SET_VALUE_ACTION:
#         validate_not_allowed(message, ['value'])


def validate_shared_lock_request(message: SharedLockRequest):
    """ Validate :py:class:`~momotor.rpc.proto.shared_pb2.SharedLockRequest` message

    :param message: The message to validate
    :raises FormatException: When the message is invalid
    """
    validate_required(message, ['key'])
