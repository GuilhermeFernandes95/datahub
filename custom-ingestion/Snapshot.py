from abc import ABC, abstractmethod
from Input import Input


class Snapshot(ABC):

    @abstractmethod
    def __init__(self,
                 number: int,
                 title: str,
                 description: str,
                 link: str,
                 owner: list,
                 inputs: list) -> object:
        self.number = number
        self.title = title
        self.description = description
        self.link = link
        self.owner = owner
        self.inputs = inputs

    def __str__(self):
        return f"{self.type} number {self.number}, with tile '{self.title}', and description '{self.description}' \n" \
               f"Inputs: {Input.get_input_entries(self.inputs)}"
