from functools import reduce


class Opts(dict):
    def __getattr__(self, name: str):
        return self.get(name)

    def use(self, *keys):
        def decorator(func):
            return reduce(lambda f, key: self.get(key)(f), keys, func)

        return decorator

    def use_all(self):
        return self.uses(*self.keys())
