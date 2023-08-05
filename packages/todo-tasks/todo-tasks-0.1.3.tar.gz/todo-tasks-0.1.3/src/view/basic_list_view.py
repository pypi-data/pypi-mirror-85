from typing import List

from ..models import Item
from .item_mixin import ItemMixin
from .list import ListView


class BasicListView(ListView, ItemMixin):
    def _get_row(self, item: Item) -> str:
        return " ".join(self._item_to_row(item))
