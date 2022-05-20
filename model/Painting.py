# Representa a la clase Painting en el almacenamiento

from datetime import datetime


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

    # funcion para agregar los puntos a la publicacion cuando es puntuada
    def add_points(self, p):
        self._points += p

    # funciones que formatean la fecha para usarlo en el __str__
    def formatted_date(self):
        return f"{self._date.day:02d}/{self._date.month:02d}/{self._date.year:04d}"

    def formatted_hour(self):
        return f"{self._date.hour:02d}:{self._date.minute:02d}"

    def __str__(self):
        return f"\"{self.title}\" by {self.author}, " \
               f"posted on {self.formatted_date()} at {self.formatted_hour()} h. " \
               f"Points: {self.points}\n"
