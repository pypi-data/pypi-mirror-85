import yaml

from ..editor import Editor
from ..repositories import TaskRepository, GlobalConfigRepository
from ..models import Configuration, ListViewType, ItemState
from ..view import BasicListView, BasicListViewWithProject, BasicTableView, BasicTableViewWithProjects, ListView

class TaskController:
    def __init__(self, task_repository: TaskRepository, global_config_repository: GlobalConfigRepository) -> None:
        self._task_repository = task_repository
        self._global_config_repository = global_config_repository

    def list(self, all_projects: bool) -> None:
        list_view = self._global_config_repository.get_list_view()

        if all_projects:
            data = self._task_repository.list_from_all_projects()

            if list_view == ListViewType.TABLE:
                view = BasicTableViewWithProjects(data)
            elif list_view == ListViewType.LIST:
                view = BasicListViewWithProject(data)
        else:
            data = self._task_repository.list()
            if list_view == ListViewType.TABLE:
                view = BasicTableView(data)
            elif list_view == ListViewType.LIST:
                view = BasicListView(data)

        view.print()

    def add(self, state: str, title: str) -> None:
        self._task_repository.add(" ".join(title), ItemState(state))
        self._task_repository.save()
        print("Task saved", ":vampire:")

    def edit(self, task_id: int) -> None:
        task = self._task_repository.get_by_id(task_id)
        editor = Editor(yaml.dump(task.dict(include={"title", "state", "tags"})))
        new_item_dict = yaml.safe_load(editor.edit())
        self._task_repository.update(task_id, new_item_dict)
        self._task_repository.save()

        print("Task edited")

    def remove(self, task_id: int) -> None:
        self._task_repository.remove(task_id)
        self._task_repository.save()
        print("Task removed :sad_panda:")
