from ..models import ItemWithProject
from .item_mixin import ItemMixin
from .list import ListView


class BasicListViewWithProject(ListView, ItemMixin):
    def _get_row(self, item: ItemWithProject) -> str:
        return " ".join(self._item_to_row(item) + [item.project])
