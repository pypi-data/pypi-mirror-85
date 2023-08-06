import asyncio
# import logging
import typing

from grpclib.server import Stream

from momotor.rpc.asset.exceptions import UnexpectedEndOfStream
from momotor.rpc.proto.asset_pb2 import AssetData, DownloadAssetResponse, UploadAssetResponse
# from momotor.rpc.utils import format_msg
from momotor.rpc.validate.request import validate_upload_asset_request, validate_download_asset_request

# logger = logging.getLogger(__name__)


# Server's side of asset up/downloading.
# Counterpart is in remote.py

async def download_asset_stream(data: AssetData, chunks: typing.Optional[typing.AsyncGenerator[bytes, None]],
                                stream: Stream, *, timeout=None):
    """ Function for use by the broker to handle an asset download stream from a client or worker.

    This communicates with a remote's :py:func:`momotor.rpc.asset.remote.receive_asset`

    :param data: An :py:class:`momotor.rpc.proto.asset_pb2.AssetData` object identifying the requested asset
    :param chunks: A generator producing chunks of the requested asset
    :param stream: The gPRC stream to the client or worker
    :param timeout: Timeout
    """
    await asyncio.wait_for(stream.send_message(DownloadAssetResponse(data=data)), timeout=timeout)

    accepted_request = await asyncio.wait_for(stream.recv_message(), timeout=timeout)
    if accepted_request:
        # logger.debug(f"download asset stream accept message {format_msg(accepted_request)}")
        validate_download_asset_request(accepted_request, expect_oneof='accepted')
    else:
        raise UnexpectedEndOfStream("Empty response")

    if accepted_request.accepted and chunks is not None:
        async for chunk in chunks:
            await asyncio.wait_for(
                stream.send_message(DownloadAssetResponse(chunk=chunk)),
                timeout=timeout
            )


async def upload_asset_stream(creator: typing.AsyncGenerator[int, typing.Optional[bytes]], stream: Stream, *,
                              timeout=None):
    """ Function for use by the broker to handle an asset upload stream to a client or worker.

    This communicates with a remote's :py:func:`momotor.rpc.asset.remote.send_asset`

    :param creator: A generator that processes the chunks and writes them to a file or other storage,
                    and yields the number of bytes remaining.
    :param stream: The gPRC stream to the client or worker
    :param timeout: Timeout
    """
    try:
        remaining = await creator.asend(None)
        done = remaining == 0
        response = UploadAssetResponse(assetSelected=done)
        await asyncio.wait_for(stream.send_message(response), timeout=timeout)

        while not done:
            try:
                chunk_request = await asyncio.wait_for(
                    stream.recv_message(),
                    timeout=timeout
                )
            except Exception as exc:
                if 'Incomplete data' in str(exc):
                    raise UnexpectedEndOfStream(str(exc))

                raise

            # logger.debug(f"upload asset stream chunk message {format_msg(chunk_request, suppress=['chunk'])}")
            if chunk_request:
                validate_upload_asset_request(chunk_request, expect_oneof='chunk')
                await creator.asend(chunk_request.chunk)
                remaining -= len(chunk_request.chunk)

            elif remaining > 0:
                raise UnexpectedEndOfStream(f"{remaining} bytes remaining")

            else:
                done = True

    finally:
        await creator.aclose()
