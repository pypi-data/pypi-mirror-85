import os
from pathlib import Path
from typing import List, Optional

from . import GlobalConfigRepository, BaseRepository
from ..models import ProjectData, Item, ItemWithProject, ItemState


class TaskRepository(BaseRepository):
    PROJECT_FILENAME = ".tasks.json"
    model = ProjectData

    def __init__(self, global_config_repository: GlobalConfigRepository, path: Optional[Path] = None) -> None:
        self._project_path = path or Path(os.getcwd())
        self._global_config_repository = global_config_repository
        self._global_config_changed = False
        super().__init__(self._project_path / self.PROJECT_FILENAME)

    def init(self):
        self._global_config_repository.add_project(self._project_path)
        self._global_config_repository.save()

    def list(self) -> List[Item]:
        return self._data.items

    def list_from_all_projects(self) -> List[ItemWithProject]:
        data = []

        for project in self._global_config_repository.get_all_projects():
            project_task_repository = TaskRepository(self._global_config_repository, Path(project))
            for item in project_task_repository.list():
                data.append(ItemWithProject(project=str(project), **item.dict()))

        return data

    def add(self, title: str, state: ItemState) -> None:
        new_item = Item(id=self._global_config_repository.get_items_counter(), state=state, title=title)
        self._data.items.append(new_item)
        self._global_config_changed = True

    def remove(self, task_id: int) -> None:
        self._data.items = [i for i in self._data.items if i.id != task_id]

    def save(self):
        super().save()

        if self._global_config_changed:
            self._global_config_repository.save()

    def _get_item_id_by_task_id(self, task_id: int) -> int:
        return next(i for i, item in enumerate(self._data.items) if item.id == task_id)

    def get_by_id(self, task_id: int) -> Item:
        return self._data.items[self._get_item_id_by_task_id(task_id)]

    def update(self, task_id: int, value: dict) -> None:
        item_id = self._get_item_id_by_task_id(task_id)
        origin_value = self._data.items[item_id]
        self._data.items[item_id] = Item(**{**origin_value.dict(), **value})
