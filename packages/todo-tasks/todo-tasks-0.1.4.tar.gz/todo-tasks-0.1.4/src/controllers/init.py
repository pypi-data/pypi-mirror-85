from ..repositories import TaskRepository

class InitController:
    def __init__(self, task_repository: TaskRepository) -> None:
        self._task_repository = task_repository

    def init(self) -> None:
        try:
            self._task_repository.init()
            print("Init file already exists", ":sad_panda:")
        except:
            print("Tasks succesfully initialized", ":thumbs_up:")
