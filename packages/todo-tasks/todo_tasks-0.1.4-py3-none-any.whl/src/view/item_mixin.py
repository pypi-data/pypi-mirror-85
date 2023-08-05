from typing import List, Optional

from ..models import Item
from ..time import get_time_difference


class ItemMixin:
    def _item_to_row(self, item: Item) -> List[str]:
        return [
            f"#{item.id}",
            item.title,
            self._get_tags(item.tags),
            str(item.state),
            get_time_difference(item.created_at),
        ]

    def _get_tags(self, tags: List[str]) -> str:
        return " ".join(map(lambda i: f"+{i}", tags))
