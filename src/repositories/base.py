from abc import ABC


class Repository(ABC):
    def __init__(self, id: int) -> None:
        self.id = id

    pass
