import pickle


class DataBase:
    __instance = None
    __store = {}
    __models = []

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '__instance'):
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, source: str) -> None:
        self.source = source

    def __getitem__(self, key):
        return self.__store[key]

    def __setitem__(self, key, value):
        self.__store[key] = value

    def load(self):
        try:
            with open(self.source, "rb") as f:
                self.__store = pickle.load(f)

                for model in self.__models:
                    model.STORE = self.__store[model.__class__.__name__]
        except (FileNotFoundError, EOFError):
            pass

    def save(self):
        with open(self.source, "wb") as f:
            for model in self.__models:
                self.__store[model.__class__.__name__] = model.STORE

            pickle.dump(self.__store, f)

    def register(self, model):
        self.__models.append(model)
