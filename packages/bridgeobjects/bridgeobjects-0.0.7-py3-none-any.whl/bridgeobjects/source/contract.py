"""The contract object for the bridgeobjects module."""

from .denomination import Denomination
from .call import Call
from .suit import Suit
from .constants import CONTRACTS, SEATS, SUITS

__all__ = ['Contract']


class Contract(object):
    """
    A Contract object for the bridgeobjects module.

    A contract has a declarer, a denomination.

    Parameters
    ----------
    name: (str) call's name
    declarer: (str) the declarer's seat name

    Example
    -------
        contract = Contarct("3NTX", "S")

    It is also identified (if appropriate) as either major, minor or no trumps.
    """

    def __init__(self, name='', declarer=''):
        self._name = name
        self._is_nt = False
        if name and self._is_valid(name):
            self._call = Call(name)
            self._denomination = self._get_denomination(name)
            if self._denomination:
                self._is_nt = self._denomination.is_nt
            if self._is_nt:
                self._trump_suit = None
            else:
                self._trump_suit = SUITS[self._name[1]]
        else:
            self._trump_suit = None
            self._call = Call('')
            self._denomination = None
        self._declarer = declarer

    def __repr__(self):
        """Return the repr string for the object."""
        return f'Contract("{self._call.name}", "{self._declarer}")'

    def __str__(self):
        """Return the str string for the object."""
        return f'Contract. {self._call.name} by {self._declarer}'

    @property
    def declarer(self):
        """Return the declarer value."""
        return self._declarer

    @declarer.setter
    def declarer(self, value):
        """Assign the declarer value."""
        if value and value not in SEATS:
            raise ValueError(f"'{value}' is not a valid seat")
        self._declarer = value

    @property
    def name(self):
        """Return the name value."""
        return self._name

    @name.setter
    def name(self, value):
        """Assign the name value."""
        if self._is_valid(value):
            self._denomination = self._get_denomination(value)
            self._is_nt = self._denomination.is_nt
            self._trump_suit = SUITS[value[1]]
        self._name = value
        self._call = Call(self._name)

    @property
    def call(self):
        """Return the call value."""
        return self._call

    @call.setter
    def call(self, value):
        """Assign the denomination value."""
        if isinstance(value, str):
            if value in CONTRACTS:
                value = Call(value)
            else:
                raise ValueError(f'{value} is not a valid Call')
        elif not isinstance(value, Call):
            raise TypeError(f'{value} is not a Call')
        self._call = value
        self._denomination = self._get_denomination(value.name)
        self._is_nt = self._denomination.is_nt or self._denomination.is_no_trumps

    @property
    def trump_suit(self):
        """Return a value for the trump suit as a Suit."""
        return self._trump_suit

    @trump_suit.setter
    def trump_suit(self, value):
        """Set the value of the trump suit as a Suit."""
        if isinstance(value, str) and value in SUITS:
            value = SUITS[value]
        elif not isinstance(value, Suit):
            raise TypeError(f'{value} is not a suit.')
        self._denomination = Denomination(value.name)
        self._trump_suit = value

    @property
    def denomination(self):
        """Return the denomination value."""
        return self._denomination

    @property
    def is_nt(self):
        """Return True if the denomination is NT."""
        return self._is_nt

    @staticmethod
    def _is_valid(name):
        """Return True if the contact name is valid."""
        if name not in CONTRACTS:
            raise ValueError(f'{name} is not a valid contract')
        return True

    @staticmethod
    def _get_denomination(name):
        """Return the denomination of the contract."""
        if name[1:3] == 'NT':
            return Denomination('NT')
        else:
            return Denomination(name[1])
