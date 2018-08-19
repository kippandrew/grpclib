from .metadata import Deadline, encode_metadata, Request, USER_AGENT
from .encoding.base import GRPC_CONTENT_TYPE
from .encoding.proto import ProtoCodec


class TestStream:

    def __init__(self, channel, request, codec, send_type, recv_type):
        pass


class TestChannel:

    def __init__(self, services, *, codec=None):
        self._services = services
        self._codec = codec or ProtoCodec()
        self._authority = 'test:50051'

    @property
    def _content_type(self):
        return GRPC_CONTENT_TYPE + '+' + self._codec.__content_subtype__

    def request(self, name, request_type, reply_type, *, timeout=None,
                deadline=None, metadata=None):
        if timeout is not None and deadline is None:
            deadline = Deadline.from_timeout(timeout)
        elif timeout is not None and deadline is not None:
            deadline = min(Deadline.from_timeout(timeout), deadline)
        else:
            deadline = None

        if metadata is not None:
            metadata = encode_metadata(metadata)

        request = Request(
            method='POST',
            scheme='http',
            path=name,
            authority=self._authority,
            content_type=self._content_type,
            user_agent=USER_AGENT,
            metadata=metadata,
            deadline=deadline,
        )

        return TestStream(self, request, self._codec, request_type, reply_type)
