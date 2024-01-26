import uuid

from core.model import Model


class User(Model):
    STORE = []

    @staticmethod
    def _username_validator(username: str) -> bool:
        return isinstance(username, str) and len(username) >= 8 and username.isidentifier()

    @staticmethod
    def _password_validator(password: str) -> bool:
        return isinstance(password, str) and 4 <= len(password) <= 8

    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password
        self.__id = uuid.uuid4().hex

    @property
    def id(self):
        return self.__id

    @property
    def username(self) -> str:
        return f"({self.__username}#)"

    @username.setter
    def username(self, new_username: str) -> None:
        assert self._username_validator(new_username), "Username not valid !"
        self.__username = new_username

    @property
    def password(self):
        return hash(self.__password)

    @password.setter
    def password(self, new_password):
        assert self._password_validator(new_password), "Password not valid !"
        self.__password = new_password

    def profile(self):
        return f"User {self.username} with id {self.id}"

