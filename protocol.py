import hashlib
import hmac
import secrets
from deck import Deck

SHUFFLE_SECURITY_PARAM = 5
HMAC_KEY = b"b4300d6f7170bc50bc5569b66cf21e3ee0dad1604577dc68279dd6907af40e48"


def gen_nizk_dleq(curve, g, gx, h, hx, x):
    """
    Generate a non-interactive zero-knowledge proof of discrete logarithm equality.

    Args:
        curve: The elliptic curve used.
        g: The generator point of the curve.
        gx: The point g multiplied by secret x.
        h: Another generator point of the curve.
        hx: The point h multiplied by secret x.
        x: The secret value.

    Returns:
        A tuple of (r, t) where r is a random value and t is the response.
    """
    r = secrets.randbelow(curve.field.n)
    gr = g * r
    hr = h * r
    c = int(
        hmac.new(
            HMAC_KEY,
            f"{gr.x}{gr.y}{hr.x}{hr.y}{gx.x}{gx.y}{hx.x}{hx.y}".encode("utf-8"),
            hashlib.sha256,
        ).hexdigest(),
        16,
    )
    t = r + c * x
    return r, t


def verify_nizk_dleq(g, gx, h, hx, r, t):
    """
    Verify a non-interactive zero-knowledge proof of discrete logarithm equality.

    Args:
        g, gx, h, hx: The elliptic curve points involved in the proof.
        r: The random value from the prover.
        t: The response from the prover.

    Returns:
        True if the proof is valid, False otherwise.
    """
    gr = g * r
    hr = h * r
    c = int(
        hmac.new(
            HMAC_KEY,
            f"{gr.x}{gr.y}{hr.x}{hr.y}{gx.x}{gx.y}{hx.x}{hx.y}".encode("utf-8"),
            hashlib.sha256,
        ).hexdigest(),
        16,
    )
    gt = g * t
    ht = h * t
    gxc = gx * c
    hxc = hx * c
    return (gt == gr + gxc) and (ht == hr + hxc)


def gen_rand_elem(curve):
    """
    Generate a random element for the deck preparation protocol along with a ZKA of Discrete Logarithm Equality.

    Args:
        curve: The elliptic curve used.

    Returns:
        A tuple of (g, gx, h, hx, r, t) where g and h are random points on the curve, gx and hx are these points multiplied by a secret x, and r and t are used for the ZKA.
    """
    g = secrets.randbelow(curve.field.n) * curve.g
    h = secrets.randbelow(curve.field.n) * curve.g
    x = secrets.randbelow(curve.field.n)
    gx = g * x
    hx = h * x
    (r, t) = gen_nizk_dleq(curve, g, gx, h, hx, x)
    return g, gx, h, hx, r, t


def fisher_yates_shuffle(s):
    """
    Perform an unbiased permutation generation using the Fisher-Yates shuffle algorithm.

    Args:
        s: The sequence to shuffle.

    Returns:
        The shuffled sequence.
    """
    for i in range(len(s) - 1):
        j = secrets.randbelow(len(s) - i) + i
        s[i], s[j] = s[j], s[i]
    return s


def shuffle_cards(deck):
    """
    Shuffle the deck using the Fisher-Yates shuffle algorithm and apply a secret multiplier.

    Args:
        deck: The deck to shuffle.

    Returns:
        A tuple of the secret multiplier, the permutation, and the shuffled deck.
    """
    shuffled_deck = Deck()
    permutation = list(range(1, len(deck.cards)))
    permutation = [0] + fisher_yates_shuffle(permutation)
    x = secrets.randbelow(deck.curve.field.n)
    for i in range(len(deck.cards)):
        shuffled_deck.cards[i] = deck.cards[permutation[i]] * x
    return x, permutation, shuffled_deck


def apply_shuffle(deck, shuffle):
    """
    Apply the specified permutation to the deck.

    Args:
        deck: The deck to apply the permutation to.
        shuffle: The permutation to apply.

    Returns:
        The shuffled deck.
    """
    shuffled_deck = Deck()
    for i in range(len(deck.cards)):
        shuffled_deck.cards[i] = deck.cards[shuffle[i]]
    return shuffled_deck


def compose_shuffles(s1, s2):
    """
    Compose two permutations into one.

    Args:
        s1: The first permutation.
        s2: The second permutation.

    Returns:
        The composition of the two permutations.
    """
    return [s1[idx] for idx in s2]


def gen_nizk_shuffle(deck):
    """
    Protocol 3. Generate a non-interactive zero-knowledge proof for a shuffle of a deck.

    Args:
        deck: The deck to shuffle.

    Returns:
        A tuple of the secret, the permutation, the shuffled deck, and a list of 3-tuples for the ZKA protocol.
    """
    (x, p, shuffled_deck) = shuffle_cards(deck)
    m = []
    for i in range(SHUFFLE_SECURITY_PARAM):
        (y, p_prime, c) = shuffle_cards(shuffled_deck)
        rom_query = "".join(f"{z.x}{z.y}" for z in deck.cards)
        rom_query += "".join(f"{z.x}{z.y}" for z in shuffled_deck.cards)
        rom_query += "".join(f"{z.x}{z.y}" for z in c.cards)
        e = (
            int(
                hmac.new(
                    HMAC_KEY, rom_query.encode("utf-8"), hashlib.sha256
                ).hexdigest(),
                16,
            )
            & 1
        )
        if e == 0:
            m.append((c, y, p_prime))
        else:
            pp_prime = compose_shuffles(p, p_prime)
            m.append((c, x * y, pp_prime))
    return x, p, shuffled_deck, m


def verify_nizk_shuffle(deck, shuffled_deck, m):
    """
    Protocol 4. Verify a non-interactive zero-knowledge proof for a shuffle of a deck.

    Args:
        deck: The original deck.
        shuffled_deck: The shuffled deck.
        m: The message containing the proof.

    Returns:
        True if the shuffle is verified, False otherwise.
    """
    for i in range(SHUFFLE_SECURITY_PARAM):
        c, y, p = m[i]
        rom_query = "".join(f"{z.x}{z.y}" for z in deck.cards)
        rom_query += "".join(f"{z.x}{z.y}" for z in shuffled_deck.cards)
        rom_query += "".join(f"{z.x}{z.y}" for z in c.cards)
        e = (
            int(
                hmac.new(
                    HMAC_KEY, rom_query.encode("utf-8"), hashlib.sha256
                ).hexdigest(),
                16,
            )
            & 1
        )
        ds = Deck()
        for j in range(len(deck.cards)):
            ds.cards[j] = shuffled_deck.cards[j] * y if e == 0 else deck.cards[j] * y
        ds = apply_shuffle(ds, p)
        if any(ds.cards[j] != c.cards[j] for j in range(len(deck.cards))):
            return False
    return True
