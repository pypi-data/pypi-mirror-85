"""CLI."""
from typing import Optional

import typer

from manabase.filler.distribution import WeightedDistribution
from manabase.filler.filler import BasicLandFiller

from .cache import CacheManager
from .client import Client
from .colors import Color
from .filter.manager import FilterManager
from .priorities import PriorityManager

manabase = typer.Typer()


@manabase.command()
def generate(  # pylint: disable=too-many-arguments, too-many-locals
    colors: str,
    filters: Optional[str] = None,
    lands: int = 23,
    occurrences: int = 4,
    priorities: Optional[str] = None,
    clear_cache: Optional[bool] = False,
    filler_weights: Optional[str] = None,
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
    filter_results = filter_manager.filter_cards(cards)

    card_list = priority_manager.build_list(filter_results)

    if card_list.available:
        weights = filler_weights.split() if filler_weights else [1] * len(color_list)
        distribution = WeightedDistribution(
            maximum=card_list.available,
            weights=weights,
        )
        land_filler = BasicLandFiller(colors=color_list, distribution=distribution)
        filler_list = land_filler.generate_filler(card_list.available)
        card_list.update(filler_list)

    # TODO: #12 Support more formatting options.
    print("\n".join([f"{card.occurrences} {card.name}" for card in card_list.entries]))


if __name__ == "__main__":
    manabase()
