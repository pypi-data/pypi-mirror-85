from contextlib import asynccontextmanager
import logging
import typing

from momotor.rpc.exception import raise_message_exception
from momotor.rpc.proto.shared_pb2 import SharedLockRequest
from momotor.rpc.proto.worker_grpc import WorkerStub
from momotor.shared.doc import annotate_docstring
from momotor.shared.state import StateABC, LockFailed

logger = logging.getLogger(__name__)


@annotate_docstring(logger=logger)
class SharedState(StateABC):
    """ An implementation of :py:class:`momotor.shared.state.StateABC` for use by workers.

    Produces log messages on the ``{logger.name}`` logger.

    :param stub: The connected worker stub
    """
    def __init__(self, stub: WorkerStub):
        self.stub = stub

    @asynccontextmanager
    async def get_lock(self, key: str, *, exclusive: bool = True) -> typing.AsyncContextManager[None]:
        async with self.stub.sharedLock.open() as stream:
            # logger.debug(f'state lock {key} acquiring')

            await stream.send_message(SharedLockRequest(lock=True, key=key, exclusive=exclusive))
            response = await stream.recv_message()
            raise_message_exception(response)

            if not response.locked:
                logger.error(f'state lock {key} failed to acquire')
                raise LockFailed

            # logger.debug(f'state lock {key} acquired')
            try:
                yield
            finally:
                await stream.send_message(SharedLockRequest(lock=False), end=True)
                response = await stream.recv_message()
                raise_message_exception(response)
                # logger.debug(f'state lock {key} released')

    async def test_lock(self, key: str, *, exclusive: bool = True) -> bool:
        responses = list(await self.stub.sharedLock([SharedLockRequest(lock=False, key=key, exclusive=exclusive)]))
        response = responses[0]
        raise_message_exception(response)
        return response.locked
