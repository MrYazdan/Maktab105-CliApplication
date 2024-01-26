from abc import ABC, abstractmethod


class Model(ABC):
    @classmethod
    @property
    @abstractmethod
    def STORE(cls):  # noqa
        raise NotImplementedError("'DATABASE' not implemented")

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)

        if hasattr(cls, 'STORE'):
            cls.STORE.append(instance)  # noqa

        return instance
