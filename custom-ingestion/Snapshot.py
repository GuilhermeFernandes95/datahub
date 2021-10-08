from abc import ABC, abstractmethod
from Input import Input
from Path import Path
from Owner import Owner
from Tag import Tag


class Snapshot(ABC):

    @abstractmethod
    def __init__(self,
                 number: int,
                 title: str,
                 description: str,
                 link: str,
                 owners: list,  # name of the corpuser (user id name)
                 inputs: list,
                 tags: list,
                 paths: list) -> object:
        self.number = number
        self.title = title
        self.description = description
        self.link = link
        self.owners = owners
        self.tags = tags
        self.paths = paths
        self.inputs = inputs

    def __str__(self):
        return f"{self.type} number {self.number}, with tile '{self.title}', and description '{self.description}' \n" \
               f"Inputs: {Input.get_input_entries(self.inputs)} \n Paths: {Path.get_path_entries(self.paths, self.get_urn_path())} " \
               f"\n Owners: {Owner.get_owner_entries(self.owners)} \n Tags: {Tag.get_tag_entries(self.tags)}"

    # Instance methods
    def get_urn_path(self) -> str:
        return ','.join([self.platform, ' '.join([self.platform, self.type, str(self.number)])])

    @staticmethod
    def get_tag_entries(tags: list) -> str:
        return ',\n'.join([x._get_tag_entry() for x in tags])

    @staticmethod
    # Chart and Dashboard urn are defined by <tool>,<id>
    def get_path_entries(paths: list, urn: str) -> str:
        return ',\n'.join([f"\"{p._get_path(i=i, id=urn.split(',')[1])}\"" for i, p in enumerate(paths)])

    @staticmethod
    def get_input_entries(inputs: list, snapshot_type: str) -> str:
        if snapshot_type == 'chart':
            return ',"inputs": [' + ',\n'.join(list(map(lambda x: x._get_input_entry(), inputs))) + ']'
        else:
            return ''

    @staticmethod
    def get_owner_entries(owners: list) -> str:
        return ',\n'.join([f"{p._get_owner_entry(i=i)}" for i, p in enumerate(owners)])
