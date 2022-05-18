# Representa a la clase User en el almacenamiento
from typing import Optional

import flask_login
import werkzeug.security as safe
import sirope


class User(flask_login.UserMixin):
    def __init__(self, username, password):
        self._username = username
        self._password = safe.generate_password_hash(password)
        self._paintings_oids = []  # referencia a todos los paintings del usuario

    @property
    def username(self):
        return self._username

    @property
    def oids_paintings(self):
        if not self.__dict__.get("_paintings_oids"):
            self._paintings_oids = []
        return self._paintings_oids

    def add_painting_oid(self, painting_oid):
        self.oids_paintings.append(painting_oid)

    def find_painting_oid(self, p):
        if self._paintings_oids.__contains__(p):
            return self._paintings_oids.__getitem__(p)

    # Verifica la contraseña
    def check_password(self, p):
        return safe.check_password_hash(self._password, p)

    def get_id(self):
        return self.username

    @staticmethod
    def find(srp: sirope.Sirope, username: str) -> "User|None":
        return srp.find_first(User, lambda u: u.username == username)

    @staticmethod
    def current_user():
        toret = flask_login.current_user

        if toret.is_anonymous:
            flask_login.logout_user()
            toret = None

        return toret
