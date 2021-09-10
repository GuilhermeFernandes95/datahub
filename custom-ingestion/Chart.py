from Snapshot import Snapshot


class Chart(Snapshot):
    snapshot_type = 'Chart'

    def __init__(self,
                 number: int,
                 title: str,
                 description: str,
                 link: str,
                 owner: list, # name of the corpuser (user id name)
                 inputs: list) -> object:
        super().__init__(number, title, description, link, owner, inputs)
        self.type = self.snapshot_type
