from abc import ABC, abstractmethod
from Input import Input
from Path import Path
from Owner import Owner


class Snapshot(ABC):

    @abstractmethod
    def __init__(self,
                 number: int,
                 title: str,
                 description: str,
                 link: str,
                 owners: list,  # name of the corpuser (user id name)
                 inputs: list,
                 paths: list) -> object:
        self.number = number
        self.title = title
        self.description = description
        self.link = link
        self.owners = owners
        self.inputs = inputs
        self.paths = paths

    def __str__(self):
        return f"{self.type} number {self.number}, with tile '{self.title}', and description '{self.description}' \n" \
               f"Inputs: {Input.get_input_entries(self.inputs)} \n Paths: {Path.get_path_entries(self.paths)} " \
               f"\n Owners: {Owner.get_owner_entries(self.owners)}"
