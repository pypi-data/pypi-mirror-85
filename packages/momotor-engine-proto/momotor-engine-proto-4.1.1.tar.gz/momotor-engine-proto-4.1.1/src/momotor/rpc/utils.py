import copy
import re
import typing

if typing.TYPE_CHECKING:
    from google.protobuf.message import Message
    from grpc import Channel, Server

whitespace = re.compile(r"[\r\n\s]+")


def format_msg(msg: "Message", *, suppress=None) -> str:
    """ Format a protobuf Message for use in logs, optionally suppressing one ore more text or binary fields """
    if msg and suppress:
        msg = copy.deepcopy(msg)
        for field in suppress:
            if msg.HasField(field):
                value = getattr(msg, field)
                replacement = f"...<{len(value)} bytes>"
                if isinstance(value, bytes):
                    replacement = replacement.encode('ascii')
                setattr(msg, field, replacement)

    return re.sub(whitespace, " ", str(msg)).replace('{ ', '{').replace(' }', '}').strip()


def setup_h2_logging(channel: typing.Union["Channel", "Server"]):
    from h2.config import DummyLogger
    from logging import getLogger, DEBUG

    class H2Logger(DummyLogger):
        def __init__(self, logger):
            super().__init__()
            self.__logger = logger

        def debug(self, *args, **kwargs):
            self.__logger.debug(*args, **kwargs)

    logger = getLogger('h2')
    if logger.isEnabledFor(DEBUG):
        # noinspection PyProtectedMember,PyUnresolvedReferences
        channel._h2_config.logger = H2Logger(logger)