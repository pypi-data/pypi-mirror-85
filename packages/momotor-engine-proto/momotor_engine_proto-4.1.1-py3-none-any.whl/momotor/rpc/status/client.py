import asyncio
import typing

from google.protobuf.empty_pb2 import Empty

from momotor.rpc.exception import raise_message_exception
from momotor.rpc.proto.client_grpc import ClientStub
from momotor.rpc.proto.job_pb2 import JobStatusStream


async def multi_job_status_stream(stub: ClientStub, *, connect_timeout: float = None, status_timeout: float = None) \
        -> typing.AsyncIterable[JobStatusStream]:
    """ Async generator that connects to the :py:func:`~momotor.rpc.proto.client_grpc.ClientBase.multiJobStatusStream`
    client endpoint and yields the :py:class:`~momotor.rpc.proto.job_pb2.JobStatusStream` status messages

    :param stub: The connected client stub
    :param connect_timeout: Connection timeout
    :param status_timeout: Status message timeout
    """

    async with stub.multiJobStatusStream.open(timeout=connect_timeout) as stream:
        await asyncio.wait_for(stream.send_message(Empty(), end=True), timeout=connect_timeout)

        while True:
            message = await asyncio.wait_for(stream.recv_message(), timeout=status_timeout)
            raise_message_exception(message)
            yield message
