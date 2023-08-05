from functools import wraps
from typing import Type

import click
import yaml
from rich import print
from inseminator import Container

from .controllers import InitController, TaskController
from .repositories import FileDoesntExistError, TaskRepository, GlobalConfigRepository


container = Container()

task_repository = container.resolve(TaskRepository)
global_config_repository = container.resolve(GlobalConfigRepository)
task_controller = container.resolve(TaskController)
init_controller = container.resolve(InitController)


class AliasedGroup(click.Group):
    def get_command(self, ctx, cmd_name):
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        matches = [x for x in self.list_commands(ctx) if x.startswith(cmd_name)]
        if not matches:
            return None
        elif len(matches) == 1:
            return click.Group.get_command(self, ctx, matches[0])
        ctx.fail("Too many matches: %s" % ", ".join(sorted(matches)))


def catch_init_not_found(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except FileDoesntExistError:
            print("Project is not initialized :(")
            exit(1)

    return wrapper


@click.group(cls=AliasedGroup)
def cli() -> None:
    pass


@click.command()
def init() -> None:
    init_controller.init()


@click.command()
@click.option("-a", "--all-projects", default=False, type=bool, is_flag=True)
@catch_init_not_found
def list(all_projects: bool) -> None:
    task_controller.list(all_projects)


@click.command()
@click.confirmation_option(prompt="Are you sure you want to drop all your tasks there?")
@catch_init_not_found
def drop() -> None:
    task_repository.drop()
    print("Local tasks lost forever", ":sad_panda:")


@click.command()
@click.option("-s", "--state", default="NEW", type=str)
@click.argument("title", type=str, nargs=-1)
@catch_init_not_found
def add(state: str, title: str) -> None:
    task_controller.add(state, title)


@click.command()
@click.argument("task_id", type=int)
@catch_init_not_found
def remove(task_id: int) -> None:
    task_controller.remove(task_id)


@click.command()
@click.argument("task_id", type=int)
@catch_init_not_found
def edit(task_id: int) -> None:
    task_controller.edit(task_id)


@click.command()
@catch_init_not_found
def config() -> None:
    config = global_config_repository.get_config()
    print(yaml.dump(config.dict()))


@click.command()
@click.argument("name", type=str)
@click.argument("value", type=str)
@catch_init_not_found
def set_config(name: str, value: str) -> None:
    global_config_repository.set_config(name, value)


@click.command()
@catch_init_not_found
def projects() -> None:
    # TODO: move to controller
   for project in global_config_repository.get_all_projects():
        print(f" - {project}")


@click.command()
def version() -> None:
    import importlib.metadata
    print(importlib.metadata.version('todo-tasks'))


cli.add_command(add)
cli.add_command(edit)
cli.add_command(remove)
cli.add_command(list)
cli.add_command(init)
cli.add_command(drop)
cli.add_command(config)
cli.add_command(set_config)
cli.add_command(projects)
cli.add_command(version)
