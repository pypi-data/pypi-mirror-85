"""CLI."""
from typing import Optional

import typer

from .cache import CacheManager
from .client import Client
from .colors import Color
from .filter.manager import FilterManager
from .priorities import PriorityManager

manabase = typer.Typer()


@manabase.command()
def generate(  # pylint: disable=too-many-arguments
    colors: str,
    filters: Optional[str] = None,
    lands: int = 23,
    occurrences: int = 4,
    priorities: Optional[str] = None,
    clear_cache: Optional[bool] = False,
):
    """Generate a manabase."""
    color_list = Color.from_string(colors)

    if filters is not None:
        filter_manager = FilterManager.from_string(filters, color_list)
    else:
        filter_manager = FilterManager.default(color_list)

    cache = CacheManager()

    if priorities is not None:
        priority_manager = PriorityManager.from_string(
            priorities,
            lands,
            occurrences,
        )
    else:
        priority_manager = PriorityManager.default(
            lands,
            occurrences,
        )

    if clear_cache or not cache.has_cache():

        client = Client()

        # TODO: #5 Multithread that part, it takes longer than forever.
        cards = client.fetch()

        cache.write_cache(cards)

    else:
        cards = cache.read_cache()

    # TODO: #1 Cache filtering results. It should be invalidated if the query
    # cache is invalidated.
    filtered_cards = filter_manager.filter_cards(cards)

    filtered_cards.sort()

    truncated_cards = priority_manager.truncate_cards(filtered_cards)

    # TODO: #12 Support more formatting options.
    print("\n".join([card.name for card in truncated_cards]))


if __name__ == "__main__":
    manabase()
