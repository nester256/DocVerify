from abc import ABC


class Service(ABC):
    id: int

    def __init__(self, id: int):
        self.id = id
