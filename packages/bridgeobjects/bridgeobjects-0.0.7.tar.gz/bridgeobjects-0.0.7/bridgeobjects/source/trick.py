"""A class to represent a bridgeobjects Trick,"""

from .constants import SEATS, CARD_NAMES
from .card import Card


__all__ = ['Trick',]


class Trick(object):
    """A trick object for the board player."""
    def __init__(self, index, cards=None):
        if not isinstance(index, int):
            raise TypeError('Index must be integer')
        if index not in range(13):
            raise ValueError('Invalid index')
        if not cards:
            cards = []
        self.index = index
        self.cards = cards
        self.start_suit = None
        self._leader = None
        self.winner = None
        self.note_keys = ['' for _ in range(4)]

    def __repr__(self):
        """ A repr string for the object."""
        return f'Trick({self.index}, {[card.name for card in self._cards]})'

    def __str__(self):
        """ A str string for the object."""
        cards = ', '.join([card.name for card in self._cards])
        text = (f'Trick. Index: {self.index}, leader: {self._leader}, winner: {self.winner}, '
                f'start suit: {self.start_suit}, cards: {cards}')
        leader = self._leader
        winner = self.winner
        cards = [card.name for card in self._cards]
        return text.format(self.index, leader, winner, self.start_suit, ', '.join(cards))

    def complete(self, trump_suit=None):
        """Complete the trick fields."""
        if len(self._cards) != 4:
            raise ValueError(f'Trick contains {len(self._cards)} card(s)')
        suit = self._cards[0].suit
        max_value = -1
        leader = SEATS.index(self._leader)
        winner_seat = 0
        for index, card in enumerate(self._cards):
            value = card.value
            if card.suit != suit:
                if trump_suit:
                    if card.suit == trump_suit:
                        value += 13
                    else:
                        value = 0
                else:
                    value = 0
            if value > max_value:
                max_value = value
                winner_seat = index
        self.winner = SEATS[(leader + winner_seat) % 4]

    @property
    def cards(self):
        """Return the cards as a list."""
        return self._cards

    @cards.setter
    def cards(self, value):
        """Set the value of the cards list."""
        if not isinstance(value, list):
            raise TypeError('Cards not a list.')
        card_list = []
        for card in value:
            if isinstance(card, str):
                if card not in CARD_NAMES:
                    raise ValueError('Invalid card name')
                card = Card(card)
            elif not isinstance(card, Card):
                raise TypeError('Item is not a card')
            card_list.append(card)
        self._cards = card_list
        
    @property
    def leader(self):
        """Return  seat of the leader as a string."""
        return self._leader

    @leader.setter
    def leader(self, value):
        """Set the value of the leader as a string."""
        if not isinstance(value, str):
            raise TypeError('Leader must be a string')
        if value not in SEATS:
            raise ValueError('Invalid seat')
        self._leader = value
