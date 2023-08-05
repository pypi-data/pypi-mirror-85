from abc import ABC, abstractmethod
from typing import Generic, List, TypeVar

from rich import print
from rich.console import Console
from rich.table import Table

T = TypeVar("T")


class TableView(ABC, Generic[T]):
    def __init__(self, items: List[T]) -> None:
        self._items = items

    @abstractmethod
    def _create_table(self) -> Table:
        pass

    @abstractmethod
    def _get_row(self, item: T) -> List[str]:
        pass

    def print(self) -> None:
        console = Console()
        table = self._create_table()

        for item in self._items:
            table.add_row(*self._get_row(item))

        console.print(table)
