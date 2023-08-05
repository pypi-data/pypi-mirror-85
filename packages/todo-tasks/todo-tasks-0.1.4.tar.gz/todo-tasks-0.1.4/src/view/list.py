from abc import ABC, abstractmethod
from typing import Generic, List, TypeVar

from rich import print
from rich.console import Console
from rich.table import Table

T = TypeVar("T")


class ListView(ABC, Generic[T]):
    def __init__(self, items: List[T]) -> None:
        self._items = items

    @abstractmethod
    def _get_row(self, item: T) -> str:
        pass

    def print(self) -> None:
        for item in self._items:
            print(self._get_row(item))
