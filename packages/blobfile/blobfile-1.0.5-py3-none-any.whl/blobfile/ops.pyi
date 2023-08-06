# This file was generated automatically by filter-stubs.py

import io
import threading
import multiprocessing as mp
import urllib3
from typing import Any
from typing import BinaryIO
from typing import Callable
from typing import Dict
from typing import Iterator
from typing import List
from typing import Literal
from typing import Mapping
from typing import NamedTuple
from typing import Optional
from typing import Sequence
from typing import TYPE_CHECKING
from typing import TextIO
from typing import Tuple
from typing import Union
from typing import overload
from blobfile.common import Request
class Stat(NamedTuple):
    size: int
    mtime: float
    ctime: float
    md5: Optional[str]
    version: Optional[str]
    ...

class DirEntry(NamedTuple):
    path: str
    name: str
    is_dir: bool
    is_file: bool
    stat: Optional[Stat]
    ...

@overload
def BlobFile(path: str, mode: Literal['rb', 'wb', 'ab'], streaming: Optional[bool]=..., buffer_size: int=..., cache_dir: Optional[str]=...) -> BinaryIO:
  ...
@overload
def BlobFile(path: str, mode: Literal['r', 'w', 'a']=..., streaming: Optional[bool]=..., buffer_size: int=..., cache_dir: Optional[str]=...) -> TextIO:
  ...
def BlobFile(path: str, mode: Literal['r', 'rb', 'w', 'wb', 'a', 'ab']=..., streaming: Optional[bool]=..., buffer_size: int=..., cache_dir: Optional[str]=...):
  ...
def basename(path: str) -> str:
  ...
def configure(log_callback: Callable[[str], None]=..., connection_pool_max_size: int=..., max_connection_pool_count: int=..., azure_write_chunk_size: int=..., google_write_chunk_size: int=..., retry_log_threshold: int=..., retry_limit: Optional[int]=...) -> None:
  ...
def copy(src: str, dst: str, overwrite: bool=..., parallel: bool=..., parallel_executor: Optional[concurrent.futures.Executor]=..., return_md5: bool=...) -> Optional[str]:
  ...
def dirname(path: str) -> str:
  ...
def exists(path: str) -> bool:
  ...
def get_url(path: str) -> Tuple[str, Optional[float]]:
  ...
def glob(pattern: str, parallel: bool=...) -> Iterator[str]:
  ...
def isdir(path: str) -> bool:
  ...
def join(a: str) -> str:
  ...
def listdir(path: str, shard_prefix_length: int=...) -> Iterator[str]:
  ...
def makedirs(path: str) -> None:
  ...
def md5(path: str) -> str:
  ...
def remove(path: str) -> None:
  ...
def rmdir(path: str) -> None:
  ...
def rmtree(path: str) -> None:
  ...
def scandir(path: str, shard_prefix_length: int=...) -> Iterator[DirEntry]:
  ...
def scanglob(pattern: str, parallel: bool=...) -> Iterator[DirEntry]:
  ...
def set_mtime(path: str, mtime: float, version: Optional[str]=...) -> bool:
  ...
def stat(path: str) -> Stat:
  ...
def walk(top: str, topdown: bool=..., onerror: Optional[Callable]=...) -> Iterator[Tuple[str, Sequence[str], Sequence[str]]]:
  ...
