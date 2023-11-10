import tinyec.ec as ec
from tinyec import registry
from poker_logic import ALL_CARDS

class Deck:
    """Represents a deck of cards using elliptic curve points for secure card representation."""
    
    curve = registry.get_curve('secp256r1')

    def __init__(self):
        """Initializes the deck with 53 'None' placeholders for the base and 52 cards."""
        self.cards = [None] * 53

    def prepare_card(self, point, idx):
        """
        Protocol 1. Prepares a card to be added to the deck by mapping it to an elliptic curve point.
        
        Args:
            point: The elliptic curve point to associate with a card.
            idx: The index of the card in the deck to be prepared.
        """
        if self.cards[idx] is None:
            self.cards[idx] = point
        else:
            self.cards[idx] = self.cards[idx] + point

    def setup_deck_from_xy_coords(self, point_list):
        """
        Sets up the deck using a list of (x, y) coordinates, each representing an elliptic curve point.
        
        Args:
            point_list: A list of (x, y) tuples to be converted to elliptic curve points.
        """
        for i, coords in enumerate(point_list):
            self.cards[i] = ec.Point(self.curve, coords[0], coords[1])

    def to_point_list(self):
        """
        Converts the deck's cards to a list of points.
        
        Returns:
            A list of [x, y] coordinates representing the elliptic curve points of the cards.
        """
        return [[card.x, card.y] for card in self.cards if card is not None]

    def get_mapping(self):
        """
        Creates a mapping from the elliptic curve points to the corresponding card objects.
        
        Returns:
            A dictionary mapping (x, y) tuples to Card objects.
        """
        return {(card.x, card.y): card_obj for card, card_obj in zip(self.cards[1:], ALL_CARDS)}
