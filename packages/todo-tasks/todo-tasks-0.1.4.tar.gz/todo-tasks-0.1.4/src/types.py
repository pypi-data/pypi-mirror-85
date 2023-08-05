from typing import Protocol

class View(Protocol):
    def print(self) -> str:
        ...
