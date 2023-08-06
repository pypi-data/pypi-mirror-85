"""A set of tests for the bridgeobjects Trick class."""
import pytest

from ..source.trick import Trick
from ..source.card import Card
from ..source.constants import SUITS


def test_trick_repr():
    """Ensure the repr is correct."""
    trick = Trick(3, [Card('AH'), Card('2H'), Card('3H'), Card('4H')])
    assert repr(trick) == "Trick(3, ['AH', '2H', '3H', '4H'])"


def test_trick_str():
    """Ensure the str is correct."""
    trick = Trick(3, [Card('AH'), Card('2H'), Card('3H'), Card('4H')])
    text = ('Trick. Index: 3, leader: None, winner: None, '
                'start suit: None, cards: AH, 2H, 3H, 4H')
    assert str(trick) == text


def test_trick_cards_setter():
    """Ensure the card setter is correct."""
    trick = Trick(1, ['AH', '2H', '3H', '4H'])
    assert repr(trick) == "Trick(1, ['AH', '2H', '3H', '4H'])"

    with pytest.raises(TypeError):
        trick = Trick(2, 'AH')

    with pytest.raises(TypeError):
        trick = Trick(3, [1, 2, 3, 4])

    with pytest.raises(ValueError):
        trick = Trick(4, ['GH', '2H', '3H', '4H'])

    # with pytest.raises(ValueError):
    #     trick = Trick(5, ['AH', '2H', '3H', '4H', '5H'])


def test_trick_index_setter():
    """Ensure the index setter is correct."""
    with pytest.raises(TypeError):
        trick = Trick('4')
    with pytest.raises(TypeError):
        trick = Trick([5])
    with pytest.raises(TypeError):
        trick = Trick(1.1)
    with pytest.raises(ValueError):
        trick = Trick(13)


def test_trick_leader_setter():
    """Ensure the trick leader setter is correct."""
    trick = Trick(6, ['2H', 'AH', '3H', '4H'])
    with pytest.raises(TypeError):
        trick.leader = 1
    with pytest.raises(ValueError):
        trick.leader = 'H'


def test_trick_complete():
    """Ensure the trick complete is correct."""
    trick = Trick(5, ['AH', '2H', '3H', '4H', '5H'])
    with pytest.raises(ValueError):
        trick.complete(SUITS['S'])
    trick = Trick(6, ['2H', 'AH', '3H', '4C'])
    trick.leader = 'E'
    trick.complete(SUITS['S'])
    assert trick.winner == 'S'

    trick = Trick(7, ['2H', 'AH', '3H', '4C'])
    trick.leader = 'E'
    trick.complete()
    assert trick.winner == 'S'

