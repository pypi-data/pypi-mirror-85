from typing import List

from rich.table import Table

from ..models import ItemWithProject
from ..time import get_time_difference
from .item_mixin import ItemMixin
from .table import TableView


class BasicTableViewWithProjects(TableView, ItemMixin):
    def _create_table(self) -> Table:
        table = Table()
        table.add_column("ID", justify="right", style="cyan", no_wrap=True)
        table.add_column("Title", style="magenta")
        table.add_column("Tags", style="red")
        table.add_column("Status")
        table.add_column("Created", justify="right", style="green")
        table.add_column("Project", style="yellow")
        return table

    def _get_row(self, item: ItemWithProject) -> List[str]:
        row = super()._item_to_row(item)
        row.append(item.project)
        return row
