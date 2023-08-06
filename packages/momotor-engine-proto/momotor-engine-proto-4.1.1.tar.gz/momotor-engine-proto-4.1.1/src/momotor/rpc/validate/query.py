from typing import Union

from momotor.rpc.exception import AssetException
from momotor.rpc.proto.asset_pb2 import RESULT, AssetQuery, Category, NO_CATEGORY, AssetData, DownloadAssetRequest
from momotor.rpc.validate.base import validate_required


def validate_query(query: AssetQuery):
    """ Validate an :py:class:`~momotor.rpc.proto.asset_pb2.AssetQuery`

    :param query: The query to validate
    :raises AssetException: When the query is invalid
    """
    category = query.category
    test_id = query.testId
    step_id = query.stepId

    if category not in Category.values() or category == NO_CATEGORY:
        raise AssetException("Invalid query category")

    elif category != RESULT and (step_id or test_id):
        raise AssetException("{} queries do not allow step/test ids".format(Category.Name(category)))


def validate_query_field(message: Union[AssetData, DownloadAssetRequest]):
    """ Validate the `query` field

    :param message: A message with a `query` field
    :raises FormatException: When the query field is missing
    :raises AssetException: When the query is invalid
    """
    validate_required(message, ['query'])
    validate_query(message.query)
