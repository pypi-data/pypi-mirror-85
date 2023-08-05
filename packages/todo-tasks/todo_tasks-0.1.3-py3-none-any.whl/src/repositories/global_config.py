import json
from pathlib import Path
import os
from functools import cached_property
from typing import List

from . import BaseRepository
from ..models import GlobalConfig, Configuration, ListViewType


class GlobalConfigRepository(BaseRepository):
    GLOBAL_CONFIG_FILENANE = ".tasks.config.json"
    model = GlobalConfig

    def __init__(self) -> None:
        globa_config_filename = Path(os.path.expanduser("~")) / self.GLOBAL_CONFIG_FILENANE
        super().__init__(globa_config_filename)

    def add_project(self, project_path: Path) -> None:
        self._data.all_projects.append(str(project_path))

    def get_all_projects(self) -> List[Path]:
        return self._data.all_projects

    def register_project_if_possible(self, project_path: Path) -> None:
        if self._exists() and project_path not in self._data.all_projects:
            self._data.all_projects.append(str(project_path))
            self.save()

    def get_list_view(self) -> ListViewType:
        return self._data.config.list_view

    def set_config(self, name: str, value: str) -> None:
        config = self._data.config
        self._data.config = Configuration(**{**config.dict(), **{name: value}})
        self.save()

    def get_config(self) -> Configuration:
        return self._data.config

    def increase_items_counter(self):
        self._data.items_counter += 1

    def get_items_counter(self) -> int:
        return self._data.items_counter
