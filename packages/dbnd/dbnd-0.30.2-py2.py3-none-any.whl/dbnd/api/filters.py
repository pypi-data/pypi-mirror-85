class MFilter:
    def __init__(self, value):
        self.value = value if value else []

    def concat(self, func, value):
        return MFilter(self.value + filter_concat(func, value).value)


def filter_concat(func, value):
    return MFilter([func(value)] if value is not None else [])


def build_filter(name, operator, value):
    return {"name": name, "op": operator, "val": value}
