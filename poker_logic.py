from collections import Counter
from dataclasses import dataclass, field
from enum import IntEnum, Enum, auto
from itertools import product
from operator import itemgetter
from typing import FrozenSet, Iterable, NamedTuple, Optional, Set, Tuple


class Rank(IntEnum):
    """Enumeration for card ranks."""

    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14


class Suit(Enum):
    """Enumeration for card suits."""

    CLUBS = auto()
    HEARTS = auto()
    DIAMONDS = auto()
    SPADES = auto()


class Card(NamedTuple):
    """Representation of a single playing card."""

    rank: Rank
    suit: Suit

    def __str__(self):
        """String representation of a Card."""
        return f"{self.rank.name.title()} of {self.suit.name.lower()}"


class HandRank(IntEnum):
    """Enumeration for poker hand ranks."""

    HIGH_CARD = 1
    PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_OF_A_KIND = 8
    STRAIGHT_FLUSH = 9
    ROYAL_FLUSH = 10


def flush_card_ranks(cards: Iterable[Card]) -> Optional[Set[Rank]]:
    """
    Determines if a flush exists in the given cards and returns the ranks if it does.

    Args:
        cards: An iterable collection of Card objects.

    Returns:
        A set of Rank objects if a flush is found, None otherwise.
    """
    suit_counts = Counter(card.suit for card in cards)
    suit, count = suit_counts.most_common(1)[0]
    if count >= 5:
        return {card.rank for card in cards if card.suit == suit}
    return None


def highest_straight(ranks: Iterable[Rank]) -> Optional[Rank]:
    """
    Identifies the highest straight in the given ranks.

    Args:
        ranks: An iterable collection of Rank objects.

    Returns:
        The highest Rank object that is part of a straight, or None if no straight is found.
    """
    rank_set = set(ranks)
    return max(
        (
            Rank(highest_val)
            for highest_val, straight in STRAIGHTS.items()
            if straight.issubset(rank_set)
        ),
        default=None,
    )


def best_hand(cards: Iterable[Card]) -> Tuple[HandRank, Tuple, str]:
    """
    Determines the best poker hand from the given cards.

    Args:
        cards: An iterable collection of Card objects.

    Returns:
        A tuple containing the HandRank enumeration, a tie-breaking tuple, and a string description of the hand.
    """
    card_ranks = [card.rank for card in cards]
    rank_counts = Counter(card_ranks)
    sorted_counts = sorted(rank_counts.items(), key=itemgetter(1, 0), reverse=True)
    sorted_ranks = tuple(sorted(card_ranks, reverse=True))

    flush = flush_card_ranks(cards)

    # Check for straight flush or royal flush
    if flush:
        straight_val = highest_straight(flush)
        if straight_val:
            if straight_val == Rank.ACE:
                return HandRank.ROYAL_FLUSH, (), "Royal flush"
            return (
                HandRank.STRAIGHT_FLUSH,
                (straight_val,),
                f"{straight_val.name.title()}-high straight flush",
            )

    # Check for four of a kind
    if sorted_counts[0][1] == 4:
        four_of_a_kind_rank = sorted_counts[0][0]
        kicker = max(rank for rank in card_ranks if rank != four_of_a_kind_rank)
        return (
            HandRank.FOUR_OF_A_KIND,
            (four_of_a_kind_rank, kicker),
            f"Four of a kind: {four_of_a_kind_rank.name.title()} with {kicker.name.title()} kicker",
        )

    # Check for full house
    if sorted_counts[0][1] == 3 and sorted_counts[1][1] >= 2:
        three_of_a_kind_rank = sorted_counts[0][0]
        pair_rank = sorted_counts[1][0]
        return (
            HandRank.FULL_HOUSE,
            (three_of_a_kind_rank, pair_rank),
            f"Full house: {three_of_a_kind_rank.name.title()}s over {pair_rank.name.title()}s",
        )

    # Check for flush
    if flush:
        flush_ranks = tuple(sorted(flush, reverse=True))[:5]
        return (
            HandRank.FLUSH,
            flush_ranks,
            f'Flush: {" ".join(rank.name.title() for rank in flush_ranks)}',
        )

    # Check for straight
    straight_val = highest_straight(card_ranks)
    if straight_val:
        return (
            HandRank.STRAIGHT,
            (straight_val,),
            f"Straight: {straight_val.name.title()}-high",
        )

    # Check for three of a kind
    if sorted_counts[0][1] == 3:
        three_of_a_kind_rank = sorted_counts[0][0]
        kickers = tuple(rank for rank in sorted_ranks if rank != three_of_a_kind_rank)[
            :2
        ]
        return (
            HandRank.THREE_OF_A_KIND,
            (three_of_a_kind_rank,) + kickers,
            f'Three of a kind: {three_of_a_kind_rank.name.title()} with kickers {" ".join(kicker.name.title() for kicker in kickers)}',
        )

    # Check for two pair
    if sorted_counts[1][1] == 2:
        higher_pair_rank = sorted_counts[0][0]
        lower_pair_rank = sorted_counts[1][0]
        kicker = max(
            rank
            for rank in card_ranks
            if rank not in (higher_pair_rank, lower_pair_rank)
        )
        return (
            HandRank.TWO_PAIR,
            (higher_pair_rank, lower_pair_rank, kicker),
            f"Two pair: {higher_pair_rank.name.title()}s and {lower_pair_rank.name.title()}s with {kicker.name.title()} kicker",
        )

    # Check for one pair
    if sorted_counts[0][1] == 2:
        pair_rank = sorted_counts[0][0]
        kickers = tuple(rank for rank in sorted_ranks if rank != pair_rank)[:3]
        return (
            HandRank.PAIR,
            (pair_rank,) + kickers,
            f'One pair: {pair_rank.name.title()} with kickers {" ".join(kicker.name.title() for kicker in kickers)}',
        )

    # High card
    high_cards = sorted_ranks[:5]
    return (
        HandRank.HIGH_CARD,
        high_cards,
        f'High card: {" ".join(rank.name.title() for rank in high_cards)}',
    )


@dataclass(order=True)
class Hand:
    """Represents a poker hand with a rank and cards."""

    hand_rank: HandRank = field(compare=True)
    tie_breaking: Tuple = field(compare=True)
    cards: FrozenSet[Card] = field(compare=False)
    description: str = field(compare=False)

    def __init__(self, cards: Iterable[Card]):
        """Initializes the Hand with the best possible combination from the given cards."""
        self.cards = frozenset(cards)
        self.hand_rank, self.tie_breaking, self.description = best_hand(self.cards)

    def __str__(self):
        """String representation of the Hand."""
        return ", ".join(str(card) for card in self.cards)


ALL_CARDS = [Card(rank, suit) for rank, suit in product(Rank, Suit)]
STRAIGHTS = {
    **{5: {14, 2, 3, 4, 5}},
    **{i: {i - j for j in range(5)} for i in range(6, 15)},
}
