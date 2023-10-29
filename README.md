# Motivation
Poker has long been a popular card game, but many poker games have moved online. While playing poker online is convenient, ensuring fairness and security without a trusted third party is a significant challenge. This project implements the [Fast Mental Poker protocol by Wei and Wang](https://www.researchgate.net/publication/220334557_A_Fast_Mental_Poker_Protocol), ensuring secure, tamper-resistant, and fair online poker games. Our goal is to use cryptographic techniques to make online poker as trustable as traditional face-to-face games.

# Research
## Secure Peer-to-Peer Communications
- Upon joining a poker table, players establish a peer-to-peer connection.
- Every action a player takes is broadcasted to all other players using authenticated message exchange via the `p2pnetwork` python library.
- This authenticated communication ensures that only legitimate moves by authenticated players are accepted.

## Deck Encryption and Shuffling
Using the sec256k1 prime-order elliptic curve, cards are encrypted in a way that even the player who shuffles the deck cannot know the order. This ensures fairness and prevents cheating. The protocols implemented include protocols 1 - 6 as specified in the paper:
- Protocol 1 (Deck Preparation): Initial deck creation and encryption.
- Protocol 2 (Random Element Generation): Securely generating random values for shuffling.
- Protocol 3 (Shuffle): Players can shuffle the deck without knowing the card order.
- Protocol 4 (Shuffle Verification): All players can verify the fairness of the shuffle.
- Protocol 5 (Card Drawing): Players draw cards securely without revealing them to others.
- Protocol 6 (Card Opening): A player can reveal their card to all others without compromising the game.

# Development
Main Libraries:

1. `p2pnetwork` (For peer-to-peer communication)
2. `ecdsa` (For the elliptic curve cryptography involved in the protocols)
3. `pycryptodome` and `pycryptodomex` (For low-level cryptographic primitives)
4. `gmpy2` (For multiprecision arithmetic in cryptographic computations)
5. `sympy` (A symbolic mathematics library which can be useful for certain mathematical cryptographic operations)
6. `mpmath` (For high-precision arithmetic which might be used for certain cryptographic computations)

# Setup

# Implementation Details
1. Protocol 1 (Deck Preparation): Initial deck creation and encryption
   1. Alice initiates the game by preparing an initial deck of cards.
   2. The deck is then encrypted by Alice, resulting in a deck: E<sub>Alice</sub>(M).
2. Protocol 2 (Random Element Generation): Securely generating random values for shuffling.
   1. Bob generates a random element, which will be used for shuffling and selecting cards from the encrypted deck.
3. Protocol 3 (Shuffle): Players can shuffle the deck without knowing the card order.
   1. Using the random element, Bob shuffles the encrypted deck.
4. Protocol 4 (Shuffle Verification): All players can verify the fairness of the shuffle.
  1. Alice verifies that the shuffled deck is still valid and has not been tampered with.
5. Protocol 5 (Card Drawing): Players draw cards securely without revealing them to others.
   1. For Alice's hand:
      1. Bob uses the random element to select five ciphertexts (representing five cards) from the encrypted deck and sends them back to Alice.
      2. Alice decrypts the selected ciphertexts to reveal her hand.
   2. For Bob's hand:
      1. Bob selects another set of five cards from the deck and doubly encrypts them: E<sub>Bob</sub>(E<sub>Alice</sub>(M)).
      2. This doubly encrypted hand is sent to Alice.
      3. Alice decrypts her layer of encryption and sends the resulting hand back to Bob as E<sub>Bob</sub>(M).
      4. Bob decrypts the received hand to reveal his set of cards.
   3. Alice and Bob maintain a list of selected card indices, crossing out the card numbers picked by Bob.
6. Protocol 6 (Card Opening): A player can reveal their card to all others without compromising the game.
   1. After the card drawing procedure, both Alice and Bob can choose to reveal their hands to each other.
   2. Based on standard poker rules, the player with the best 5-card hand is determined as the winner.