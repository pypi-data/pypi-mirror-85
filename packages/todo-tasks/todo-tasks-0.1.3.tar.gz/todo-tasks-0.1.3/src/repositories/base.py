import json
import os
from functools import cached_property
from pathlib import Path
from typing import List, Generic, Type, TypeVar
from abc import ABC, abstractmethod

from pydantic import BaseModel

from .errors import FileAlreadyExistsError, FileDoesntExistError
from ..models import ProjectData, GlobalConfig


T = TypeVar("T", ProjectData, GlobalConfig)


class BaseRepository(ABC, Generic[T]):
    @property
    @abstractmethod
    def model(self) -> Type[T]:
        ...

    def __init__(self, filename: Path) -> None:
        self._filename = filename

    @cached_property
    def _data(self) -> T:
        return self._load()

    def _exists(self) -> bool:
        return os.path.exists(self._filename)

    def _load(self) -> T:
        if not self._exists():
            raise FileDoesntExistError(self._filename)

        with open(self._filename, "r") as f:
            return self.model(**json.load(f))

    def _init(self, data: str) -> None:
        if self._exists():
            raise FileAlreadyExistsError(self._filename)

        with open(self._filename, "w+") as f:
            f.write(data)

    def save(self) -> None:
        with open(self._filename, "w") as f:
            f.write(self._data.json())

    def drop(self) -> None:
        if not self._exists():
            raise FileDoesntExistError(self._filename)

        os.remove(self._filename)
