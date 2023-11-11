import time
from deck import Deck
from player_connection import PlayerConnection
from poker_logic import Hand
from protocol import gen_rand_elem

HAND_SIZE = 7

def prepare_deck(player):
    """
    Prepare the deck by sending random elements for each card.
    """
    card_prep_msg = []
    for i in range(53):
        (g, gl, h, hl, r, t) = gen_rand_elem(player.curve)
        card_prep_msg.append([[g.x, g.y], [gl.x, gl.y], [h.x, h.y], [hl.x, hl.y], r, t])
        player.deck.prepare_card(hl, i)
    player.send_to_nodes({
        "type": "CARD_PREP",
        "cards": card_prep_msg
    })

def verify_deck(alice, bob):
    """
    Verify that both players have the same deck.
    """
    for i in range(53):
        if alice.deck.cards[i] != bob.deck.cards[i]:
            print(f"FAILURE VERIFYING NIZK FOR CARD {i}!!! WE SHOULD ABORT")
            return False
        else:
            print(f"SUCCESSFULLY GENERATED CARD {i}: ({alice.deck.cards[i].x},{alice.deck.cards[i].y})")
    return True

def start_game(alice, bob):
    """
    Start the game by initializing players and connecting them.
    """
    alice.start()
    bob.start()
    time.sleep(1)
    alice.connect_with_node('127.0.0.1', 10002)
    time.sleep(2)

def exchange_greetings(alice, bob):
    """
    Exchange greetings between players.
    """
    alice.send_to_nodes({"type": "HELLO", "name": "alice"})
    bob.send_to_nodes({"type": "HELLO", "name": "bob"})
    time.sleep(1)

def shuffle_and_draw(alice, bob):
    """
    Shuffle the deck and draw cards for both players.
    """
    alice.send_to_nodes({"type": "START_SHUFFLE"})
    time.sleep(30)
    bob.send_to_nodes({"type": "START_SHUFFLE"})
    time.sleep(30)
    alice.send_to_nodes({"type": "DRAW_CARDS", "idxs": list(range(1, HAND_SIZE + 1))})
    bob.send_to_nodes({"type": "DRAW_CARDS", "idxs": list(range(HAND_SIZE + 1, 2 * HAND_SIZE + 1))})
    time.sleep(10)

def reveal_and_compare_hands(alice, bob, card_mapping):
    """
    Reveal both players' hands and determine the winner.
    """
    alice_hand = Hand(card_mapping[alice.hand[i][0].x, alice.hand[i][0].y] for i in range(HAND_SIZE))
    bob_hand = Hand(card_mapping[bob.hand[i][0].x, bob.hand[i][0].y] for i in range(HAND_SIZE))
    print(f"Alice's hand: {alice_hand}")
    print(f"Bob's hand: {bob_hand}")
    alice.send_to_nodes({"type": "REQUEST_REVEAL"})
    bob.send_to_nodes({"type": "REQUEST_REVEAL"})
    time.sleep(20)
    if alice_hand > bob_hand:
        print(f'Alice beats Bob with a hand of {alice_hand.description} over {bob_hand.description}.')
    elif alice_hand < bob_hand:
        print(f'Bob beats Alice with a hand of {bob_hand.description} over {alice_hand.description}.')
    else:
        print(f'Alice and Bob split the pot both with hands of {alice_hand.description}.')

def main():
    """
    Main function to run the mental poker game.
    """
    deck = Deck()
    alice = PlayerConnection("127.0.0.1", 10001, id='alice')
    bob = PlayerConnection("127.0.0.1", 10002, id='bob')
    start_game(alice, bob)
    exchange_greetings(alice, bob)
    prepare_deck(alice)
    time.sleep(30)  # Wait for deck preparation
    if not verify_deck(alice, bob):
        return  # Abort if deck verification fails
    card_mapping = alice.deck.get_mapping()
    shuffle_and_draw(alice, bob)
    reveal_and_compare_hands(alice, bob, card_mapping)
    alice.stop()
    bob.stop()

if __name__ == "__main__":
    main()
