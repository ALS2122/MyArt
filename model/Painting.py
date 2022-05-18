# Representa a la clase Painting en el almacenamiento

from datetime import datetime

import sirope


class Painting:
    def __init__(self, t, p, a):
        self._title = t
        self._path = p
        self._date = datetime.now()
        self._author = a
        self._points = 0

    @property
    def date(self):
        return self._date

    @property
    def title(self):
        return self._title

    @property
    def path(self):
        return self._path

    @property
    def points(self):
        return self._points

    @property
    def author(self):
        return self._author

    def add_points(self, p):
        self._points += p

    @staticmethod
    def find(srp: sirope.Sirope, title: str) -> "Painting|None":
        return srp.find_first(Painting, lambda p: p.title == title)

    def __str__(self):
        day = self.date.day
        month = self.date.month
        year = self.date.year

        hour = self.date.hour
        minute = self.date.minute

        return f"\"{self.title}\" by {self.author}, " \
               f"posted on {day:02d}/{month:02d}/{year:02d} at {hour:02d}:{minute:02d} h. " \
               f"Points: {self.points}\n"
