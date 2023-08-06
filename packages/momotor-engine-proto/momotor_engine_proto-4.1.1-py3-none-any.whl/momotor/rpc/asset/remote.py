import asyncio
import logging
import pathlib
import typing
import zipfile

from asyncio_extras import call_in_executor, open_async

from momotor.rpc.asset.exceptions import AssetHashMismatchError, UnexpectedEndOfStream, AssetSizeMismatchError
from momotor.rpc.asset.utils import get_file_multihash, get_file_hash, file_writer, file_reader
from momotor.rpc.const import CHUNK_SIZE
from momotor.rpc.exception import raise_message_exception
from momotor.rpc.hash import decode as decode_hash, is_identity_code
from momotor.rpc.proto.asset_pb2 import AssetData, UploadAssetRequest, DownloadAssetRequest, AssetQuery, \
    Category, ZIP, XML
from momotor.rpc.proto.auth_pb2 import ServerInfoResponse
from momotor.rpc.proto.client_grpc import ClientStub
from momotor.rpc.proto.worker_grpc import WorkerStub
from momotor.shared.doc import annotate_docstring

logger = logging.getLogger(__name__)

# Remote (clients and workers) side of asset up/downloading.
# Counterpart is in server.py

StubType = typing.Union[ClientStub, WorkerStub]


@annotate_docstring(logger=logger)
async def send_asset(stub: StubType, job_id: str, query: AssetQuery, path: typing.Union[str, pathlib.Path],
                     server_info: ServerInfoResponse, *,
                     process_executor=None, timeout=None) -> None:
    """ Function for use by a client or worker to send an asset to the broker server

    Produces log messages on the ``{logger.name}`` logger.

    :param stub: The connected stub to the broker.
    :param job_id: Id of the job
    :param query: Query for the asset
    :param path: Local file path of the file to send
    :param server_info: The server's info response
    :param process_executor: An asyncio executor to execute long running CPU bound tasks
    :param timeout: Timeout
    """

    path = pathlib.Path(path)

    stat, hash_data, is_zip = await asyncio.gather(
        call_in_executor(path.stat),
        call_in_executor(get_file_multihash, path, server_info, executor=process_executor),
        call_in_executor(zipfile.is_zipfile, path)
    )

    size = stat.st_size
    hash_value, identity_hash = hash_data
    data = AssetData(
        query=query,
        format=ZIP if is_zip else XML,
        size=size,
        hash=hash_value,
    )
    cat_name = Category.Name(query.category)

    async with stub.uploadAsset.open() as stream:
        logger.debug(f"sending {cat_name}")

        try:
            await asyncio.wait_for(
                stream.send_message(UploadAssetRequest(jobId=job_id, assetData=data)),
                timeout=timeout
            )

            response = await stream.recv_message()
            raise_message_exception(response)

            if response.assetSelected:
                logger.debug(f"sending {cat_name} accepted, asset known")
            elif identity_hash:
                logger.debug(f"sending {cat_name} accepted, asset unknown, id-encoded")
            else:
                logger.debug(f"sending {cat_name} accepted, asset unknown")

                if server_info:
                    chunk_size = min(server_info.chunkSize, CHUNK_SIZE)
                else:
                    chunk_size = CHUNK_SIZE

                read_queue = asyncio.Queue(1)
                read_task = asyncio.ensure_future(file_reader(path, 'rb', read_queue, chunk_size=chunk_size))
                try:
                    count = 0
                    while True:
                        chunk = await read_queue.get()
                        if not chunk:
                            break

                        count += 1
                        logger.debug(f"sending {cat_name} chunk {count}")
                        await asyncio.wait_for(
                            stream.send_message(UploadAssetRequest(chunk=chunk)),
                            timeout=timeout
                        )
                finally:
                    await read_task

            logger.debug(f"sending {cat_name} done")

        finally:
            try:
                await stream.end()
            except Exception as exc:
                logger.warning(f"unable to end stream: {exc}")


@annotate_docstring(logger=logger)
async def receive_asset(stub: StubType, job_id: str, query: AssetQuery, path: typing.Union[str, pathlib.Path],
                        exists: typing.Callable[[AssetData], typing.Awaitable[bool]] = None,
                        process_executor=None, timeout=None) -> typing.Tuple[AssetData, bool]:
    """ Function for use by a client or worker to request and receive an asset from the broker.

    Produces log messages on the ``{logger.name}`` logger.

    :param stub: The connected stub to the broker.
    :param job_id: Id of the job
    :param query: Query for the asset
    :param path: Local file path where the file is to be stored
    :param exists: A function that checks if the file is already known locally
    :param process_executor: An asyncio executor to execute long running CPU bound tasks
    :param timeout: Timeout
    :return: A tuple with the :py:class:`~momotor.rpc.proto.asset_pb2.AssetData` identifying the asset, and
             a boolean indicating whether the asset already exists locally.
    """

    cat_name = Category.Name(query.category)

    async with stub.downloadAsset.open() as stream:
        logger.debug(f"receiving {cat_name}")

        await asyncio.wait_for(
            stream.send_message(DownloadAssetRequest(jobId=job_id, query=query)),
            timeout=timeout
        )

        response = await stream.recv_message()
        raise_message_exception(response)

        data = response.data

        hash_digest, hash_code = decode_hash(data.hash)
        is_identity_hash = is_identity_code(hash_code)

        existing = not is_identity_hash and (await exists(data) if callable(exists) else False)
        await asyncio.wait_for(
            stream.send_message(DownloadAssetRequest(accepted=is_identity_hash or not existing), end=True),
            timeout=timeout
        )

        if existing:
            logger.debug(f"receiving {cat_name} accepted, asset known")
        elif data.size == 0:
            logger.debug(f"receiving {cat_name} accepted, asset empty")
        elif is_identity_hash:
            logger.debug(f"receiving {cat_name} accepted, asset received as identity-hash")

            if data.size != len(hash_digest):
                raise AssetHashMismatchError("Hash size mismatch")

            async with open_async(path, 'wb') as f:
                await f.write(hash_digest)

        else:
            logger.debug(f"receiving {cat_name} accepted, asset unknown")

            count, remaining = 0, data.size

            write_queue = asyncio.Queue(1)
            write_task = asyncio.ensure_future(file_writer(path, 'wb', write_queue))
            try:
                while remaining > 0:
                    chunk = response.chunk
                    if len(chunk) > remaining:
                        raise AssetSizeMismatchError

                    if chunk:
                        await write_queue.put(chunk)
                        remaining -= len(chunk)

                    if remaining > 0:
                        count += 1
                        logger.debug(f"receiving {cat_name} chunk {count}")

                        try:
                            response = await asyncio.wait_for(stream.recv_message(), timeout=timeout)
                        except Exception as exc:
                            if 'Incomplete data' in str(exc):
                                raise UnexpectedEndOfStream(str(exc))

                            raise

                        if not response:
                            raise UnexpectedEndOfStream("No response")

                        raise_message_exception(response)

            finally:
                await write_queue.put(None)
                await write_task

            file_hash = await call_in_executor(get_file_hash, hash_code, path, executor=process_executor)
            if hash_digest != file_hash:
                logger.error(f"receiving {cat_name} failed: hash mismatch")
                raise AssetHashMismatchError("Hash value mismatch")

            logger.debug(f"receiving {cat_name} done")

        return data, existing
