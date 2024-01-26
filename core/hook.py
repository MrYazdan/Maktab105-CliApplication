import enum
from typing import Callable


class Mode(enum.Enum):
    INITIAL = "initial"
    START = "start"
    FINISH = "finish"


class Hook:
    MODE = Mode
    __registered = {}

    def __init__(self, mode: Mode, _callable: Callable, *args, **kwargs):
        assert isinstance(mode, Mode), "mode must be an instance of hook Mode"
        self.mode = mode.value

        assert callable(_callable), "_callable must be callable"
        self.callable = _callable

        self.args = args
        self.kwargs = kwargs

    @classmethod
    def register(cls, instance: object | list | tuple):
        if isinstance(instance, cls):
            cls.__registered[instance.mode] = cls.__registered.get(instance.mode, []) + [instance]

        elif isinstance(instance, (list, tuple)):
            for hook in instance:
                cls.register(hook)

    @classmethod
    @property
    def registered(cls): # noqa
        return cls.__registered

    def __call__(self):
        return self.callable(*self.args, **self.kwargs)
