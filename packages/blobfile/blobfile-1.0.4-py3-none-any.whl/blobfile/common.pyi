# This file was generated automatically by filter-stubs.py

import urllib3
from typing import Any
from typing import Mapping
from typing import Optional
from typing import Sequence
from typing import Tuple
class ConcurrentWriteFailure(RequestFailure):
    """
    A write failed due to another concurrent writer
    """
    ...

class Error(Exception):
    """Base class for blobfile exceptions."""

    def __init__(self, message: str, *args: Any):
        self.message = ...

class Request:

    def __init__(self, method: str, url: str, params: Optional[Mapping[str,
        str]]=..., headers: Optional[Mapping[str, str]]=..., data: Any=...,
        preload_content: bool=..., success_codes: Sequence[int]=...,
        retry_codes: Sequence[int]=...) ->None:
        self.url = ...
        self.method = ...
        self.params = ...
        self.headers = ...
        self.data = ...
        self.preload_content = ...
        self.success_codes = ...
        self.retry_codes = ...

    def __repr__(self):
        ...

class RequestFailure(Error):
    """
    A request failed, possibly after some number of retries
    """

    def __init__(self, message: str, request_string: str, response_status:
        int, error: Optional[str], error_description: Optional[str]):
        self.request_string = ...
        self.response_status = ...
        self.error = ...
        self.error_description = ...

    def __str__(self):
        ...

    @classmethod
    def create_from_request_response(cls, message: str, request: Request,
        response: urllib3.HTTPResponse) ->Any:
        ...

class RestartableStreamingWriteFailure(RequestFailure):
    """
    A streaming write failed in a permanent way that requires restarting from the beginning of the stream
    """
    ...

