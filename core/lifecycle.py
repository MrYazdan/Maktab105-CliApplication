class Lifecycle:
    def __init__(self, hooks=None):
        self.hooks = hooks
        self.on_mode("initial")

    def __enter__(self):
        self.on_mode("start")
        return self

    def __exit__(self, *args, **kwargs):
        self.on_mode("finish")

    def on_mode(self, mode: str):
        if self.hooks and mode in self.hooks:
            for hook in self.hooks[mode]:
                hook()
