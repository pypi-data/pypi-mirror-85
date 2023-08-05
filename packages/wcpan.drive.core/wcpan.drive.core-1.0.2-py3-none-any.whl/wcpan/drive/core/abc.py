from __future__ import annotations


__all__ = ('ReadableFile', 'Hasher', 'WritableFile', 'Middleware')


from abc import ABCMeta, abstractmethod
from typing import (
    AsyncGenerator,
    AsyncIterator,
    List,
    Optional,
    Tuple,
    Type,
)
from types import TracebackType

from .types import (
    ChangeDict,
    MediaInfo,
    Node,
    PrivateDict,
)


class ReadableFile(metaclass=ABCMeta):

    @abstractmethod
    def __aiter__(self) -> AsyncIterator[bytes]:
        pass

    @abstractmethod
    async def __aenter__(self) -> ReadableFile:
        pass

    @abstractmethod
    async def __aexit__(self,
        et: Optional[Type[BaseException]],
        ev: Optional[BaseException],
        tb: Optional[TracebackType],
    ) -> bool:
        pass

    @abstractmethod
    async def read(self, length: int) -> bytes:
        pass

    @abstractmethod
    async def seek(self, offset: int) -> None:
        pass

    @abstractmethod
    async def node(self) -> Node:
        pass


class Hasher(metaclass=ABCMeta):

    @abstractmethod
    def update(self, data: bytes) -> None:
        pass

    @abstractmethod
    def digest(self) -> bytes:
        pass

    @abstractmethod
    def hexdigest(self) -> str:
        pass

    @abstractmethod
    def copy(self) -> 'Hasher':
        pass


class WritableFile(metaclass=ABCMeta):

    @abstractmethod
    async def __aenter__(self) -> WritableFile:
        pass

    @abstractmethod
    async def __aexit__(self,
        et: Optional[Type[BaseException]],
        ev: Optional[BaseException],
        tb: Optional[TracebackType],
    ) -> bool:
        pass

    @abstractmethod
    async def tell(self) -> int:
        pass

    @abstractmethod
    async def seek(self, offset: int) -> None:
        pass

    @abstractmethod
    async def write(self, chunk: bytes) -> int:
        pass

    @abstractmethod
    async def node(self) -> Optional[Node]:
        pass


class RemoteDriver(metaclass=ABCMeta):

    @classmethod
    @abstractmethod
    def get_version_range(cls) -> Tuple[int, int]:
        pass

    @abstractmethod
    async def __aenter__(self) -> RemoteDriver:
        pass

    @abstractmethod
    async def __aexit__(self,
        et: Optional[Type[BaseException]],
        ev: Optional[BaseException],
        tb: Optional[TracebackType],
    ) -> bool:
        pass

    @abstractmethod
    async def get_initial_check_point(self) -> str:
        pass

    @abstractmethod
    async def fetch_root_node(self) -> Node:
        pass

    @abstractmethod
    async def fetch_changes(self,
        check_point: str,
    ) -> AsyncGenerator[Tuple[str, List[ChangeDict]], None]:
        pass

    @abstractmethod
    async def create_folder(self,
        parent_node: Node,
        folder_name: str,
        private: Optional[PrivateDict],
        exist_ok: bool,
    ) -> Node:
        pass

    @abstractmethod
    async def rename_node(self,
        node: Node,
        new_parent: Optional[Node],
        new_name: Optional[str],
    ) -> Node:
        pass

    @abstractmethod
    async def trash_node(self, node: Node) -> None:
        pass

    @abstractmethod
    async def download(self, node: Node) -> ReadableFile:
        pass

    @abstractmethod
    async def upload(self,
        parent_node: Node,
        file_name: str,
        file_size: Optional[int],
        mime_type: Optional[str],
        media_info: Optional[MediaInfo],
        private: Optional[PrivateDict],
    ) -> WritableFile:
        pass

    @abstractmethod
    async def get_hasher(self) -> Hasher:
        pass


Middleware = RemoteDriver
