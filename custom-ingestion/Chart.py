from Snapshot import Snapshot


class Chart(Snapshot):
    snapshot_type = 'Chart'

    def __init__(self,
                 number: int,
                 title: str,
                 description: str,
                 link: str,
                 owners: list,
                 inputs: list,
                 paths: list) -> object:
        super().__init__(number, title, description, link, owners, inputs, paths)
        self.type = self.snapshot_type
