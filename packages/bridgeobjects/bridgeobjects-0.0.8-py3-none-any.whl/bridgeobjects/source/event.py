"""The Event class for the bridgeobjects package."""

import datetime

__all__ = ['Event']


class Event(object):
    """
    The event object for the bridgeobjects module.

    An event is the collection of boards played as a competition,
    match or drive.

    Parameters
    ----------
    name: (str) the event's name
    date_time: (datetime.datetime) event's date and time
    """
    def __init__(self, name="", date_time=None):
        if date_time:
            if not isinstance(date_time, datetime.datetime):
                raise TypeError(f'{date_time} is not a datetime')
        self._name = name
        if date_time:
            self._date = datetime.date(date_time.year,
                                       date_time.month,
                                       date_time.day)
            self._time = datetime.time(date_time.hour, date_time.minute)
        else:
            self._date = None
            self._time = None
        self._location = ""
        self._session = ""
        self._scoring_method = ""

        self.boards = []

    def __repr__(self):
        return f"Event('{self._name}')"

    def __str__(self):
        event_date = self._date.strftime('%d %b %Y')
        return f'Event. Description: {self._name}, date: {event_date}.'

    @property
    def name(self):
        """Return the event's name as a string."""
        return self._name

    @name.setter
    def name(self, value):
        """Set the name property to an allowed value."""
        self._name = value

    @property
    def location(self):
        """Return the event's location as a string."""
        return self._location

    @location.setter
    def location(self, value):
        """Set the location property to an allowed value."""
        self._location = value

    @property
    def scoring_method(self):
        """Return the event's scoring_method as a string."""
        return self._scoring_method

    @scoring_method.setter
    def scoring_method(self, value):
        """Set the session scoring_method to an allowed value."""
        self._scoring_method = value

    @property
    def date(self):
        """Return the event's date as a datetime.date."""
        return self._date

    @date.setter
    def date(self, value):
        """Set the date property to an allowed value."""
        assert(isinstance(value, datetime.date)), 'value is not a date'
        self._date = value

    @property
    def time(self):
        """Return the event's time as a datetime.time."""
        return self._time
