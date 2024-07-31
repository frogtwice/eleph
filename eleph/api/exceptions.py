class SingleValuedException[T](Exception):
    def __init__(self, value: T):
        self.value = value


class MissingParameter(SingleValuedException[str]):
    pass


class Redirect(SingleValuedException[str]):
    pass


class UnprocessableEntity(SingleValuedException[str]):
    pass
